from cryptocompare.cryptocompare import LIMIT
from flask import Flask, json
import cryptocompare
import datetime
from flask import jsonify
from werkzeug.wrappers import response
app = Flask(__name__)

# Set API key
cryptocompare.cryptocompare._set_api_key_parameter(
    'ed1876548dc9a2cde4ee926c1d496c1b4fd35c640de94b3cc16d7e409830342f')

# API endpoint to return data for BTC and ETH in a given datetime range
@app.route("/data/<date_from>/<date_to>")
def get_data(date_from, date_to):
    date_from = int(date_from)
    date_to = int(date_to)
    # Maximum number of entries returned by cryptocompare.cryptocompare in a single call
    LIMIT = 1400
    if(date_to - date_from < 60*LIMIT):
        response =  jsonify({
            'btc': cryptocompare.get_historical_price_minute('BTC', 'USD', limit=int((date_to - date_from)/60), toTs=date_to),
            'eth': cryptocompare.get_historical_price_minute('ETH', 'USD', limit=int((date_to - date_from)/60), toTs=date_to)
            })
    elif(date_to - date_from < 3600*LIMIT):
        response = jsonify({
            'btc': cryptocompare.get_historical_price_hour('BTC', 'USD', limit=int((date_to - date_from)/3600), toTs=date_to),
            'eth': cryptocompare.get_historical_price_hour('ETH', 'USD', limit=int((date_to - date_from)/3600), toTs=date_to)
            })
    elif(date_to - date_from < 86400*LIMIT):
        response = jsonify({
            'btc': cryptocompare.get_historical_price_day('BTC', 'USD', limit=int((date_to - date_from)/86400), toTs=date_to),
            'eth': cryptocompare.get_historical_price_day('ETH', 'USD', limit=int((date_to - date_from)/86400), toTs=date_to)
            })
    else:
        response = 'Date range out of limit'
    # Allow cross origin requests
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
