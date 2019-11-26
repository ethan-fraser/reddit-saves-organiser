from . import app
from flask import request, render_template, url_for
import praw

@app.flask_app.route('/')
def index():
	if not app.reddit.user.me():
		authurl = app.getauthurl()
		app.flask_app.jinja_env.globals.update(authurl=authurl)
	print("returning index.html")
	return render_template("index.html")


@app.flask_app.route('/authorize_callback', methods=['GET', 'POST'])
def authorize_callback():
	if code := request.args.get('code'):
		app.authorize(code)
	return render_template("authorize_callback.html")