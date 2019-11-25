from flask import Flask
import praw

from dotenv import load_dotenv
load_dotenv()

app = Flask("redditsavesorganiser")
app.config.from_pyfile("config.py")

if app.config['REFRESH_TOKEN']:
	reddit = praw.Reddit(
		client_id=app.config['CLIENT_ID'],
		client_secret=app.config['CLIENT_SECRET'],
		refresh_token=app.config['REFRESH_TOKEN'],
		user_agent="organiserbot"
		)
else:	
	reddit = praw.Reddit(
		client_id=app.config['CLIENT_ID'],
		client_secret=app.config['CLIENT_SECRET'],
		redirect_uri=app.config['REDIRECT_URI'],
		user_agent="organiserbot"
		)

saves = []

app.jinja_env.globals.update(
	praw=praw,
	Submission=praw.models.reddit.submission.Submission,
	reddit=reddit,
	isinstance=isinstance,
	len=len,
	print=print
	)

import redditsavesorganiser.routes