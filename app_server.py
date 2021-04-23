#!/usr/bin/env python3
# This is the main program that can be executed 
# from the command line ./app_server.py at any time

from flask import Flask
import connexion
import serverqp

app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('swagger.yaml' )

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
	# app.run(debug=True, host='0.0.0.0', port=5555)
