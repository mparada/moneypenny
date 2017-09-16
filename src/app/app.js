/**
 * Copyright 2017, Google, Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

// [START app]
const express = require('express');
const crypto = require('crypto');

const app = express();
app.enable('trust proxy');

const http = require('http').Server(app);
const io = require('socket.io')(http);

// Imports the Google Cloud client library
const Datastore = require('@google-cloud/datastore');

// Your Google Cloud Platform project ID
const projectId = 'moneypenny-dabc6';

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});

app.get('/helloHttp', (req, res) => {
  const response = "This is a sample response from your webhook!" //Default response from the webhook to show it's working
  io.emit('chat message', response);
  res.setHeader('Content-Type', 'application/json'); //Requires application/json MIME type
  res.send(JSON.stringify({ "speech": response, "displayText": response}));
});

app.get('/transaction', (req, res) => {
  // Instantiates a client
  const datastore = Datastore({
    projectId: projectId
  });

  // The kind for the new entity
  const kind = 'Transaction';
  // The Cloud Datastore key for the new entity
  const transactionKey = datastore.key(kind);
  // amount	currency	date	recipient	reference	sender


  // const login_params = req.body.result.contexts.filter((obj) => obj.name === 'login')[0].parameters;
  const trans_params = req.body.result.contexts.filter((obj) => obj.name === 'do_transaction-followup')[0].parameters;

  const transaction = {
    key: transactionKey,
    data: {
      amount: trans_params.money.amount,
      currency: trans_params.money.currency,
      date: new Date().toJSON(),
      recipient: trans_params.recipient,
      // sender: login_params.Name,
      reference: "Smart Voice Transaction",
    }
  };

  // Saves the entity
  datastore.save(transaction)
    .then(() => {
      // console.log(`Saved ${transaction.key}`);
      console.log('Saved ' + transaction.key);

      const response = `${transaction.data.amount} ${transaction.data.currency} have been sent to ${transaction.data.recipient}.`;

      res.setHeader('Content-Type', 'application/json'); //Requires application/json MIME type
      res.send(JSON.stringify({ "speech": response, "displayText": response}));

    })
    .catch((err) => {
      console.error('ERROR:', err);
    });

});

// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log('App listening on port ${PORT}');
  console.log('Press Ctrl+C to quit.');
});
// [END app]
