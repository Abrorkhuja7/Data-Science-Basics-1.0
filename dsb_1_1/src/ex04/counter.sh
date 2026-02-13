#!/bin/sh

INPUT="../ex03/hh_positions.csv"
OUTPUT="hh_uniq_positions.csv"

echo '"name","count"' > "$OUTPUT"

tail -n +2 "$INPUT" | \
    cut -d',' -f3 | \
    sort | \
    uniq -c | \
    sort -rn | \
    sed 's/^ *//' | \
    awk '{count=$1; $1=""; name=substr($0,2); print name","count}' >> "$OUTPUT"

echo "Done! Unique positions saved to $OUTPUT"
