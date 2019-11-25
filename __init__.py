from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from redditsavesorganiser.App import App
flask_app = Flask("redditsavesorganiser")
app = App(flask_app)

import redditsavesorganiser.routes
