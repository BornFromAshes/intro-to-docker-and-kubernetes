import os
import requests
import flask
import json
import redis
import time

API_KEY = os.environ.get('API_KEY')
CACHE_TIME = int(os.environ.get('CACHE_TIME'))
CURRENCY_NAME = os.environ.get('CURRENCY_NAME')
SERVER_PORT = os.environ.get('serverport')


app = flask.Flask(__name__)
redis_connection = redis.StrictRedis(host='172.17.0.3', port=6379)


@app.route('/', methods=['GET'])
def homepage():
    json_dump = json.dumps({"response": "To get the price of your currency use /getprice"})
    return json_dump


@app.route('/getprice/', methods=['GET'])
def get_price():
    redis_response = json.loads(redis_connection.get('btc'))

    if time.time() - redis_response["time"] > CACHE_TIME:
        output = set_redis(str(CURRENCY_NAME))
    else:
        output = redis_response
    return json.dumps(output)


def set_redis(in_crypto):
    url = 'https://rest.coinapi.io/v1/assets/' + in_crypto
    headers = {'X-CoinAPI-Key': API_KEY}
    response = requests.get(url, headers=headers)
    name = response.json()[0]["name"]
    price = response.json()[0]["price_usd"]
    output = {"name": name, "price": price, "time": time.time()}
    redis_connection.set(in_crypto, json.dumps(output))
    return output


if __name__ == "__main__":
    set_redis(CURRENCY_NAME)
    app.run(debug=True, host='0.0.0.0', port=SERVER_PORT)
