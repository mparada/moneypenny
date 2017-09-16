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
