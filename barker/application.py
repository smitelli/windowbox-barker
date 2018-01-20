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
    post_count_limit = config.getint('windowbox', 'post_count_limit')
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
    url_padding = None

    print 'Starting windowbox-barker...'

    for p in windowbox.walk_new_posts(limit=post_count_limit):
        # Only read Twitter's 'short_url_length' param once, to prevent rate-
        # limiting issues. Don't read it at all if there are no posts.
        if url_padding is None:
            # The current length of a t.co URL PLUS one space preceding it
            url_padding = twitter.configuration()['short_url_length'] + 1

        message = p.get_message(message_length_max - url_padding)
        page_url = windowbox.get_post_url_for(p.id)
        tweet_text = u'{} {}'.format(message, page_url)

        # Windowbox has a pretty gross thundering herd bug when building new
        # image derivatives. Since Twitter is about to wail on this page, make
        # a speculative hit on the image derivative to make sure it's built
        # before we tweet it, allowing the site to handle the traffic better.
        page = scraper.parse(page_url)
        image_url = page.get_twitter_image_url()
        scraper.load(image_url)

        print u'Sending [{}]...'.format(tweet_text)

        status = twitter.update_status(status=tweet_text)
        if not status.created_at:
            raise Exception('Tweet was not created!')

        print 'Created.'
    print 'Done.'
