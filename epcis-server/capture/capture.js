var request = require('request');

require('dotenv').config({ path: "../config/.env" })


const examples = require('./examples');


exports.postepcis = (epcisDoc)=>{

    request({
        uri:process.env.EPCIS_CAPTURE_END_POINT,
        method: 'POST',
        body: epcisDoc,
        json:true

    }, function(error, response, body){
        if (!error && response.statusCode == 200) {
            console.log("response " , response.statusCode);
        }
        else{
            console.log(error);
        }
      });

}


