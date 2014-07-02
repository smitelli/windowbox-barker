from __future__ import absolute_import
import shelve
import requests
from urlparse import urlparse, urlunparse


class WindowboxAPI(object):
    def __init__(self, site_url, state_file, timeout=10):
        self.site_url = site_url
        self.state_file = state_file
        self.timeout = timeout

        self._shelf = shelve.open(filename=self.state_file)

    def walk_new_posts(self):
        start_offset = self._shelf.get('start_offset', 0)

        for post in self._get_posts_since(start_offset):
            yield post

            self._shelf['start_offset'] = post.id
            self._shelf.sync()

    def get_post_url_for(self, post_id):
        return self._get_absolute_url_for('/post/{}'.format(post_id))

    def _get_posts_since(self, start_offset):
        url = self._get_absolute_url_for('/')
        headers = {'Accept': 'application/json'}

        while True:
            params = {'since': start_offset}
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)

            if response.status_code == requests.codes.not_found:
                # If we hit a 404, stop the whole process
                break
            elif response.status_code != requests.codes.ok:
                raise RuntimeError('API response code is not OK')

            try:
                data = response.json()
            except ValueError:
                raise RuntimeError('API response body is not JSON')

            for post in data['posts']:
                yield PostModel(**post)

            if data['has_next']:
                start_offset = data['posts'][-1]['id']
            else:
                break

    def _get_absolute_url_for(self, path):
        scheme, netloc, _, _, _, _ = urlparse(self.site_url)

        new_parts = (scheme, netloc, path, '', '', '')

        return urlunparse(new_parts)


class PostModel(object):
    def __init__(self, **kwargs):
        vars(self).update(kwargs)

    def get_message(self, length=None, suffix='...'):
        if length is None or len(self.message) <= length:
            return self.message

        length -= len(suffix)

        if self.message[length].isspace():
            return self.message[:length] + suffix
        else:
            return self.message[:length].rsplit(' ', 1)[0] + suffix
