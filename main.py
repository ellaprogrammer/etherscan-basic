import os
import logging
import traceback

import flask
from replit import db

import urllib.request, json

app = flask.Flask(__name__)

@app.errorhandler(500)
def internal_server_error(e: str):
  return flask.jsonify(error=str(e)), 500

# FIXME: lets set up a DB endpoint
@app.route('/db', methods=['GET, POST'])
def info():
  for key in db.keys():
    print(key)

@app.route('/', methods=['GET', 'POST'])
def comments():
  try:
    output_addresses = ['']
    if flask.request.method == "POST" and 'transaction' in flask.request.form:
      transaction_hash = [flask.request.form['transaction']]
      url = "https://api.etherscan.io/api?module=account&action=txlist&address=" + transaction_hash[0] + "&startblock=0&endblock=99999999&sort=asc&apikey=" + os.environ['ETHERSCAN_API_KEY']
      response = urllib.request.urlopen(url)
      data = response.read()
      dict = json.loads(data)
      count = 0
      for x, y in dict.items():
        if x == "result":
          # print(y[0])
          for z in y:
            if z["from"] == flask.request.form['wallet_address']:
              count += 1
      print(count)
      # json_formatted_str = json.dumps(dict, indent=2)
      # print(json_formatted_str[13000:18000])
      
      # transaction_matches = json_formatted_str[13000:18000]
      transaction_matches = [count]
      # output_addresses = output of API call
      output_addresses = transaction_matches

      # join input list to store in DB as key string
      joined_string = ",".join(transaction_hash)
      # let's prevent against scammers clogging out DB
      if len(joined_string) > 70:
        joined_string = joined_string[:70] + '_ABBREV'  
      db[joined_string] = output_addresses

      
    return flask.render_template(
      'emoji.html', addresses=output_addresses)
  except Exception as e:
    logging.exception('failed to database')
    flask.abort(500, description=str(e) + ': ' + traceback.format_exc())

app.run('0.0.0.0')
