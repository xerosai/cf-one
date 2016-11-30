# File: debug.py
# Desc: debug script
# Date: November 30, 2016 @ 2:32 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7200, debug=True)
