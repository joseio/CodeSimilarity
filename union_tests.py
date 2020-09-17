if __name__ == '__main__':
    import argparse
    import csv
    import random
    import os
    import re
    from config import *

    parser = argparse.ArgumentParser()
    parser.add_argument("sector", type=str, help="Sector number")
    parser.add_argument("level", nargs='?', type=str,
                        help="Level number", default='')
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to run get concrete tests for")
    parser.add_argument("-n", "--num_seeds", type=int,
                        default=-1, help="Specify the number of concrete inputs to log")
    args = parser.parse_args()

    if not args.level and not args.dataset:
        print('Enter sector and level.')
        exit(1)

    # assign values
    sector = args.sector
    level = args.level
    numSeeds = args.num_seeds

    # Example of how to run:
    #   py .\union_tests.py 2 5      <-- Sector 2, level 5

    # Get last modified folder in Results dir (newest result)
    if args.dataset == 'Pex4Fun':
        resultsDir = PEX_OUTPUT_ROOT / Path('Pex4Fun') / sector
    elif args.dataset == 'PKU':
        resultsDir = PEX_OUTPUT_ROOT / Path('PKU') / sector
    else:
        resultsDir = PEX_OUTPUT_ROOT / 'Sector{}-Level{}'.format(sector, level)
    all_subdirs = [resultsDir / d for d in os.listdir(
        resultsDir) if os.path.isdir(resultsDir / d)]
    latest_subdir = resultsDir / max(all_subdirs, key=os.path.getmtime)

    # Get concrete test inputs from results.csv
    testSet = set()
    with open(latest_subdir / PEX_OUTPUT_NAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # Find Path condition row
            if '{"' in row[0]:
                # Extract the concrete inputs
                input = row[0]
                input = input[input.find(':')+1: input.rfind('}')].strip(' "')
                # Account for multiple arguments (e.g., {"x": "0", "y": "1"})
                while ':' in input:
                    # Find position of second var in string (in form `"x":`)
                    secondVarPos = re.search(r"\"\w+\":", input).start()
                    # input = input[:input.find('"')+1] + \
                    input = input[:secondVarPos] + input[input.find(':')+1:]
                input = input.replace('"', '')
                # Delete 'Length=' that's prepended to some inputs
                if 'Length=' in input:
                    input = '{' + input[input.find(';') + 2:]
                testSet.add(input)

    # Write test set to new text file
    with open(latest_subdir / UNION_CONCRETE_TESTS, 'w') as txt_file:
        if numSeeds <= 0:
            numSeeds = len(testSet)
            for test in testSet:
                txt_file.write(test + '\n')
                print(test)
        else:
            list_testSet = list(testSet)
            # Randomly select `numSeeds` number of concrete tests
            for x in range(numSeeds):
                randTest = random.choice(list_testSet)
                txt_file.write(randTest + '\n')
                print(randTest)
    print('Added all tests to ' + str(latest_subdir / UNION_CONCRETE_TESTS))
