exports.AggregationEvent={
    "@context": [
        "https://gs1.github.io/EPCIS/epcis-context.jsonld",
        {
            "example": "https://example.org/epcis"
        }
    ],
    "eventID": "ni:///sha-256;87b5f18a69993f0052046d4687dfacdf48f7c988cfabda2819688c86b4066a49?ver=CBV2.0",
    "type": "AggregationEvent",
    "eventTime": "2013-06-08T14:58:56.591Z",
    "eventTimeZoneOffset": "+02:00",
    "parentID":"urn:epc:id:sscc:0614141.1234567890",
    "childEPCs":["urn:epc:id:sgtin:0614141.107346.2017","urn:epc:id:sgtin:0614141.107346.2018"],
    "action": "OBSERVE",
    "bizStep": "receiving",
    "disposition": "in_progress",
    "readPoint": {"id": "urn:epc:id:sgln:0614141.00777.0"},
    "bizLocation": {"id": "urn:epc:id:sgln:0614141.00888.0"},
    
    "childQuantityList": [
        {"epcClass":"urn:epc:idpat:sgtin:4012345.098765.*","quantity":10},
        {"epcClass":"urn:epc:class:lgtin:4012345.012345.998877","quantity":200.5,"uom":"KGM"}
    ],
    "example:myField":"Example of a vendor/user extension"
};

exports.AssociationEvent={
    "@context": "https://gs1.github.io/EPCIS/epcis-context.jsonld",
    "eventID": "ni:///sha-256;025ac144187a8c5e14caf4d1cfa69250a33dc59a5bc42a68d31b1b5e55a3f15a?ver=CBV2.0",
    "type": "AssociationEvent",
    "eventTime": "2019-11-01T14:00:00.000+01:00",
    "eventTimeZoneOffset": "+01:00",
    "parentID":"urn:epc:id:grai:4012345.55555.987",
    "childEPCs":["urn:epc:id:giai:4000001.12345"],
    "action": "ADD",
    "bizStep": "assembling",
    "readPoint": {"id": "urn:epc:id:sgln:4012345.00001.0"}
};


exports.Extended_Event={
    "@context": [
        "https://gs1.github.io/EPCIS/epcis-context.jsonld",
        {
            "example": "https://example.org/epcis"
        }
    ],
    "type": "example:CustomEvent",
    "eventTime": "2005-04-03T20:33:31.116000-06:00",
    "eventTimeZoneOffset": "-06:00"
};


exports.ObjectEvent={
    "@context": "https://gs1.github.io/EPCIS/epcis-context.jsonld",
    "eventID": "ni:///sha-256;df7bb3c352fef055578554f09f5e2aa41782150ced7bd0b8af24dd3ccb30ba69?ver=CBV2.0",
    "type": "ObjectEvent",
    "action": "OBSERVE",
    "bizStep": "shipping",
    "disposition": "in_transit",
    "epcList": ["urn:epc:id:sgtin:0614141.107346.2017","urn:epc:id:sgtin:0614141.107346.2018"],
    "eventTime": "2005-04-03T20:33:31.116000-06:00",
    "eventTimeZoneOffset": "-06:00",
    "readPoint": {"id": "urn:epc:id:sgln:0614141.07346.1234"},
    "bizTransactionList": [  {"type": "po", "bizTransaction": "http://transaction.acme.com/po/12345678" }  ]
};


exports.TransformationEvent={
    "@context": [
        "https://gs1.github.io/EPCIS/epcis-context.jsonld",
        {
            "example": "https://example.org/epcis"
        }
    ],
    "eventID": "ni:///sha-256;e65c3a997e77f34b58306da7a82ab0fc91c7820013287700f0b50345e5795b97?ver=CBV2.0",
    "type": "TransformationEvent",
    "eventTime": "2013-10-31T14:58:56.591Z",
    "eventTimeZoneOffset": "+02:00",
    "inputEPCList": ["urn:epc:id:sgtin:4012345.011122.25","urn:epc:id:sgtin:4000001.065432.99886655"],
    "inputQuantityList": [{"epcClass":"urn:epc:class:lgtin:4012345.011111.4444","quantity":10,"uom":"KGM"},
            {"epcClass":"urn:epc:class:lgtin:0614141.077777.987","quantity":30},
            {"epcClass":"urn:epc:idpat:sgtin:4012345.066666.*","quantity":220}		  		
    ],
    "outputEPCList": [
        "urn:epc:id:sgtin:4012345.077889.25",
        "urn:epc:id:sgtin:4012345.077889.26",
        "urn:epc:id:sgtin:4012345.077889.27",
        "urn:epc:id:sgtin:4012345.077889.28"
    ],
  
    "bizStep": "commissioning",
    "disposition": "in_progress",
    "readPoint": {"id": "urn:epc:id:sgln:4012345.00001.0"},
    "ilmd": {"example:bestBeforeDate":"2014-12-10","example:batch":"XYZ" },
    "example:myField":"Example of a vendor/user extension"
};




