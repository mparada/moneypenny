#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Flask, request, jsonify)
from flask_sqlalchemy import SQLAlchemy

import datetime
import os

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
        self.customer = None

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

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    print(request)
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        self.customer = data['name']
        response = "Got Customer"
        return jsonify({ "speech": response, "displayText": response})
    elif request.method == 'GET':
        return jsonify({ "name": "Daniel" })

if __name__ == "__main__":
    app.run(debug=True)
