#!/usr/bin/env python
from md5 import md5
import simplejson as json
import tweepy
import feedparser
import bitly
from BeautifulSoup import BeautifulSoup

def test():
	consumer_key = "Y58SeSAKiseoXalPqbYhIQ"
	consumer_secret = "q51SOmJhT8eVRORKtx6AiqJ1YfsDnRAqbmWmtdjklo"
	access_token = "178269422-SNexeTB56lZ9wQ3VXL1nRJg0WeYdWoHUfqlEwjO2"
	access_token_secret = "WrGaBCHtGbZLttIQKVmrqhTp9wOYM9KSs6HSOHLf3k"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	bot = tweepy.API(auth)
	shortapi = bitly.Api(login='chrishan', apikey='R_39fbf3e0a40688bfe792dd90bd41b4e8')
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
			#print entry
			try:
				for link in links:
					if link['href'].find('/user/') < 0:
						#urllink = str(unicode(link['href']).encode("utf-8"))
						status += ' ' + shortapi.shorten(link['href'])
					if link.string.find('comments') > 0:
						status += ' ' + link.string
						num_comments = int(link.string[1:-1].split()[0])
				
				try:
					status = title[:(140 - len(status))] + status
				except:
					status = repr(title[:(140 - len(status))]) + status
				
				print status
				print num_comments
			except:
				pass
if __name__ == "__main__":
	test()
                
        
        
        
          
