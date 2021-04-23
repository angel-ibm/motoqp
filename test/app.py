#!/usr/bin/env python3
# This is the main program that can be executed 
# from the command line ./app.py at any time
# no use of connexion here

from flask import Flask
app = Flask(__name__)

from routes import *   # pylint: disable=unused-wildcard-import

if __name__ == '__main__':
	app.run(host='0.0.0.0')
	# app.run(debug=True, host='0.0.0.0', port=5555,  static_url_path='/static')
