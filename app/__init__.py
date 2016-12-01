# File: __init__.py
# Desc: Entry-point
# Date: November 30, 2016 @ 2:31 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_pyfile('app_config.py')

CORS(app=app)

db = MongoEngine(app=app)
if db:
    print('db up')

from .api import *
