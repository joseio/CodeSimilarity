#!/bin/bash
# Input = dataset name (e.g., CodeHunt, Pex4Fun, or PKU)
# dirs=$(find Collected/$1/ -maxdepth 1 -type d | cut -c 19-) # <-- For Pex4Fun

dirs=$(find Collected/$1/ -maxdepth 1 -type d | cut -c 15-) # <-- For PKU
for d in ${dirs[@]}; do
    echo "$d"
    py runpex.py -j 8 -d $1 $d
    wait
done
$SHELL