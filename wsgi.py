# File: wsgi.py
# Desc: Production. Run with gunicorn
# Date: November 30, 2016 @ 2:41 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from app import app

if __name__ == '__main__':
    app.run()
