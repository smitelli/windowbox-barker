from __future__ import absolute_import
import ConfigParser
from barker import AppPath
from barker.models.scraper import MetadataScraper
from barker.models.windowbox import WindowboxAPI

def run():
    config = ConfigParser.SafeConfigParser()
    config.read(AppPath.base('config.ini'))

    windowbox_kwargs = {
        'site_url': config.get('windowbox', 'site_url'),
        'state_file': config.get('windowbox', 'state_file'),
        'timeout': config.getint('windowbox', 'timeout')}
    windowbox = WindowboxAPI(**windowbox_kwargs)

    twitter_kwargs = {
        'consumer_key': config.get('twitter', 'consumer_key'),
        'consumer_secret': config.get('twitter', 'consumer_secret'),
        'access_token': config.get('twitter', 'access_token'),
        'access_token_secret': config.get('twitter', 'access_token_secret'),
        'message_length_max': config.getint('twitter', 'message_length_max')}
    #twitter = TwitterAPI(**twitter_kwargs)


    scraper = MetadataScraper(timeout=windowbox_kwargs['timeout'])
    for p in windowbox.walk_new_posts():
        page_url = windowbox.get_post_url_for(p.id)

        # Fix race
        page = scraper.parse(page_url)
        image_url = page.get_twitter_image_url()
        scraper.load(image_url)

        print p.get_message(20), page_url
