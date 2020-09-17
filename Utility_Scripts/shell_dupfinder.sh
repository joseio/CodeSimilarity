#!\bin\bash
root='C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results\'
cluster='\Union\clusters(pc+rv)\'

# Sector2-Level1
dirs=$(find "${root}Sector2-Level1\2020-4-15-17-31-28${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector2-Level1\2020-4-15-17-31-28${cluster}${d}"
    wait
done
# Sector2-Level2
dirs=$(find "${root}Sector2-Level2\2020-4-15-17-51-12${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector2-Level2\2020-4-15-17-51-12${cluster}${d}"
    wait
done
# Sector2-Level5
dirs=$(find "${root}Sector2-Level5\2020-4-15-19-18-35${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector2-Level5\2020-4-15-19-18-35${cluster}${d}"
    wait
done
# Sector2-Level6
dirs=$(find "${root}Sector2-Level6\2020-4-15-19-26-9${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector2-Level6\2020-4-15-19-26-9${cluster}${d}"
    wait
done

# Sector3-Level1
dirs=$(find "${root}Sector3-Level1\2020-4-15-19-34-17${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector3-Level1\2020-4-15-19-34-17${cluster}${d}"
    wait
done
# Sector3-Level2
dirs=$(find "${root}Sector3-Level2\2020-4-15-19-36-34${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector3-Level2\2020-4-15-19-36-34${cluster}${d}"
    wait
done
# Sector3-Level3
dirs=$(find "${root}Sector3-Level3\2020-4-15-19-40-16${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector3-Level3\2020-4-15-19-40-16${cluster}${d}"
    wait
done
# Sector3-Level6
dirs=$(find "${root}Sector3-Level6\2020-4-15-21-54-23${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector3-Level6\2020-4-15-21-54-23${cluster}${d}"
    wait
done

# Sector4-Level2
dirs=$(find "${root}Sector4-Level2\2020-4-15-22-2-43${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector4-Level2\2020-4-15-22-2-43${cluster}${d}"
    wait
done
# Sector4-Level3
dirs=$(find "${root}Sector4-Level3\2020-4-16-13-14-55${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector4-Level3\2020-4-16-13-14-55${cluster}${d}"
    wait
done
# Sector4-Level4
dirs=$(find "${root}Sector4-Level4\2020-4-15-22-20-27${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector4-Level4\2020-4-15-22-20-27${cluster}${d}"
    wait
done
# Sector4-Level6
dirs=$(find "${root}Sector4-Level6\2020-4-15-22-22-51${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
for d in ${dirs[@]}; do
    echo "$d"
    py dupFinder.py -d CodeHunt -ec "${root}Sector4-Level6\2020-4-15-22-22-51${cluster}${d}"
    wait
done

# Sector 9 (Algorithms)
# dirs=$(find "${root}Sector9-Level1\2020-4-5-0-11-52(implication,all_concrete)${cluster}" -maxdepth 1 -mindepth 1 -type d | cut -c 116-)
# for d in ${dirs[@]}; do
#     echo "$d"
#     py dupFinder.py -d CodeHunt -ec "${root}Sector9-Level1\2020-4-5-0-11-52(implication,all_concrete)${cluster}${d}"
#     wait
# done