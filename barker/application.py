from __future__ import absolute_import
import ConfigParser
import tweepy
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
    scraper = MetadataScraper(timeout=windowbox.timeout)

    consumer_key = config.get('twitter', 'consumer_key')
    consumer_secret = config.get('twitter', 'consumer_secret')
    access_token = config.get('twitter', 'access_token')
    access_token_secret = config.get('twitter', 'access_token_secret')
    message_length_max = config.getint('twitter', 'message_length_max')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter = tweepy.API(auth)

    # TODO find t.co URL length

    for p in windowbox.walk_new_posts():
        message = p.get_message(message_length_max)
        page_url = windowbox.get_post_url_for(p.id)
        tweet_text = u'{} {}'.format(message, page_url)

        # Windowbox has a pretty gross thundering herd bug when building new
        # image derivatives. Since Twitter is about to wail on this page, make
        # a speculative hit on the image derivative to make sure it's built
        # before we tweet it, allowing the site to handle the traffic better.
        page = scraper.parse(page_url)
        image_url = page.get_twitter_image_url()
        scraper.load(image_url)

        #status = twitter.update_status(status=tweet_text)
        print tweet_text
