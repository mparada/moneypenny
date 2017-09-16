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
    recipient = db.Column(db.String(100))
    reference = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(10))
    date = db.Column(db.DateTime())

    def __init__(self, sender, recipient, reference, amount, currency, date=None):
        self.sender = sender
        self.recipient = recipient
        self.reference = reference
        self.amount = amount
        self.currency = currency
        self.date = date if date else datetime.datetime.now()

    def as_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "reference": self.reference,
            "amount": self.amount,
            "currency": self.currency,
            "date": self.date.strftime('%d.%m.%Y')}

def get_name(data):
    for context in data['result']['contexts']:
        if context['name'] == 'login':
            return context['parameters']['Name']

@app.route('/balance', methods=['GET', 'POST'])
def balance():
    data = request.get_json()
    balance = 0
    name = get_name(data) if request.method == 'POST' else "Danel"
    for t in Transaction.query.all():
        if t.recipient == name:
            balance += t.amount
        elif t.sender == name:
            balance -= t.amount
    response = ("{}'s balance is {} Swiss Francs.".format(name, balance))
    return jsonify({"speech": response, "displayText": response})


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
    db.create_all()
    for person in ["Daniel", "John", "Dina"]:
        salary = Transaction("ETH Zurich", person, "Salary", 1000, "CHF")
        db.session.add(salary)
    db.session.commit()
    app.run(debug=True)
