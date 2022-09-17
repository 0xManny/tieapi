from flask import Flask, jsonify
from flask_apscheduler import APScheduler
import requests


app = Flask(__name__)
app.url_map.strict_slashes = False
scheduler = APScheduler()

var = 0

@app.route("/")
def home():
    return {
        'msg': 'API is working fine',
        'var': var
    }

def setVar():
    var += 1

def getVar():
    return var


if __name__ == "__main__":
    #app.debug = True
    scheduler.add_job(id = 'Scheduled Task', func=setVar, trigger="interval", seconds=10)
    scheduler.start()
    app.run(host="0.0.0.0",port= 5000)