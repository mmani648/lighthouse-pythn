from flask import Flask,request,jsonify
import os
import string
from waitress import serve
import random
from bs4 import BeautifulSoup as bs
import json
app = Flask(__name__)
def StartTest(url,mode,filename):
    command=f'lighthouse {url} --preset={mode} --output json --output-path {filename}.json --chrome-flags="--headless" --chrome-flags="--ignore-certificate-errors"'
    wait=os.popen(command)
    wait.read()
@app.route('/')
def home():
    website =request.args.get("website")
    mode   = request.args.get("mode")
    filename=''.join(random.choices(string.ascii_uppercase +string.digits, k=16))
    StartTest(website,mode,filename)
    data= open(f"{filename}.json","r",encoding="utf-8").read()
    data =json.loads(data)
    SpeedIndex=data["audits"]["speed-index"]["numericValue"]
    NetworkRequestTime =data["audits"]["server-response-time"]["numericValue"]
    return jsonify({
        "SpeedIndex":SpeedIndex,
        "NetworkRequestTime":NetworkRequestTime,
    })

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)