#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Flask, request, jsonify)
from flask_sqlalchemy import SQLAlchemy
from OpenSSL import SSL

import datetime
import os

context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__), 'moneypenny.crt')
key = os.path.join(os.path.dirname(__file__), 'moneypenny.key')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100))
    receipient = db.Column(db.String(100))
    reference = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(10))
    date = db.Column(db.DateTime())

    def __init__(self, sender, receipient, reference, amount, currency):
        self.sender = sender
        self.receipient = receipient
        self.reference = reference
        self.amount = amount
        self.currency = currency
        self.date = datetime.datetime()

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        response = "Got Data"
        return jsonify({ "speech": response, "displayText": response})

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    context = (cer, key)
    app.run(host='0.0.0.0', debug=True, ssl_context=context)
