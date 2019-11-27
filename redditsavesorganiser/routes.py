from . import app
from flask import request, render_template, url_for, redirect
import praw

@app.flask_app.route('/')
def index():
	if app.reddit.user.me():
		display_list = []

		if request.args.get('subreddit') or request.args.get('search'):
			if request.args.get('subreddit') and request.args.get('search'):
				sub_tmp = app.sort_by_subreddit(request.args.get('subreddit'))
				search_tmp = app.search(request.args.get('search'))
				if len(search_tmp) >= len(sub_tmp):
					display_list = [i for i in search_tmp if i in sub_tmp]
				else:
					display_list = [i for i in sub_tmp if i in search_tmp]
			elif request.args.get('subreddit'):
				display_list = app.sort_by_subreddit(request.args.get('subreddit'))
			elif request.args.get('search'):
				display_list = app.search(request.args.get('search'))
		else:
			display_list = app.saves
		app.flask_app.jinja_env.globals.update(display_list=display_list)
		return render_template("index.html")
	else:
		authurl = app.getauthurl()
		app.flask_app.jinja_env.globals.update(authurl=authurl)
		return render_template("please_authorize.html")


@app.flask_app.route('/authorize_callback', methods=['GET', 'POST'])
def authorize_callback():
	if code := request.args.get('code'):
		app.authorize(code)
	return render_template("authorize_callback.html")