exports.AllEvents = [
{
    "@context": [
        "https://gs1.github.io/EPCIS/epcis-context.jsonld",
        {
            "example": "https://example.org/epcis"
        }
    ],
    "eventID": "ni:///sha-256;87b5f18a69993f0052046d4687dfacdf48f7c988cfabda2819688c86b4066a49?ver=CBV2.0",
    "type": "AggregationEvent",
    "eventTime": "2013-06-08T14:58:56.591Z",
    "eventTimeZoneOffset": "+02:00",
    "parentID":"urn:epc:id:sscc:0614141.1234567890",
    "childEPCs":["urn:epc:id:sgtin:0614141.107346.2017","urn:epc:id:sgtin:0614141.107346.2018"],
    "action": "OBSERVE",
    "bizStep": "receiving",
    "disposition": "in_progress",
    "readPoint": {"id": "urn:epc:id:sgln:0614141.00777.0"},
    "bizLocation": {"id": "urn:epc:id:sgln:0614141.00888.0"},
    
    "childQuantityList": [
        {"epcClass":"urn:epc:idpat:sgtin:4012345.098765.*","quantity":10},
        {"epcClass":"urn:epc:class:lgtin:4012345.012345.998877","quantity":200.5,"uom":"KGM"}
    ],
    "example:myField":"Example of a vendor/user extension"
},
{
    "@context": "https://gs1.github.io/EPCIS/epcis-context.jsonld",
    "eventID": "ni:///sha-256;df7bb3c352fef055578554f09f5e2aa41782150ced7bd0b8af24dd3ccb30ba69?ver=CBV2.0",
    "type": "ObjectEvent",
    "action": "OBSERVE",
    "bizStep": "shipping",
    "disposition": "in_transit",
    "epcList": ["urn:epc:id:sgtin:0614141.107346.2017","urn:epc:id:sgtin:0614141.107346.2018"],
    "eventTime": "2005-04-03T20:33:31.116000-06:00",
    "eventTimeZoneOffset": "-06:00",
    "readPoint": {"id": "urn:epc:id:sgln:0614141.07346.1234"},
    "bizTransactionList": [  {"type": "po", "bizTransaction": "http://transaction.acme.com/po/12345678" }  ]
},
{
    "@context": "https://gs1.github.io/EPCIS/epcis-context.jsonld",
    "eventID": "ni:///sha-256;025ac144187a8c5e14caf4d1cfa69250a33dc59a5bc42a68d31b1b5e55a3f15a?ver=CBV2.0",
    "type": "AssociationEvent",
    "eventTime": "2019-11-01T14:00:00.000+01:00",
    "eventTimeZoneOffset": "+01:00",
    "parentID":"urn:epc:id:grai:4012345.55555.987",
    "childEPCs":["urn:epc:id:giai:4000001.12345"],
    "action": "ADD",
    "bizStep": "assembling",
    "readPoint": {"id": "urn:epc:id:sgln:4012345.00001.0"}
},
{
    "@context": [
        "https://gs1.github.io/EPCIS/epcis-context.jsonld",
        {
            "example": "https://example.org/epcis"
        }
    ],
    "eventID": "ni:///sha-256;e65c3a997e77f34b58306da7a82ab0fc91c7820013287700f0b50345e5795b97?ver=CBV2.0",
    "type": "TransformationEvent",
    "eventTime": "2013-10-31T14:58:56.591Z",
    "eventTimeZoneOffset": "+02:00",
    "inputEPCList": ["urn:epc:id:sgtin:4012345.011122.25","urn:epc:id:sgtin:4000001.065432.99886655"],
    "inputQuantityList": [{"epcClass":"urn:epc:class:lgtin:4012345.011111.4444","quantity":10,"uom":"KGM"},
            {"epcClass":"urn:epc:class:lgtin:0614141.077777.987","quantity":30},
            {"epcClass":"urn:epc:idpat:sgtin:4012345.066666.*","quantity":220}		  		
    ],
    "outputEPCList": [
        "urn:epc:id:sgtin:4012345.077889.25",
        "urn:epc:id:sgtin:4012345.077889.26",
        "urn:epc:id:sgtin:4012345.077889.27",
        "urn:epc:id:sgtin:4012345.077889.28"
    ],
  
    "bizStep": "commissioning",
    "disposition": "in_progress",
    "readPoint": {"id": "urn:epc:id:sgln:4012345.00001.0"},
    "ilmd": {"example:bestBeforeDate":"2014-12-10","example:batch":"XYZ" },
    "example:myField":"Example of a vendor/user extension"
}

];


