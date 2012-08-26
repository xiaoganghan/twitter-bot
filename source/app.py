#!/usr/bin/env python

import cgi,urllib
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import logging
from md5 import md5
import simplejson as json
import tweepy
import bitly
import urllib2

from local_settings import TwitterKey, BitlyKey

class TwitterDB(db.Model):
    reddit_id = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)


class TwitterBot(webapp.RequestHandler):
    def get(self):
        consumer_key = TwitterKey['consumer_key']
        consumer_secret = TwitterKey['consumer_secret']
        access_token = TwitterKey['access_token']
        access_token_secret = TwitterKey['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        bot = tweepy.API(auth)

        shortapi = bitly.Api(login=BitlyKey['login'], apikey=BitlyKey['apikey'])

        url = 'http://www.reddit.com/r/programming/.json'
        jsondata = json.loads(urllib2.urlopen(url).read())

        tweets = ''
        if 'data' in jsondata and 'children' in jsondata['data']:
            posts = jsondata['data']['children']
            posts.reverse()
            for ind, post in enumerate(posts):
                entry = post['data']
                logging.debug(entry['permalink'] + ' ' +entry['url'])
                postid = entry['id']
                query = TwitterDB.all()
                num_comments = entry['num_comments']
                query.filter('reddit_id =', postid)
                res = query.fetch(1)

                if len(res) == 0 and num_comments > 5:
                    title = entry['title']
                    score = entry['score']
                    downs = entry['downs']
                    ups = entry['ups']
                    permalink = shortapi.shorten('http://www.reddit.com' + entry['permalink'])
                    url = shortapi.shorten(entry['url'])
                    author = entry['author']
                    status = ' %s [%s by:%s comments:%d score:%d]' % (url, permalink, author, num_comments, score)
                    status = title[:(140 - len(status))] + status
                    status = status.encode('utf-8')
                    logging.debug(status)
                    tweets += '<p>' + status + '</p>'
                    bot.update_status(status)
                    item = TwitterDB()
                    item.reddit_id = postid
                    item.put()

        self.response.out.write("Done!\n" + tweets)
                
                
application = webapp.WSGIApplication([('/bots/twitterbot', TwitterBot)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
	main()
                
        
        
        
          
