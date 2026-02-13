#!/bin/sh

# keep header
head -n 1 ../ex01/hh.csv > hh_sorted.csv

# sort by created_at (2nd col), then id (1st col)
tail -n +2 ../ex01/hh.csv | sort -t',' -k2,2 -k1,1 >> hh_sorted.csv

echo "Done! Sorted CSV saved to hh_sorted.csv"
