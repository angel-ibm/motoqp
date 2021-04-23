#!/usr/bin/env python3
# These are the urls described in Flask jargon

from app import app
from myexec import myexec

@app.route('/simple_test')
def simple_test_sh():
	return myexec("./simple_test.sh")

@app.route('/')
def welcome():
	return "Welcome to Moto QP"
