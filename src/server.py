#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Flask, request, jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)


customer_name = "Daniel"

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
        login = None
        for context in data['result']['contexts']:
            if context['name'] == 'login':
                login = context
                break

        if not login:
            return jsonify({ "speech": "Invalid Session"})

        amount = login['parameters']['money']['amount']
        currency = login['parameters']['money']['currency']
        recipient = login['parameters']['recipient']
        sender = login['parameters']['Name']
        response = "Okay, sending {} {} from {} to {}".format(amount, currency,
                sender, recipient)
        return jsonify({ "speech": response, "displayText": response})


@app.route('/')
def hello_world():
    return 'Hello, World!'


def get_login(request):
    data = request.get_json()
    login = None
    for context in data['result']['contexts']:
        if context['name'] == 'login':
            login = context
            break
    return login


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    global customer_name
    if request.method == 'POST':
        login = get_login(request)
        customer_name = login['parameters']['Name']
        response = "Got Customer"
        return jsonify({"speech": response, "displayText": response})
    elif request.method == 'GET':
        return jsonify({"name": customer_name})
        #return app.send_static_file('Persona_Daniel.html')


if __name__ == "__main__":
    app.run(debug=True)
