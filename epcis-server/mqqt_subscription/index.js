const mqtt = require('mqtt');


//const mqttBrokerUrl = 'mqtt://your-mqtt-broker'; // Replace with your MQTT broker URL
const mqttBrokerUrl = 'mqtt://localhost:1883';

// Create a MQTT client and connect to the broker
const mqttClient = mqtt.connect(mqttBrokerUrl);

// Event handler for MQTT client connection
mqttClient.on('connect', () => {
  console.log('Connected to MQTT broker');
  // Subscribe to a topic
  mqttClient.subscribe('epcisv2');
});

// Event handler for MQTT client connection
mqttClient.on('connect', () => {
    console.log('Connected to MQTT broker');
    // You can do further actions here when the client is connected
  });
  
  // Event handler for MQTT client errors
mqttClient.on('error', (error) => {
    console.error('MQTT client error:', error);
    // Handle the error as needed
  });


// Event handler for incoming MQTT messages
mqttClient.on('message', (topic, message) => {
  console.log(`Received message on topic '${topic}': ${message.toString()}`);
  // Here, you can handle the incoming MQTT message as required
});
