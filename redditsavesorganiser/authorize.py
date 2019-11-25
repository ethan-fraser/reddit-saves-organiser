from . import app, reddit, saves
from random import randint

def getauthurl():
	state = str(randint(1000, 10000))
	return reddit.auth.url(['identity', 'history', 'save', 'read'], state, 'permanent')

def authorize(code):
	refresh_token = reddit.auth.authorize(code)
	saves = reddit.user.me().saved(limit=500)
	app.config.update(REFRESH_TOKEN = refresh_token)