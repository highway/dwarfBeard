#
# This file is part of dwarfBeard.
#
# dwarfBeard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dwarfBeard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See <http://www.gnu.org/licenses/> for license information.

import dwarfBeard

from dwarfBeard import common

# parse_qsl moved to urlparse module in v2.6
try:
    from urlparse import parse_qsl #@UnusedImport
except:
    from cgi import parse_qsl #@Reimport

import lib.oauth2 as oauth
import lib.pythontwitter as twitter

class TwitterNotifier:

    consumer_key = "bvx5tIQTqOlkpU3NQ5LJqwCV6"
    consumer_secret = "vnDm06dCsJXiHOMJIioMtjpCPM5xlXBCRfaOB0lMoTvx85v8Ko"
    
    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
    AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
    SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'
    
    def notify_snatch(self, ep_name):
        if dwarfBeard.TWITTER_NOTIFY_ON_LEVELUP:
            self._notifyTwitter(common.notifyStrings[common.NOTIFY_LEVELUP]+': '+ep_name)

    def notify_download(self, ep_name):
        if dwarfBeard.TWITTER_NOTIFY_ON_RARETASK:
            self._notifyTwitter(common.notifyStrings[common.NOTIFY_RARETASK]+': '+ep_name)

    def test_notify(self):
        return self._notifyTwitter("This is a test notification from dwarfBeard", force=True)

    def _get_authorization(self):
    
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1() #@UnusedVariable
        oauth_consumer             = oauth.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        oauth_client               = oauth.Client(oauth_consumer)
    
        print 'Requesting temp token from Twitter'
    
        resp, content = oauth_client.request(self.REQUEST_TOKEN_URL, 'GET')
    
        if resp['status'] != '200':
            print 'Invalid respond from Twitter requesting temp token:', resp['status']
        else:
            request_token = dict(parse_qsl(content))
    
            dwarfBeard.TWITTER_USERNAME = request_token['oauth_token']
            dwarfBeard.TWITTER_PASSWORD = request_token['oauth_token_secret']
    
            return self.AUTHORIZATION_URL+"?oauth_token="+ request_token['oauth_token']
    
    def _get_credentials(self, key):
        request_token = {}
    
        request_token['oauth_token'] = dwarfBeard.TWITTER_USERNAME
        request_token['oauth_token_secret'] = dwarfBeard.TWITTER_PASSWORD
        request_token['oauth_callback_confirmed'] = 'true'
    
        token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        token.set_verifier(key)
    
        print 'Generating and signing request for an access token using key ', key
    
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1() #@UnusedVariable
        oauth_consumer             = oauth.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        print 'oauth_consumer: ', str(oauth_consumer)
        oauth_client  = oauth.Client(oauth_consumer, token)
        print 'oauth_client:', str(oauth_client)
        resp, content = oauth_client.request(self.ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % key)
        print 'resp, content:', str(resp)+ ',' + str(content)
    
        access_token  = dict(parse_qsl(content))
        print 'access_token: ', str(access_token)
    
        print 'resp[status] = ', str(resp['status'])
        if resp['status'] != '200':
            print 'The request for a token with did not succeed: ', str(resp['status']), logger.ERROR
            return False
        else:
            print 'Your Twitter Access Token key:',  access_token['oauth_token']
            print 'Access Token secret:', access_token['oauth_token_secret']
            dwarfBeard.TWITTER_USERNAME = access_token['oauth_token']
            dwarfBeard.TWITTER_PASSWORD = access_token['oauth_token_secret']
            return True
    
    
    def _send_tweet(self, message=None):
    
        username=self.consumer_key
        password=self.consumer_secret
        access_token_key=dwarfBeard.TWITTER_USERNAME
        access_token_secret=dwarfBeard.TWITTER_PASSWORD
    
        print u"Sending tweet: ", message
    
        api = twitter.Api(username, password, access_token_key, access_token_secret)
    
        try:
            api.PostUpdate(message)
        except Exception, e:
            print u"Error Sending Tweet"
            return False
    
        return True
    
    def _notifyTwitter(self, message='', force=False):
        prefix = dwarfBeard.TWITTER_PREFIX
    
        if not dwarfBeard.USE_TWITTER and not force:
            return False
    
        return self._send_tweet(prefix+": "+message)

notifier = TwitterNotifier