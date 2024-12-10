const express = require('express');
const app = express();
const swaggerUi = require('swagger-ui-express');
var PORT = 8081;
/*
var options = {
  swaggerOptions: {
    url: 'https://ref.gs1.org/standards/epcis/2.0.0/openapi.json'
  }
}

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(null, options));

*/

const swaggerDocument = require('./epcisV2_openapi.json');
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.listen(PORT, function(err){
    if (err) console.log("Error in server setup")
    console.log("Server listening on Port", PORT);
    console.log('API-Interface localhost:'+PORT+'/api-docs');
})