
require('dotenv').config({ path: "./config/.env" })

const eventIdGen = require('./utili/eventIdGen.js');
const examples = require('./capture/examples.js');
const getDigital = require('./utili/digitalLink.js');
const capture = require('./capture/capture.js');
const query = require('./query/query.js');

//getepcis()

//Generates uuid
console.log(eventIdGen.uuid());
//Generates hashValue given an epcis document

const epcis_doc={}
//console.log(eventIdGen.epcisHashValue(epcis_doc));

//capture a simple 
//console.log(examples.ObjectEvent);
//console.log(examples.test);


const urn="urn:epc:id:sgtin:0614141.107346.2018";
getDigital.urn_dl(urn);

//console.log(process.env.EPCIS_END_POINT)

//capture epcis document
//capture.postepcis(examples.test)


//query epcis document
//query.getEPCIS2();