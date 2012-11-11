# -*- coding: utf-8 -*-

import os, json, requests
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort, jsonify

# import all of mongoengine
# from mongoengine import *
from flask.ext.mongoengine import mongoengine

# import data models
#import models

app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = False

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
mongoengine.connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")


categories = ['web','physical computing','software','video','music','installation','assistive technology','developing nations','business','social networks']

# --------- Routes ----------

# this is our main page
@app.route("/", methods=['GET','POST'])
def index():

	# user inputs name to simple form

	return render_template("index.html")


@app.route("/check", methods=['POST'])
def check():

	
	name_str = request.form.get('name-input')
	vendors = []
	response = "no"

	templateData = {
		'name' : name_str,
		'response' : 'no'
	}

	url = "http://itpmailcall.herokuapp.com/data/mailpieces/onshelf"
	data_request = requests.get(url)
	data = data_request.json
	items = data["ideas"]

	for i in items:
		if i['to'] == name_str:
			vendors.append(i['from'])
			response = "yes"
			
	templateData = {
		'name' : name_str,
		'vendors' : vendors,
		'response' : response
	}		
	
	return render_template("/return.html", **templateData)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# slugify the title 
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	