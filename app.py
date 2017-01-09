#!/usr/bin/env python

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

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")


#DATABASE_URL = 'postgres://ihpmyqskfsfglq:f04a5064a0018a3489efa7a39000dd936cc935cc46bd08af90b8e3d6bc01edec@ec2-54-228-212-74.eu-west-1.compute.amazonaws.com:5432/deefr25eh78pk'

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ[DATABASE_URL]
#db = SQLAlchemy(app)
#db.create_all()

#from models import *

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

    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, 'abc'))

    #db.session.add(ExpenseRecord(expense,service))
    #db.session.commit()
    #salvare i parametri

    speech = "Spesa salvata con successo."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech
    }

conn.commit()
cur.close()
conn.close()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
