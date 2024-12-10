const crypto = require('crypto');
//const { uuid } = require('');

exports.uuid = ()=>{
    //return crypto.randomUUID()
    return crypto.randomBytes(20).toString('hex');
    //return uuid();
}

exports.epcisHashValue = (epcis_doc)=>{
    return "under constraction"
}
