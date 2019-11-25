from . import app, reddit
from .authorize import getauthurl, authorize
from .sorting import *
from flask import Flask, request, render_template, redirect, url_for
import praw

@app.route('/')
def index():
	if not reddit.user.me():
		authurl = getauthurl()
		app.jinja_env.globals.update(authurl=authurl)
	app.jinja_env.globals.update(sort_by_subreddit=sort_by_subreddit)
	return render_template("index.html")


@app.route('/authorize_callback', methods=['GET', 'POST'])
def authorize_callback():
	if code := request.args.get('code'):
		authorize(code)
	return render_template("authorize_callback.html")