exports.test =
{
    "type": "EPCISDocument",
    "schemaVersion": "2.0",
    "creationDate": "2013-06-04T14:59:02.099+02:00",
    "sender": "urn:epc:id:sgln:0353579.00001.0",
    "receiver": "urn:epc:id:sgln:5012345.00001.0",
    "instanceIdentifier": "1234567890",
    "epcisBody": {
      "eventList": [
        {
          "type": "ObjectEvent",
          "eventTime": "2005-04-05T02:33:31.116Z",
          "eventTimeZoneOffset": "-06:00",
          "eventID": "urn:uuid:374d95fc-9457-4a51-bd6a-0bba133845a8",
          "certificationInfo": "https://accreditation-council.example.org/certificate/ABC12345",
          "epcList": [
            "urn:epc:id:sgtin:0614141.107346.6080"
          ],
          "action": "ADD",
          "bizStep": "receiving",
          "disposition": "in_progress",
          "readPoint": {
            "id": "urn:epc:id:sgln:0012345.11111.400"
          },
          "bizLocation": {
            "id": "urn:epc:id:sgln:0012345.11111.0"
          },
          "bizTransactionList": [
            {
              "type": "po",
              "bizTransaction": "urn:epc:id:gdti:0614141.00001.1618034"
            },
            {
              "type": "pedigree",
              "bizTransaction": "urn:epc:id:gsrn:0614141.0000010253"
            }
          ],
          "quantityList": [
            {
              "epcClass": "urn:epc:class:lgtin:4012345.012345.998877",
              "quantity": 200,
              "uom": "KGM"
            }
          ],
          "sourceList": [
            {
              "type": "location",
              "source": "urn:epc:id:sgln:4012345.00225.0"
            },
            {
              "type": "possessing_party",
              "source": "urn:epc:id:pgln:4012345.00225"
            },
            {
              "type": "owning_party",
              "source": "urn:epc:id:pgln:4012345.00225"
            }
          ],
          "destinationList": [
            {
              "type": "location",
              "destination": "urn:epc:id:sgln:0614141.00777.0"
            },
            {
              "type": "possessing_party",
              "destination": "urn:epc:id:pgln:0614141.00777"
            },
            {
              "type": "owning_party",
              "destination": "urn:epc:id:pgln:0614141.00777"
            }
          ],
          "sensorElementList": [
            {
              "sensorMetadata": {
                "time": "2019-04-02T13:05:00.000Z",
                "deviceID": "urn:epc:id:giai:4000001.111",
                "deviceMetadata": "https://id.gs1.org/8004/4000001111",
                "rawData": "https://example.org/8004/401234599999",
                "startTime": "2019-04-02T12:55:01.000Z",
                "endTime": "2019-04-02T13:55:00.000Z",
                "dataProcessingMethod": "https://example.com/253/4012345000054987",
                "bizRules": "https://example.com/253/4012345000054987",
                "ext1:someFurtherMetadata": "someText"
              },
              "sensorReport": [
                {
                  "type": "Temperature",
                  "deviceID": "urn:epc:id:giai:4000001.111",
                  "rawData": "https://example.org/8004/401234599999",
                  "dataProcessingMethod": "https://example.com/253/4012345000054987",
                  "time": "2019-07-19T13:00:00.000Z",
                  "microorganism": "https://www.ncbi.nlm.nih.gov/taxonomy/1126011",
                  "chemicalSubstance": "https://identifiers.org/inchikey:CZMRCDWAGMRECN-UGDNZRGBSA-N",
                  "value": 26,
                  "component": "example:x",
                  "stringValue": "SomeString",
                  "booleanValue": true,
                  "hexBinaryValue": "f0f0f0",
                  "uriValue": "https://id.gs1.org/8004/4000001111",
                  "minValue": 26,
                  "maxValue": 26.2,
                  "meanValue": 13.2,
                  "percRank": 50,
                  "percValue": 12.7,
                  "uom": "CEL",
                  "sDev": 0.1,
                  "ext1:someFurtherReportData": "someText",
                  "deviceMetadata": "https://id.gs1.org/8004/4000001111"
                }
              ]
            }
          ],
          "persistentDisposition": {
            "set": [
              "completeness_verified"
            ],
            "unset": [
              "completeness_inferred"
            ]
          }
        }
      ]
    },
    "@context": [
          "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
          {
            "ext3": "http://example.com/ext3/", "ext2": "http://example.com/ext2/", "ext1": "http://example.com/ext1/"
          }
        ]
  }
  