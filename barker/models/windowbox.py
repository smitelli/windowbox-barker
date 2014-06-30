from __future__ import absolute_import
import shelve
import requests
from urlparse import urlparse, urlunparse


class WindowboxAPI(object):
    def __init__(self, site_url, state_file):
        self.site_url = site_url
        self.state_file = state_file

        self._shelf = shelve.open(filename=self.state_file)

    def walk_new_posts(self):
        start_offset = self._shelf.get('start_offset', 0)

        for post in self._get_posts_since(start_offset):
            yield post

            self._shelf['start_offset'] = post.id
            self._shelf.sync()

    def _get_posts_since(self, start_offset):
        url = self._get_absolute_url_for('/')
        headers = {'Accept': 'application/json'}

        while True:
            response = requests.get(
                url, params={'since': start_offset}, headers=headers, timeout=10)

            if response.status_code is not requests.codes.ok:
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
