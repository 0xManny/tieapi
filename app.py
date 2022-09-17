from flask import Flask, jsonify
import requests

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def home():
    return {
        'msg': 'API is working fine'
    }


if __name__ == "__main__":
    #app.debug = True
    app.run(host="0.0.0.0",port= 5000)