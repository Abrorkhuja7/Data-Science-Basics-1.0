#!/bin/sh

INPUT="../ex03/hh_positions.csv"
HEADER=$(head -1 "$INPUT")

# Process each data row
tail -n +2 "$INPUT" | while IFS= read -r line; do
    date=$(echo "$line" | cut -d',' -f2 | tr -d '"' | cut -dT -f1)

    outfile="${date}.csv"

    if [ ! -f "$outfile" ]; then
        echo "$HEADER" > "$outfile"
    fi

    echo "$line" >> "$outfile"
done

echo "Done! Partition files created for each date."
