var fs = require('fs');
/*
* HTTP Cloud Function.
*
* @param {Object} req Cloud Function request context.
* @param {Object} res Cloud Function response context.
*/
exports.helloHttp = function helloHttp (req, res) {
  response = "This is a sample response from your webhook!" //Default response from the webhook to show it's working

  res.setHeader('Content-Type', 'application/json'); //Requires application/json MIME type
  res.send(JSON.stringify({ "speech": response, "displayText": response
  }));
  //"speech" is the spoken version of the response, "displayText" is the visual version
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write(fs.readFileSync('https://storage.googleapis.com/moneypenny-dabc6.appspot.com/index.html'));
  res.end();

};


exports.transaction = function transaction (req, res) {
  // Imports the Google Cloud client library
  const Datastore = require('@google-cloud/datastore');

  // Your Google Cloud Platform project ID
  const projectId = 'moneypenny-dabc6';

  // Instantiates a client
  const datastore = Datastore({
    projectId: projectId
  });

  // The kind for the new entity
  const kind = 'Transaction';
  // The Cloud Datastore key for the new entity
  const transactionKey = datastore.key(kind);
// amount	currency	date	recipient	reference	sender
  // Prepares the new entity
  const transaction = {
    key: transactionKey,
    data: {
      amount: 0.00,
      currency: 'CHF',
      date: new Date().toJSON(),
      recipient: "Bob",
      sender: "Alice",
      reference: "Default",
    }
  };

  // Saves the entity
  datastore.save(transaction)
    .then(() => {
      console.log(`Saved ${transaction.key}`);

      const response = `Send ${transaction.data.amount}
        ${transaction.data.currency} to ${transaction.data.recipient}`.

      res.setHeader('Content-Type', 'application/json'); //Requires application/json MIME type
      res.send(JSON.stringify({ "speech": response, "displayText": response
        //"speech" is the spoken version of the response, "displayText" is the visual version
      }));

    })
    .catch((err) => {
      console.error('ERROR:', err);
    });
};
