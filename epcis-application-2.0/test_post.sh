#!/bin/bash

# 서버 URL 및 도메인 설정
SERVER_URL="http://localhost:8090/epcis/v2/events"
DOMAIN="https://yourdomain.com"

# POST 요청 데이터 정의
POST_DATA=$(cat <<EOF
{
  "@context": [
    "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
    {
      "$DOMAIN/damageType": "$DOMAIN/vocab/damageType",
      "$DOMAIN/dimensions": "$DOMAIN/vocab/dimensions",
      "$DOMAIN/repairCost": "$DOMAIN/vocab/repairCost",
      "$DOMAIN/repairItems": "$DOMAIN/vocab/repairItems"
    }
  ],
  "type": "ObjectEvent",
  "action": "ADD",
  "bizStep": "repairing",
  "disposition": "in_progress",
  "epcList": ["urn:epc:id:road:0012345"],
  "eventTime": "2024-12-11T10:00:00.000Z",
  "eventTimeZoneOffset": "+00:00",
  "readPoint": {
    "id": "urn:epc:id:geo:37.7750,-122.4195"
  },
  "ilmd": {
    "$DOMAIN/dimensions": {
      "Width": 0,
      "Height": 0
    },
    "$DOMAIN/damageType": "longitudinal crack",
    "$DOMAIN/repairCost": {
      "TotalCost": 1300,
      "items": [
        {
          "ItemDescription": "Surface Cleaning and Preparation",
          "Quantity": 1,
          "UnitPrice": 200
        },
        {
          "ItemDescription": "Crack Filling Material (Epoxy/Asphalt)",
          "Quantity": 50,
          "UnitPrice": 5
        },
        {
          "ItemDescription": "Labor Costs for Repair Team",
          "Quantity": 3,
          "UnitPrice": 100
        },
        {
          "ItemDescription": "Equipment Rental (Crack Sealing Machine)",
          "Quantity": 1,
          "UnitPrice": 300
        },
        {
          "ItemDescription": "Post-Repair Inspection and Testing",
          "Quantity": 1,
          "UnitPrice": 150
        },
        {
          "ItemDescription": "Traffic Management (Signs/Barriers)",
          "Quantity": 1,
          "UnitPrice": 100
        }
      ]
    }
  }
}
EOF
)

# POST 요청 전송
echo "Sending POST request to $SERVER_URL..."
curl -s -X POST "$SERVER_URL" \
-H "Content-Type: application/json" \
-H "GS1-EPCIS-Version: 2.0.0" \
-H "GS1-CBV-Version: 2.0.0" \
-d "$POST_DATA"

echo ""
echo "POST request sent successfully."

# GET 요청 전송
echo "Fetching data from $SERVER_URL..."
GET_RESPONSE=$(curl -s -X GET "$SERVER_URL" \
-H "Content-Type: application/json" \
-H "GS1-EPCIS-Version: 2.0.0" \
-H "GS1-CBV-Version: 2.0.0")

# 데이터를 JSON 포맷으로 출력
echo "Processing and formatting the response..."
echo "$GET_RESPONSE" | jq --arg DOMAIN "$DOMAIN" '.epcisBody.queryResults.resultBody.eventList[] | {
  "Event Time": .eventTime,
  "EPC List": .epcList,
  "Geo Location": .readPoint.id,
  "Damage Type": .ilmd[$DOMAIN + "/damageType"],
  "Repair Cost": .ilmd[$DOMAIN + "/repairCost"].TotalCost,
  "Repair Items": .ilmd[$DOMAIN + "/repairCost"].items,
  "Dimensions": .ilmd[$DOMAIN + "/dimensions"]
}' || echo "Error: Please ensure jq is installed to format the output."
