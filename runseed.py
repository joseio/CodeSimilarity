if __name__ == '__main__':
    import os
    import sys
    import subprocess
    import time
    import argparse
    import shutil
    import datetime
    import subprocess
    import string
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from config import *
    from runpex import clean_finished, pex_runner_wrapper, pick_free, CSVSaver

    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--parallelism", type=int,
                        default=1, help="Run Pex in parallel")
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to run seeded tests for")
    parser.add_argument("sector", type=str, help="Sector number")
    parser.add_argument("level", nargs='?', type=str,
                        help="Level number", default='')

    args = parser.parse_args()

    if not args.level and not args.dataset:
        print('Enter sector and level.')
        exit(1)

    # Assign values
    sector = args.sector
    level = args.level
    parallelism = args.parallelism

    # Local vars
    if args.dataset == 'Pex4Fun':
        input_dir = CODEHUNT_OUTPUT_ROOT / args.dataset / sector
        template_PUT = PEX_PUT_TEMPLATE / args.dataset / '{}.cs'.format(sector)
        vnames = VARNAME_SWITCH['p4f-{}'.format(sector)]
    elif args.dataset == 'PKU':
        input_dir = CODEHUNT_OUTPUT_ROOT / args.dataset / sector
        template_PUT = PEX_PUT_TEMPLATE / args.dataset / '{}.cs'.format(sector)
        vnames = VARNAME_SWITCH['pku-{}'.format(sector)]
    else:
        input_dir = CODEHUNT_OUTPUT_ROOT / \
            Path('win-{}-{}'.format(sector, level))
        template_PUT = PEX_PUT_TEMPLATE / \
            'Sector{}-Level{}.cs'.format(sector, level)
        vnames = VARNAME_SWITCH['{}-{}'.format(sector, level)]

    parallelism = args.parallelism if args.parallelism > 1 else 1
    shutil.rmtree(PEX_TMP_ROOT, ignore_errors=True)
    instances = {PEX_TMP_ROOT /
                 str(tid): False for tid in range(parallelism)}

    # Setup instances
    for ins in instances:
        shutil.copytree(PEX_SOLUTION_TEMPLATE, ins)
        shutil.copy(template_PUT, ins /
                    PEX_TEST_PROJECT_NAME / PEX_TEST_FILENAME)

    # Example of how to run:
    #   py .\runseed.py 2 5 win-2-5     <-- Sector 2, level 5 (winning only)
    #   py .\runseed.py -j 4 2 5 win-2-5     <--Sector 2, level 5 (winning only) w/ 4 parallel threads

    # Get last modified folder in Results dir (newest result)
    if args.dataset == 'Pex4Fun':
        resultsDir = PEX_OUTPUT_ROOT / Path('Pex4Fun') / sector
    if args.dataset == 'PKU':
        resultsDir = PEX_OUTPUT_ROOT / Path('PKU') / sector
    else:
        resultsDir = PEX_OUTPUT_ROOT / 'Sector{}-Level{}'.format(sector, level)
    all_subdirs = [resultsDir / d for d in os.listdir(
        resultsDir) if os.path.isdir(resultsDir / d)]
    latest_subdir = resultsDir / max(all_subdirs, key=os.path.getmtime)
    unionDir = latest_subdir / UNION_CONCRETE_TESTS
    output_dir = latest_subdir / UNION_RESULTS
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    if not unionDir.exists():
        print('Cannot find ' + UNION_CONCRETE_TESTS)

    # Creating my own punctuation where I remove the '+' and '-' from string.punctuation
    punctuation = '!"#$%&\'()*,./:;<=>?@[\\]^_`{|}~'

    # Get all concrete tests, removing '\n'
    with open(unionDir, 'r') as f:
        concreteTests = f.read().splitlines()

    for test in concreteTests:
        objInit, input = '', ''

        # Build Similarity.sln after having edited ProgramTest.cs...I think runpex calls MSBuild already...
        # subprocess.call([DEVENV_EXE, '/build', 'Debug', PEX_SOLUTION_TEMPLATE / PEX_SOLUTION_NAME])

        # Run pex for each instance
        for ins in instances:
            # shutil.copytree(PEX_SOLUTION_TEMPLATE, ins)
            # shutil.copy(template_PUT, ins /
            #             PEX_TEST_PROJECT_NAME / PEX_TEST_FILENAME)

            # Replace ',' that is NOT inside {} w/ '@'
            lvl = 0
            mod_test = test[:]
            for x in range(len(mod_test)):
                if mod_test[x] == '{':
                    lvl += 1
                if mod_test[x] == '}':
                    lvl -= 1
                if lvl == 0 and mod_test[x] == ',':
                    mod_test = mod_test[:x] + '@' + mod_test[x+1:]
            split = mod_test.split('@')
            # Check if each arg is string/number
            for x in range(len(split)):
                noquotes = True
                arg = split[x]
                # Conv '{}' -> '[]' if PC is input array
                if arg and arg.strip()[0] == '{':
                    # Check if first letter after left brace is letter
                    if arg.strip()[1].isalpha() or arg.strip()[1] in punctuation:
                        objInit = 'new string[]'
                        arr_split = arg[1:-1].split(',')
                        # Add double quote to each arg
                        for i in range(len(arr_split)):
                            arr_split[i] = '"' + arr_split[i] + '"'
                        split[x] = '{' + ','.join(arr_split) + '}'
                        # split.insert(x, objInit)
                        split[x] = objInit + split[x]

                    else:
                        # Use double[] if decimal in arg, else int[]
                        objInit = 'new int[]' if '.' not in arg else 'new double[]'
                        # split.insert(x, objInit)
                        split[x] = objInit + split[x]

                # Surround string w/ double quotes
                elif noquotes and arg and (arg.strip()[0].isalpha() or arg.strip()[0] in punctuation):
                    noquotes = False  # Don't add dobule quotes more than 1x
                    split[x] = '"' + arg.strip() + '"'

            mod_test = ','.join(split)

            with open(ins / PEX_TEST_PROJECT_NAME / PEX_TEST_FILENAME, 'r+') as f:
                print(ins / PEX_TEST_PROJECT_NAME / PEX_TEST_FILENAME)
                txt = f.read().splitlines()
                for x in range(len(txt)):
                    # Add `[PexClass(MaxRuns = 1)]`
                    if 'PexClass' in txt[x]:
                        if args.dataset == 'PKU':
                            txt[x] = '[PexClass(typeof(global::GlobalMembers), MaxRuns = 1, MaxConditions = 5000)]'
                        else:
                            txt[x] = '[PexClass(typeof(global::Program), MaxRuns = 1, MaxConditions = 5000)]'
                    # Add `[PexArguments()]` to the right of `[PexMethod]` in ProgramTest.cs
                    if '[PexMethod' in txt[x]:
                        # Add'l formatting required if two int array inputs
                        twoArrs = mod_test.split('},  {', 1)
                        if len(twoArrs) > 1:
                            # txt[x] = '\t[PexMethod(MaxBranches = 100000, MaxConditions = 4000)] ' + '[PexArguments(' + objInit + ' ' + twoArrs[0] + '}, ' + objInit + ' {' + twoArrs[1] + ')]'
                            txt[x] = '\t[PexMethod(MaxBranches = 100000, MaxConditions = 4000)] ' + \
                                '[PexArguments(' + mod_test + ')]'
                        else:
                            # txt[x] = '\t[PexMethod(MaxBranches = 100000, MaxConditions = 4000)] ' + '[PexArguments(' + objInit + ' ' + mod_test + ')]'
                            txt[x] = '\t[PexMethod(MaxBranches = 100000, MaxConditions = 4000)] ' + \
                                '[PexArguments(' + mod_test + ')]'
                        # Point to beginning, clear, then re-write file contents
                        f.seek(0)
                        f.truncate(0)
                        f.writelines('\n'.join(txt))
                        break
        if os.path.exists(output_dir / 'Solution'):
            shutil.rmtree(output_dir / 'Solution')
        shutil.copytree(next(iter(instances)), output_dir / 'Solution')

        if args.parallelism > 1:
            thread_pool = ThreadPoolExecutor(max_workers=args.parallelism)

        # Main part
        # Strip illegal chars for Windows folder name
        mod_test = mod_test.translate(str.maketrans(
            {'\\': '[backslash]', '/': '[forwardslash]', ':': '[colon]', '*': '[asterisk]', '?': '[question]', '"': '[dquote]', '<': '[larrow]', '>': '[rarrow]', '|': '[pipe]'}))
        total_cnt = len([1 for root, dirs, files in os.walk(input_dir)
                         for f in files if f.endswith('.cs')])
        csv_wrapper = CSVSaver(
            output_dir / 'Input({})'.format(mod_test) / PEX_OUTPUT_NAME)
        counter = 0
        submitted = dict()
        for user_dir in input_dir.iterdir():
            user = user_dir.name
            for i, cs_path in enumerate(user_dir.iterdir(), start=1):
                counter += 1
                file = cs_path.name
                des_path = output_dir / \
                    'Input({})'.format(mod_test) / '{}-Try{}'.format(user, i)
                if args.parallelism > 1:
                    while True:
                        worker = pick_free(instances)
                        if worker:
                            break
                        else:
                            clean_finished(submitted, instances, csv_wrapper)
                            time.sleep(1)
                    cwd = worker
                    s = thread_pool.submit(
                        pex_runner_wrapper, cwd, cs_path, des_path, vnames, user, i, file, counter, total_cnt)
                    submitted[s] = cwd
                    instances[cwd] = True
                else:
                    cwd = next(iter(instances))
                    csv_wrapper.write_rows(pex_runner_wrapper(
                        cwd, cs_path, des_path, vnames, user, i, file, counter, total_cnt))

        if parallelism > 1:
            clean_finished(submitted, instances, csv_wrapper)
            thread_pool.shutdown()
