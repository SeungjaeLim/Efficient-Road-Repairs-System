#!/usr/bin/env node
var WebSocketClient = require('websocket').client;

var client = new WebSocketClient();

client.on('connectFailed', function(error) {
    console.log('Connect Error: ' + error.toString());
});

client.on('connect', function(connection) {
    console.log('connection upgrade');
    connection.send('Message from the client!');

    connection.on('error', function(error) {
        console.log("Connection Error: " + error.toString());
    });
    connection.on('close', function() {
        console.log('echo-protocol Connection Closed');
    });
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log("Received: '" + message.utf8Data + "'");
        }else{
            console.log("message.type: " + message.type );
        }
    });
    
     

});


//client.connect('ws://localhost:8085/queries/queryNameUnic/events?second=*/10');
client.connect('ws://localhost:8090/queries/UniqueQueryName/events?second=*/15');