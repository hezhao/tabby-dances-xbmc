import os
import sys
import time
import xbmc
import xbmcgui

rootDir = os.path.dirname(os.path.realpath(__file__))
if rootDir[-1] == ';':rootDir = rootDir[0:-1]
libTwitterDir = os.path.join(rootDir, 'python-twitter')
libGrooveDir = os.path.join(rootDir, 'groove-dl')
sys.path.append(libTwitterDir)
sys.path.append(libGrooveDir)

import twitter
import groove


# Your Aapp
consumer_key=<your_apps_consumer_key>
consumer_secret=<your_apps_consumer_secret>

# @user
access_token_key = <your_user_token_key>
access_token_secret = <your_user_token_secret>


def printUnicode(str):
	'''
	Print debug information, by default python 2 is ascii encoded in xbmc 
	'''
	print str.encode('utf-8')


class XBMCPlayer(xbmc.Player):
	def __init__(self):
		self.groovy = True
		self.tag = None
		self.mention_from = None
		self.in_reply_to_status_id = None
		self.artist = ''
		self.title = ''
		self.last_mention_id = 0
	
	def onPlayBackStarted(self):
		'''
		Extend XBMC callback method to post tweet of current playing song 
		'''
		print '[Tabby Dances] onPlayBackStarted'
		
		tweet = None
		try:
			if self.in_reply_to_status_id and self.mention_from:
				# streaming from grooveshark (in response to twitter)
				tweet = '@' + self.mention_from + ' I am dancing to ' + self.title + ' by ' + self.artist + ' right meow! '
				status = api.PostUpdate(tweet, self.in_reply_to_status_id)
			else:
				# play directly wihin XBMC or AirPlay
				pass
		except Exception, e:
			print '[Tabby Exception] ' + str(e)
			return
		printUnicode('[Tabby Dances] ' + tweet)

	def parseTweet(self, tweet):
		'''
		Parse tweet and send query to GrooveShark
		'''
		if not tweet:
			return
		
		# split that tweet into list
		cmd = tweet.text.lower().split()
		
		# pass tweet and only match the following command(s)
		# play song: '@wktabby play <song/musician name>'
		if cmd[1] == 'play':
			query = ' '.join(cmd[2:])
			printUnicode(query)
			self.mention_from = tweet.user.screen_name
			self.in_reply_to_status_id = tweet.id
			self.grooveStream(query)
		
		# save the tweet id so that next time search from new tweet since here 
		self.last_mention_id = tweet.id

	def grooveStream(self, query):
		'''
		Retrive URL, artist, title with query from GrooveShark
		'''
		songUrl, self.artist, self.title = groove.retriveSongUrl(query)
		if songUrl:
			listitem = xbmcgui.ListItem(query)
			listitem.setInfo('music', {'Title': self.title, 'Artist': self.artist})
			self.play(songUrl, listitem)
		else:
			tweet = '@' + self.mention_from + ' Sorry I didn\'t find ' + '"' + query + '"'
			try:
				status = api.PostUpdate(tweet, self.in_reply_to_status_id)
			except Exception, e:
				print '[Tabby Exception] ' + str(e)
				return
			printUnicode('[Tabby Dances] ' + tweet)

	def searchLatestAtMention(self):
		'''
		Search the latest @mention tweets
		'''
		# reset tweet info
		self.mention_from = None
		self.in_reply_to_status_id = None
		
		# only check @mentions when player is idle
		if self.isPlaying():
			return
		
		# get all @mention tweets from last mention
		try:
			tweets = api.GetMentions(since_id = self.last_mention_id)
			print 'last_mention_id = %d' % self.last_mention_id
		except Exception, e:
			print '[Tabby Exception] ' + str(e)
			return
		
		# process tweets if there are any
		if len(tweets) > 0:
			
			# print all @mention tweets from last mention
			for t in tweets:
				printUnicode('[Tabby Dances] ' + str(t.id) + ' :: ' + t.user.screen_name + ' :: ' + t.text)
			
			# find the latest tweet if there are more than one
			tweet = tweets[0]
			return tweet
		
		# no new tweets from last mention
		return None


if __name__ == '__main__':
	
	### 1. Authenticate with Twitter ###
	
	api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
	access_token_key=access_token_key, access_token_secret=access_token_secret)
	credentials = api.VerifyCredentials()
	printUnicode('[Tabby Dances] Ready to post to ' + credentials.name)
	
	### 2. While loop to search and process twitter @mention ###
	
	player = XBMCPlayer()
	
	while(not xbmc.abortRequested):
		
		# find latest tweet
		tweet = player.searchLatestAtMention()
		
		# process the tweet
		player.parseTweet(tweet)
		
		# rate limit is 350 per hour, thats every 11 second (3600s / 350 = 11s)
		# we use 15s just for safe
		xbmc.sleep(15000)
		