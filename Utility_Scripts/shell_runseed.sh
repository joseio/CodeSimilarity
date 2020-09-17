#!/bin/bash

# CodeHunt dataset
# py runseed.py -j 8 2 2
# wait
# py runseed.py -j 8 2 5
# wait
# py runseed.py -j 8 2 6
# wait
# py runseed.py -j 8 3 1
# wait
# py runseed.py -j 8 3 2
# wait
# py runseed.py -j 8 3 3
# wait
# py runseed.py -j 8 3 6
# wait
# py runseed.py -j 8 4 2
# wait
# py runseed.py -j 8 4 3
# wait
# py runseed.py -j 8 4 4 
# wait
# py runseed.py -j 8 4 6


# Pex4Fun dataset
# Input = dataset name (e.g., CodeHunt, Pex4Fun, or PKU)
dirs=$(find Results/$1/ -maxdepth 1 -mindepth 1 -type d | cut -c 13-)
for d in ${dirs[@]}; do
    echo "$d"
    py runseed.py -j 8 -d $1 $d
    wait
done
$SHELL