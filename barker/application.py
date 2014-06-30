from __future__ import absolute_import
import ConfigParser
from barker import AppPath
from barker.models.windowbox import WindowboxAPI

def run():
    config = ConfigParser.SafeConfigParser()
    config.read(AppPath.base('config.ini'))

    windowbox_kwargs = {
        'site_url': config.get('windowbox', 'site_url'),
        'state_file': config.get('windowbox', 'state_file')}
    windowbox = WindowboxAPI(**windowbox_kwargs)

    twitter_kwargs = {
        'consumer_key': config.get('twitter', 'consumer_key'),
        'consumer_secret': config.get('twitter', 'consumer_secret'),
        'access_token': config.get('twitter', 'access_token'),
        'access_token_secret': config.get('twitter', 'access_token_secret')}
    #twitter = TwitterAPI(**twitter_kwargs)
