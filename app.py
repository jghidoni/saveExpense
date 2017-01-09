#!/usr/bin/env python

#REQUIREMENTS: psycopg2==2.6.1 Flask-SQLAlchemy===2.1

import urllib
import json
import os
import psycopg2
import urlparse

from flask import Flask
from flask import request
from flask import make_response
from flask.ext.sqlalchemy import SQLAlchemy

# Flask app should start in global layout
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
from models import *

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "save.expense":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    expense = parameters.get("expense-type")
    service = parameters.get("service-bought")
    amount = parameters.get("unit-currency")
    date = parameters.get("date")

    db.session.add(ExpenseRecord(expense,service))
    db.session.commit()
    #salvare i parametri

    speech = "Spesa salvata con successo."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
