#!/bin/sh

OUTPUT="hh_concatenated.csv"

FIRST_FILE=$(ls [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv | sort | head -1)
HEADER=$(head -1 "$FIRST_FILE")

echo "$HEADER" > "$OUTPUT"

for f in $(ls [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv | sort); do
    tail -n +2 "$f" >> "$OUTPUT"
done

echo "Done! All partitions concatenated into $OUTPUT"
