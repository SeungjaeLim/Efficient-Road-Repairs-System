require('dotenv').config({ path: "../config/.env" })

exports.urn_dl = (urn)=>{
    const urn_pars = urn.split(':');
    if(urn_pars[3]=='sgtin'){
        const sgtin=urn_pars[4].split('.')
        const sgtinDl=this.sgtin_dl(sgtin[0],sgtin[1]);
        return sgtinDl;
    }
    
    
}


exports.sgtin_dl = (company_prefix, serial)=>{

    return process.env.GS1_Digital_Link_prefixed+'/01/'+company_prefix+'/21/'+serial;
}

exports.sgln_dl = (company_prefix, serial)=>{

}

//GS1_Digital_Link_prefixed

exports.gln_dl = (company_prefix)=>{

}

//SGLN_URN("")