#!/bin/sh
jq -r '
["id","created_at","name","has_test","alternate_url"],
(.items[] | [.id,.created_at,.name,.has_test,.alternate_url])
| @csv
' ../ex00/hh.json > hh.csv

echo "Done! CSV saved to hh.csv"
