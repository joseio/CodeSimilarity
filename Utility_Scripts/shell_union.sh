#!/bin/bash
# Input = dataset name (e.g., CodeHunt, Pex4Fun, or PKU)
dirs=$(find Results/$1/ -maxdepth 1 -type d | cut -c 17-)
for d in ${dirs[@]}; do
    echo "$d"
    py union_tests.py -d $1 $d
    wait
done