import random

# Return body of Main method


def fill_main(sector, level):
    if sector == '1' and level == '4':
        # two integers
        return ['\t\tPuzzle(Int32.Parse(args[0]), Int32.Parse(args[1]));\n']
    if sector == '2' and level == '1':
        # int array
        ret = []
        ret.append(
            '\t\tstring[] tmp = args[0].Replace("[", "").Replace("]","").Split(\',\');\n')
        ret.append('\t\tPuzzle(Array.ConvertAll(tmp, int.Parse));\n')
        return ret
    if sector == '2' and level == '5':
        # int array
        ret = []
        ret.append(
            '\t\tstring[] tmp = args[0].Replace("[", "").Replace("]","").Split(\',\');\n')
        ret.append('\t\tPuzzle(Array.ConvertAll(tmp, int.Parse));\n')
        return ret
    if sector == '3' and level == '1':
        # int array, integer
        ret = []
        ret.append(
            '\t\tstring[] tmp = args[0].Replace("[", "").Replace("]","").Split(\',\');\n')
        ret.append(
            '\t\tPuzzle(Array.ConvertAll(tmp, int.Parse), Int32.Parse(args[1]));\n')
        return ret
    if sector == '3' and level == '2':
        # one integer
        return ['\t\tPuzzle(Int32.Parse(args[0]));\n']


# Return randomly generated LARGE input for the five puzzles
def input_generator(sector, level):
    if sector == '1' and level == '4':
        # two integers
        return [random.randint(5000, 100000), random.randint(5000, 100000)]
    if sector == '2' and level == '1':
        # int array
        arr, arrLen = [], random.randint(500, 1000)
        for x in range(arrLen):
            arr.append(random.randint(5000, 100000))
        return [arr]
    if sector == '2' and level == '5':
        # int array
        arr, arrLen = [], random.randint(500, 1000)
        for x in range(arrLen):
            arr.append(random.randint(5000, 100000))
        return [arr]
    if sector == '3' and level == '1':
        # int array, integer
        arr, arrLen = [], random.randint(500, 1000)
        for x in range(arrLen):
            arr.append(random.randint(5000, 100000))
        return [arr, random.randint(5000, 100000)]
    if sector == '3' and level == '2':
        # one integer (decreased range to avoid stack overflow)
        return [random.randint(20, 45)]


# Cluster submissisons by square sums
def cluster(sector, level, squareSumDict):
    # if sector == '1' and level == '4':

    # if sector == '2' and level == '1':
    # if sector == '2' and level == '5':
    # if sector == '3' and level == '1':
    if sector == '3' and level == '2':
        # Separate recursive subs from iterative ones
        for sub in squareSumDict:
            if squareSumDict[sub] < 10:
                # Put into cluster 0 (iterative)
                # else:
                # Put into cluster 1 (recursive)


if __name__ == "__main__":
    from timeit import default_timer as timer
    from datetime import datetime, timedelta
    from collections import defaultdict
    from config import *
    import subprocess
    import argparse
    import json
    import os
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("sector", type=str, help="Sector")
    parser.add_argument("level", type=str, help="Level")
    parser.add_argument("data_dir", type=str,
                        help="Path to filtered submissions")
    args = parser.parse_args()
    # Example of how to run:
    #   py .\runtime_logger.py 2 5 win-2-5    <-- Sector 2 level 5, folder win-2-5

    # Initialize vars and folders
    runtimeDict = defaultdict(list)
    dt_now = datetime.now()
    output_dir = RUNTIME_RESULTS / 'Sector{}-Level{}'.format(args.sector, args.level) / '{}-{}-{}-{}-{}-{}'.format(
        dt_now.year, dt_now.month, dt_now.day, dt_now.hour, dt_now.minute, dt_now.second)
    # checkers
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Compile each submission and generate their .exe files
    for student in os.listdir(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir)):
        for sub in os.listdir(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) / student):
            if not sub.endswith('.cs') or 'COMPILED' in sub:
                continue
            compiledSub = 'COMPILED-' + sub
            # Read all lines of each submission
            with open(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) / student / sub, 'r') as f:
                contents = f.readlines()
            # Add Main method to submission
            with open(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) / student / compiledSub, 'w') as f:
                    # Write this so I can use 'Array.ConvertAll()'. Duplicate 'using' statements don't matter.
                f.write('using System;')
                for line in contents:
                    # Inject main method
                    if 'public class Program' in line:
                        f.write(line)
                        f.write(
                            '\tpublic static void Main(string[] args) {\n')
                        f.writelines(fill_main(args.sector, args.level))
                        f.write('\t}\n')
                        continue
                    f.write(line)
            # Try to compile, next iteration if fails to compile
            try:
                # '-out:' specifies the output .exe file location
                subprocess.check_output(
                    ['csc', '-out:' + str(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) / student / compiledSub.replace('.cs', '.exe')), str(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) / student / compiledSub)], stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print('{} failed to compile'.format(compiledSub))
                continue

    # Run and time each submission. Record 20 data points per submission.
    for x in range(20):
        # Get randomly generated input for puzzle type
        randInput = input_generator(args.sector, args.level)
        for student in os.listdir(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir)):
            for sub in os.listdir(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) / student):
                if sub.endswith('.exe'):
                    # Run the compilable submission and time it
                    start = timer()
                    try:
                        subprocess.call([str(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) / student / sub), str(
                            randInput[0]), str(randInput[1]) if len(randInput) > 1 else ''], shell=True)
                    except FileNotFoundError:
                        print(sub, ' not found in ', student)
                    end = timer()
                    runtimeDict[sub].append(end - start)

    # Write all runtimes to text file
    with open(output_dir / 'Runtimes.txt', 'w') as f:
        f.write(json.dumps(runtimeDict))

    # Write all square sums to text file
    squareSumDict = dict()
    for sub in runtimeDict:
        squareSumDict[sub] = sum(i*i for i in runtimeDict[sub])
    with open(output_dir / 'Square Sums.txt', 'w') as f:
        f.write(json.dumps(squareSumDict))

    # Remove the modified sub.cs and its compiled .exe
    for student in os.listdir(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir)):
        for sub in os.listdir(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) / student):
            if 'COMPILED' not in sub:
                continue
            try:
                os.remove(CODEHUNT_OUTPUT_ROOT / Path(args.data_dir) /
                          student / sub)
                os.remove(CODEHUNT_OUTPUT_ROOT /
                          Path(args.data_dir) / student / sub)
            except OSError:
                pass

    # Cluster submissions by square sum
    cluster(args.sector, args.level, squareSumDict)
