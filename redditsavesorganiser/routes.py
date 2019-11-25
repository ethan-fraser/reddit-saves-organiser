from . import app, reddit
from .authorize import getauthurl, authorize
from flask import Flask, request, render_template, redirect, url_for
import praw

@app.route('/')
def index():
	if not reddit.user.me():
		authurl = getauthurl()
		app.jinja_env.globals.update(authurl=authurl)
	return render_template("index.html")


@app.route('/authorize_callback', methods=['GET', 'POST'])
def authorize_callback():
	if code := request.args.get('code'):
		authorize(code)
	return render_template("authorize_callback.html")