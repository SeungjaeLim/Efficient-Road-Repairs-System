#!/bin/bash

# 서버 URL 설정
SERVER_URL="http://localhost:8090/epcis/v2/events"
DOMAIN="https://yourdomain.com"

# GET 요청으로 기존 이벤트 가져오기
echo "Fetching existing data from $SERVER_URL..."
GET_RESPONSE=$(curl -s -X GET "$SERVER_URL" \
-H "Content-Type: application/json" \
-H "GS1-EPCIS-Version: 2.0.0" \
-H "GS1-CBV-Version: 2.0.0")

# 이벤트 리스트 추출
EVENT_LIST=$(echo "$GET_RESPONSE" | jq -c '.epcisBody.queryResults.resultBody.eventList[]')

if [ -z "$EVENT_LIST" ]; then
  echo "No events found to process."
  exit 0
fi

# 상태를 변경할 bizStep 및 disposition 설정
NEW_BIZSTEP="urn:epcglobal:cbv:bizstep:inactive"
NEW_DISPOSITION="urn:epcglobal:cbv:disp:disposed"

# 각 이벤트를 업데이트
echo "Processing and updating each event..."
echo "$EVENT_LIST" | while IFS= read -r EVENT; do
  EVENT_TIME=$(echo "$EVENT" | jq -r '.eventTime')
  EPC_LIST=$(echo "$EVENT" | jq -c '.epcList')
  READ_POINT=$(echo "$EVENT" | jq -r '.readPoint.id')

  # POST 데이터 구성
  POST_DATA=$(jq -n \
    --arg context "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld" \
    --arg bizStep "$NEW_BIZSTEP" \
    --arg disposition "$NEW_DISPOSITION" \
    --argjson epcList "$EPC_LIST" \
    --arg eventTime "$EVENT_TIME" \
    --arg readPoint "$READ_POINT" \
    '{
      "@context": $context,
      "type": "ObjectEvent",
      "action": "ADD",
      "bizStep": $bizStep,
      "disposition": $disposition,
      "epcList": $epcList,
      "eventTime": $eventTime,
      "eventTimeZoneOffset": "+00:00",
      "readPoint": {
        "id": $readPoint
      }
    }')

  echo "Debug: POST_DATA = $POST_DATA"
  echo "Updating event with EPC: $EPC_LIST..."
  curl -s -X POST "$SERVER_URL" \
  -H "Content-Type: application/json" \
  -H "GS1-EPCIS-Version: 2.0.0" \
  -H "GS1-CBV-Version: 2.0.0" \
  -d "$POST_DATA"

  echo "Event updated to bizStep: $NEW_BIZSTEP, disposition: $NEW_DISPOSITION."
done

echo "All events processed and updated."
