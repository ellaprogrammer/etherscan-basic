import os
import logging
import traceback

import flask
from replit import db

import urllib.request, json


EMOJI = ['💯', '❤️', '🥳', '💩']
# my_secret = os.environ['api_key']

app = flask.Flask(__name__)

@app.errorhandler(500)
def internal_server_error(e: str):
  return flask.jsonify(error=str(e)), 500

# how to route to diff endpoint?
@app.route('/db', methods=['GET, POST'])
def info():
  for key in db.keys():
    print(key)

@app.route('/', methods=['GET', 'POST'])
def comments():
  try:
    # counts = db.get('emoji', {})
    output_addresses = ['']
    if flask.request.method == "POST" and 'transaction' in flask.request.form:
      transaction_hash = [flask.request.form['transaction']]
      url = "https://api.etherscan.io/api?module=account&action=txlist&address=0x25ed58c027921e14d86380ea2646e3a1b5c55a8b&startblock=0&endblock=99999999&sort=asc&apikey={}".format(os.environ.get('ETHERSCAN_API_KEY'))
      response = urllib.request.urlopen(url)
      data = response.read()
      dict = json.loads(data)
      json_formatted_str = json.dumps(dict, indent=2)
      print(json_formatted_str.blockNumber['13547831'])
      
      transaction_matches = ['address_requested_found1,address_requested_found2']
      # output_addresses = output of API call
      output_addresses = transaction_matches

      # join input list to store in DB as key string
      joined_string = ",".join(transaction_hash)
      # let's prevent against scammers clogging out DB
      if len(joined_string) > 70:
        joined_string = joined_string[:70] + '_ABBREV'  
      db[joined_string] = output_addresses
    
      
      # if flask.request.method == "POST" and 'emoji' in flask.request.form:
    #   emoji = flask.request.form['emoji']
    #   if emoji in EMOJI:
    #     try:
    #       counts[emoji] += 1
    #     except KeyError:
    #       counts[emoji] = 1
    #     db['emoji'] = counts
    # sorted_counts = sorted(counts.items(), key=lambda el: el[1], reverse=True)

      
    return flask.render_template(
      'emoji.html', addresses=output_addresses)
  except Exception as e:
    logging.exception('failed to database')
    flask.abort(500, description=str(e) + ': ' + traceback.format_exc())

app.run('0.0.0.0')
