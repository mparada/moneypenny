#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Flask, request, jsonify, send_from_directory)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import datetime
import os
from threading import Event

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)
socketio = SocketIO(app)

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


def get_name(result):
    for context in result['contexts']:
        if context['name'] == 'login':
            return context['parameters']['Name']

@app.route('/FE/<path:path>')
def send_fe(path):
    return send_from_directory('../FE', path)

@app.route('/money_penny', methods=['GET', 'POST'])
def money_penny():
    result = request.get_json()['result']
    if result['action'] == 'get_balance':
        name = get_name(result) if request.method == 'POST' else "Daniel"
        return get_balance(name)
    elif result['action'] == 'mortgagecall.mortgagecall-yes':
        name = get_name(result) if request.method == 'POST' else "Daniel"
        return customer(name)
    else:
        return get_transaction()


@app.route('/balance', methods=['GET', 'POST'])
def get_balance(name="Daniel"):
    balance = 0
    for t in Transaction.query.all():
        if t.recipient == name:
            balance += t.amount
        elif t.sender == name:
            balance -= t.amount
    response = ("{}'s balance is {} USD.".format(name, balance))
    socketio.emit('balance', response)
    return jsonify({"speech": response, "displayText": response})


@app.route('/transaction', methods=['GET', 'POST'])
def get_transaction():
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

        socketio.emit('transaction', 'Transferring ' + str(amount) + ' ' + currency + ' to ' + recipient + '.')

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
def customer(name="Daniel"):
    socketio.emit('name', name)
    response = "Got Customer"
    return jsonify({"speech": response, "displayText": response})

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

if __name__ == "__main__":
    db.create_all()
    for person in ["Daniel", "John", "Dina"]:
        salary = Transaction("ETH Zurich", person, "Salary", 1000, "CHF")
        db.session.add(salary)
    db.session.commit()
    socketio.run(app)
    #app.run(debug=True)
