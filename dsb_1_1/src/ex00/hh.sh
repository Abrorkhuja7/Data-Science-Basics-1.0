#!/bin/sh

# The vacancy name is passed as the first argument
VACANCY="$1"

# Call the HH API:
# - text: the search query (URL-encoded automatically by curl with --data-urlencode)
# - per_page: how many results to fetch (20)
# - page: which page (0 = first)
curl -s \
  -H "User-Agent: ex00 (School 21, Tashkent)" \
  --get "https://api.hh.ru/vacancies" \
  --data-urlencode "text=$VACANCY" \
  --data-urlencode "per_page=20" \
  --data-urlencode "page=0" \
  | jq '.' > hh.json

echo "Done! Results saved to hh.json"
