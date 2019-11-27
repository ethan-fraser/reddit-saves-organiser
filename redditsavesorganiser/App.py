import praw
from random import randint
import os

class App:

	def __init__(self, flask_app):
		self.flask_app = flask_app
		self.flask_app.config.update(
			CLIENT_ID=os.environ.get('CLIENT_ID'),
			CLIENT_SECRET=os.environ.get('CLIENT_SECRET'),
			REDIRECT_URI=os.environ.get('REDIRECT_URI'),
			REFRESH_TOKEN=os.environ.get('REFRESH_TOKEN'),
			)

		self.client_id=self.flask_app.config['CLIENT_ID']
		self.client_secret=self.flask_app.config['CLIENT_SECRET']
		self.redirect_uri=self.flask_app.config['REDIRECT_URI']
		self.refresh_token=self.flask_app.config['REFRESH_TOKEN']

		self.user=''
		self.state=str(randint(1000, 10000))

		self.saves = []
		self.fullnames = []
		self.subreddits = []
		self.subreddits_full = []

		# if self.refresh_token:
		# 	self.reddit = praw.Reddit(
		# 		client_id=self.client_id,
		# 		client_secret=self.client_secret,
		# 		refresh_token=self.refresh_token,
		# 		user_agent="reddit-saves-organiser"
		# 		)
		# else:	
		# 	self.reddit = praw.Reddit(
		# 		client_id=self.client_id,
		# 		client_secret=self.client_secret,
		# 		redirect_uri=self.redirect_uri,
		# 		user_agent="reddit-saves-organiser"
		# 		)

		self.reddit = praw.Reddit(
			client_id=self.client_id,
			client_secret=self.client_secret,
			redirect_uri=self.redirect_uri,
			user_agent="reddit-saves-organiser"
			)

		self.flask_app.jinja_env.globals.update(
			praw=praw,
			Submission=praw.models.reddit.submission.Submission,
			reddit=self.reddit,
			app=self,
			isinstance=isinstance,
			len=len,
			list=list,
			print=print
			)

	def getauthurl(self):
		return self.reddit.auth.url(['identity', 'history', 'save', 'read'], self.state, 'permanent')

	def authorize(self, code):
		self.refresh_token = self.reddit.auth.authorize(code)
		self.flask_app.config.update(REFRESH_TOKEN = self.refresh_token)
		self.user = self.reddit.user.me()
		self.saves = list(self.user.saved(limit=500))
		self.fullnames = [i.fullname for i in self.saves]
		for i in self.reddit.info(self.fullnames):
			if (dn := i.subreddit.display_name) not in self.subreddits:
				self.subreddits.append(dn)
				self.subreddits_full.append(dn)
			else:
				self.subreddits_full.append(dn)
		self.subreddits.sort(key=lambda x: x.lower())

	def sort_by_subreddit(self, subreddit):
		targetsub = self.reddit.subreddit(subreddit)
		tmp=[]
		for x in range(len(self.saves)):
			if self.subreddits_full[x] == targetsub:
				tmp.append(self.saves[x])
		return tmp

	def search(self, key):
		key = " " + key.lower().strip() + " "
		tmp = []
		for i in self.reddit.info(self.fullnames):
			if isinstance(i, praw.models.reddit.submission.Submission):
				if key in i.title.lower() or key in i.selftext.lower():
					tmp.append(i)
			else:
				if key in i.body.lower():
					tmp.append(i)
		return tmp
		