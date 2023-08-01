import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

import data

binance_api = "EtULk58JlMoLSuIMsMCDoz1aehGMpfBItU3Fvu5cj7Rm62KCkHDCidJsheVnGhYg"
binance_secret = "NgJTBZBDcJH49ELK8LBV4NlafPSKQvTW3ZFKGeOvqMZrj61dePXgExMVH0KhOw1y"

app = Flask(__name__)
CORS(app)
deals = []

users = {
    "andrey": "842b734469573c88cdbc5eb4f027e718",
    "alexey_msnet": "f4e2708b9951d627ad51b7c6454b52dd"
}


@app.route("/get")
def readAll():
    s = request.args.get("symbol")
    if s is not None:
        return data.dict_.get(s + "USDT")
    return data.dict_


@app.route("/getPrice")
def getPrice():
    key = f"https://api.binance.com/api/v3/ticker/"
    data = requests.get(key).json()
    return data


@app.route("/placeOrder", methods=['POST'])
def placeOrder():
    json = request.get_json()
    sym = json.get("symbol")
    quantity = json.get("quantity")
    side = json.get("side")
    if sym and quantity and side:
        deals.append({
            "symbol": sym,
            "quantity": quantity,
            "side": side
        })
    return deals[-1]


@app.route("/deals")
def deals_func():
    return jsonify(data.deals)


@app.route("/dealsSend")
def send():
    json = request.get_json()
    data.deals = json
    return "ok"


@app.route("/dictSend")
def dictSend():
    json = request.get_json()
    data.dict_ = json
    return "ok"


@app.route("/dealsRemove/<index>")
def deals_func_rem(index: int):
    return "no"


@app.route("/login", methods=["POST"])
def login():
    json = request.get_json()
    if json.get("login") in users:
        if json.get("password") == users.get(json.get("login")):
            return {"status": "ok"}
    return {"status": "access denied"}


if __name__ == '__main__':
    app.run(host="0.0.0.0")
