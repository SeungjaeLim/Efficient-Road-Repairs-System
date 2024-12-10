# epcis-application-2.0

This repository provides  
- Docker file for epcis 2.0
- EPCIS 2.0 REST API Documentation using swagger interface 
- Library to constract events to capture to epcis and query from epcis.

## To run epcis 2.0 on docker
```console
cd epcisV2/{version}
docker-compose pull
docker-compose up
```

## EPCIS 2.0 REST API Documentation
```console
cd src
npm install
node openApi.js
```
Go to browser and access localhost:8081/api-docs

You will see the following: 

![Alt text](./docs/swagger.png?raw=true "Title")



## epcis capturing application


## epcis querying application


## epcis MQQT Subscription Example
You can find the mqtt client example to subscribe and 

