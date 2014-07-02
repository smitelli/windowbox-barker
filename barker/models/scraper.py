import requests
from bs4 import BeautifulSoup


class MetadataScraper(object):
    def __init__(self, timeout=10):
        self.timeout = timeout

        self.response_text = None
        self.soup = None

    def parse(self, url):
        response = self.load(url)

        self.response_text = response.text
        self.soup = BeautifulSoup(self.response_text)

        return self

    def load(self, url):
        self.response_text = None
        self.soup = None

        response = requests.get(url, timeout=self.timeout)

        if response.status_code != requests.codes.ok:
            raise RuntimeError('Server response code is not OK')

        return response

    def get_twitter_image_url(self):
        meta_twitter_image = self.soup.find('meta', {'name': 'twitter:image'})

        if meta_twitter_image is None:
            return None

        return meta_twitter_image['content']
