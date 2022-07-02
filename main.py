import os
import logging
import traceback

import flask
from replit import db

EMOJI = ['💯', '❤️', '🥳', '💩']
my_secret = os.environ['api_key']

app = flask.Flask(__name__)

@app.errorhandler(500)
def internal_server_error(e: str):
    return flask.jsonify(error=str(e)), 500


@app.route('/', methods=['GET', 'POST'])
def comments():
	try:
		counts = db.get('emoji', {})
		if flask.request.method == "POST" and 'emoji' in flask.request.form:
			emoji = flask.request.form['emoji']
			if emoji in EMOJI:
				try:
					counts[emoji] += 1
				except KeyError:
					counts[emoji] = 1
				db['emoji'] = counts
		sorted_counts = sorted(counts.items(), key=lambda el: el[1], reverse=True)
		return flask.render_template(
			'emoji.html', emoji=EMOJI, counts=sorted_counts)
	except Exception as e:
		logging.exception('failed to database')
		flask.abort(500, description=str(e) + ': ' + traceback.format_exc())


app.run('0.0.0.0')
