#!/bin/sh

awk -F',' 'BEGIN{OFS=","}
NR==1 {print; next}
{
  name=$3
  if (name ~ /Junior|Middle|Senior/) {
    out=""
    if (name ~ /Junior/) out=out (out?"/":"") "Junior"
    if (name ~ /Middle/) out=out (out?"/":"") "Middle"
    if (name ~ /Senior/) out=out (out?"/":"") "Senior"
    $3="\"" out "\""
  } else {
    $3="\"-\""
  }
  print
}' ../ex02/hh_sorted.csv > hh_positions.csv

echo "Done! Cleaned CSV saved to hh_positions.csv"
