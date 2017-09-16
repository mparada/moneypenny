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
    recipient = db.Column(db.String(100))
    reference = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(10))
    date = db.Column(db.DateTime())

    def __init__(self, sender, recipient, reference, amount, currency):
        self.sender = sender
        self.recipient = recipient
        self.reference = reference
        self.amount = amount
        self.currency = currency
        self.date = datetime.datetime.now()

    def as_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "reference": self.reference,
            "amount": self.amount,
            "currency": self.currency,
            "date": self.date.strftime('%d.%m.%Y')}


@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'GET':
        transactions = Transaction.query.all()
        return jsonify([t.as_dict() for t in transactions])

    if request.method == 'POST':
        data = request.get_json()
        login = None
        for context in data['result']['contexts']:
            if context['name'] == 'login':
                login = context
                break

        if not login:
            return jsonify({"speech": "Invalid Session"})

        params = login['parameters']
        amount = params['money']['amount']
        currency = params['money']['currency']
        recipient = params['recipient']
        sender = params['Name']

        transaction = Transaction(sender, recipient, "Money Penny Transfer",
                                  amount, currency)

        db.session.add(transaction)
        db.session.commit()

        response = "Okay, sending {} {} from {} to {}".format(amount, currency,
                                                              sender, recipient)
        return jsonify({"speech": response, "displayText": response})


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
