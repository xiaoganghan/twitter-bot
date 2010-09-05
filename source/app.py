#!/usr/bin/env python

# --------- Imports --------
import cgi,urllib
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from md5 import md5
import simplejson as json
import tweepy
import feedparser
import bitly
from BeautifulSoup import BeautifulSoup

# ------- Database Handling -----
class TwitterDB(db.Model):
    reddit_id = db.StringProperty()

# ---- The Job Handler --------
class TwitterBot(webapp.RequestHandler):
	def get(self):
		consumer_key = ""
		consumer_secret = ""
		access_token = ""
		access_token_secret = ""
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		bot = tweepy.API(auth)
		shortapi = bitly.Api(login='', apikey='')
		feed = 'http://www.reddit.com/r/programming/.rss'
		atomxml = feedparser.parse(feed)
		entries = atomxml['entries']
		tweets = ''
		
		if len(entries) != 0:
			entries.reverse()
			for x in range(len(entries)):
				entry = entries[x]
				title = str(unicode(entry['title']).encode("utf-8"))
				link = str(unicode(entry['link']).encode("utf-8"))
				myid = str(unicode(entry['id']).encode("utf-8"))
				summary = str(unicode(entry['summary']).encode("utf-8"))
				num_comments = 0
				status = ''
				soup = BeautifulSoup(summary)
				links = soup.findAll('a')
				for link in links:
					if link['href'].find('/user/') < 0:
						status += ' ' + shortapi.shorten(link['href'])
					if link.string.find('comments') > 0:
						status += ' ' + link.string
 						num_comments = int(link.string[1:-1].split()[0])
				
				try:
					status = title[:(140 - len(status))] + status
				except:
					status = repr(title[:(140 - len(status))]) + status
                
				query = TwitterDB.all()
				query.filter('reddit_id =', myid)
				res = query.fetch(1)
                
				if len(res) == 0 and num_comments > 5:
					tweets += '<p>' + status + '</p>'
					bot.update_status(status)
					item = TwitterDB()
					item.reddit_id = myid
					item.put()
				else:
					continue
		self.response.out.write("Done!\n" + tweets)
                
                
application = webapp.WSGIApplication([('/bots/twitterbot', TwitterBot)],
                                     debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
                
        
        
        
          
