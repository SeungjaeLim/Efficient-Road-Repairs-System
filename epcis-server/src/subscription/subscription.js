const express = require('express');
var request = require('request');


var server = express();

server.disable('x-powered-by');

server.use(express.json())

server.post('/subscription', function (req, res) {
    console.log("Got a POST  subscription ID " );
    console.log("req " , JSON.stringify(req.body, null, 2));
    //console.log("req " , req.body);
    res.status(200).send('Hello POST');
 })
 
server.listen(8082, () => {
    console.log("EPCIS Clinet for webhook Started");
    console.log("EPCIS Server running on port ", 8082);
});

scheduleSubscription();
//streanSubscription();
function scheduleSubscription(){
    request({
        uri: 'http://127.0.0.1:8090/epcis/v2/queries/UniqueQueryName/subscriptions',
        method: 'POST',
        body: {
            "dest": "http://localhost:8082/subscription",
            "signatureToken": "13df38d8275b13f05704629e5f1cf3d45d6132d5",
            "schedule": {
              "second": "*/15"
            }
          },
        json: true
      }, function (error, response, body) {
        if (!error) {
          console.log("sent")
          console.log("response ", response.statusCode);
          console.log("body ", response.body);
        }
        else {
          console.log("error not found")
          console.log(error);
        }
      });
}

function streanSubscription(){
    request({
        uri: 'http://127.0.0.1:8090/epcis/v2/queries/UniqueQueryName/subscriptions',
        method: 'POST',
        body: {
            "dest": "http://localhost:8082/subscription",
            "signatureToken": "13df38d8275b13f05704629e5f1cf3d45d6132d5",
            "stream": true
          },
        json: true
      }, function (error, response, body) {
        if (!error) {
          console.log("sent")
          console.log("response ", response.statusCode);
        }
        else {
          console.log("error not found")
          console.log(error);
        }
      });
}




















