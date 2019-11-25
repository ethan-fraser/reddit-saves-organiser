import praw
from random import randint

class App:

	def __init__(self, flask_app):
		self.flask_app = flask_app
		self.flask_app.config.from_pyfile("config.py")

		self.client_id=self.flask_app.config['CLIENT_ID']
		self.client_secret=self.flask_app.config['CLIENT_SECRET']
		self.redirect_uri=self.flask_app.config['REDIRECT_URI']
		self.refresh_token=self.flask_app.config['REFRESH_TOKEN']

		self.user=''
		self.state=str(randint(1000, 10000))

		self.saves = []
		self.fullnames = []
		self.subreddits = []

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
		self.subreddits = [i.subreddit for i in self.reddit.info(self.fullnames)]

	def sort_by_subreddit(self, subreddit):
		targetsubid = self.reddit.subreddit(subreddit)
		return [self.saves[x] for x in range(len(self.saves)) if self.subreddits[x] == targetsubid]