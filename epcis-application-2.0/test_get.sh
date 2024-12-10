#!/bin/bash

# 서버 URL 및 도메인 설정
SERVER_URL="http://localhost:8090/epcis/v2/events"
DOMAIN="https://yourdomain.com"

# GET 요청 전송
echo "Fetching data from $SERVER_URL..."
GET_RESPONSE=$(curl -s -X GET "$SERVER_URL" \
-H "Content-Type: application/json" \
-H "GS1-EPCIS-Version: 2.0.0" \
-H "GS1-CBV-Version: 2.0.0")

# 변경되지 않은 데이터 필터링 및 출력
echo "Filtering unprocessed events..."
echo "$GET_RESPONSE" | jq --arg DOMAIN "$DOMAIN" '
.epcisBody.queryResults.resultBody.eventList[]
| select(.bizStep != "completed" and .disposition != "resolved") 
| {
    "Event Time": .eventTime,
    "EPC List": .epcList,
    "Geo Location": .readPoint.id,
    "Damage Type": .ilmd[$DOMAIN + "/damageType"],
    "Repair Cost": .ilmd[$DOMAIN + "/repairCost"].TotalCost,
    "Repair Items": .ilmd[$DOMAIN + "/repairCost"].items,
    "Dimensions": .ilmd[$DOMAIN + "/dimensions"]
}' || echo "Error: Please ensure jq is installed to format the output."

echo "Unprocessed events listed above."
