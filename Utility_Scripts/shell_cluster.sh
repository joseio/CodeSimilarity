#!/bin/bash

# CodeHunt dataset
# py cluster.py 2 1 win-2-1 > "Results/Sector2-Level1/2020-4-15-17-31-28/Union/clusterLog.txt" &
# py cluster.py 2 2 win-2-2 > "Results/Sector2-Level2/2020-4-15-17-51-12/Union/clusterLog.txt" &
# py cluster.py 2 5 win-2-5 > "Results/Sector2-Level5/2020-4-15-19-18-35/Union/clusterLog.txt" &
# py cluster.py 2 6 win-2-6 > "Results/Sector2-Level6/2020-4-15-19-26-9/Union/clusterLog.txt" 
# wait
# py cluster.py 3 1 win-3-1 > "Results/Sector3-Level1/2020-4-15-19-34-17/Union/clusterLog.txt" &
# py cluster.py 3 2 win-3-2 > "Results/Sector3-Level2/2020-4-15-19-36-34/Union/clusterLog.txt" &
# py cluster.py 3 3 win-3-3 > "Results/Sector3-Level3/2020-4-15-19-40-16/Union/clusterLog.txt" &
# py cluster.py 3 6 win-3-6 > "Results/Sector3-Level6/2020-4-15-21-54-23/Union/clusterLog.txt" 
# wait
# py cluster.py 4 2 win-4-2 > "Results/Sector4-Level2/2020-4-15-22-2-43/Union/clusterLog.txt" &
# py cluster.py 4 3 win-4-3 > "Results/Sector4-Level3/2020-4-16-13-14-55/Union/clusterLog.txt" &
# py cluster.py 4 4 win-4-4 > "Results/Sector4-Level4/2020-4-15-22-20-27/Union/clusterLog.txt" &
# py cluster.py 4 6 win-4-6 > "Results/Sector4-Level6/2020-4-15-22-22-51/Union/clusterLog.txt" 


# Pex4Fun dataset
# Input = dataset name (e.g., CodeHunt, Pex4Fun, or PKU)
# dirs=$(find Results/$1/ -maxdepth 1 -type d | cut -c 17-) # <-- Pex4Fun
dirs=$(find Results/$1/ -maxdepth 1 -type d | cut -c 13-) # <-- PKU
for d in ${dirs[@]}; do
    echo "$d"
    py cluster.py -d $1 $d
    wait
done
$SHELL