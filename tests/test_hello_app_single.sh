
QUERY="{ \"log-messages\": [ { \"private-key\": \"raghsmqjmftu10fngvb89a7fgoo\", \"app\": \"test\", \"level\": \"INFO\", \"message\": \"string\" } ]}"
echo $QUERY
curl -X POST "http://wally113.cit.tu-berlin.de:5444/api_v1/data" \
 -H "accept: application/json" \
 -H "Content-Type: application/json" \
 -d "$QUERY"

