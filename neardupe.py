if __name__ == "__main__":
    import os
    import re
    import shutil
    import argparse
    import subprocess
    from pathlib import Path
    from config import *

    # Config
    root = r'C:\Users\rayjo\Documents\GitHub\Near-Duplicate-Code-Detector'
    tokenizerDir = root + r'\tokenizers\CsharpTokenizer'
    tokenizerDll = tokenizerDir + \
        r'\CsharpTokenizer\bin\Debug\netcoreapp2.1\CsharpTokenizer.dll'
    dupeDetectorDir = root + r'\DuplicateCodeDetector'
    dupeDetectorProj = dupeDetectorDir + r'\DuplicateCodeDetector.csproj'

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir', type=str, help='Root directory of where evaluation subjects reside')
    parser.add_argument('-b', '--build', action='store_true',
                        help='Build tokenizer and DuplicateCodeDetector C# projects')
    parser.add_argument('-st', '--student', action='store_true',
                        help='Evaluate only one subject (student)')
    parser.add_argument('-ec', '--eqclass', action='store_true',
                        help='Evaluate only on subjects within an equivalence class that our tool produces')
    parser.add_argument('-su', '--subset', action='store_true',
                        help='Evaluate only a subset of subjects (students)')
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to run dupFinder on: CodeHunt, Pex4Fun, or PKU")
    parser.add_argument(
        "-a", "--algorithm", help="Run dupFinder on one algorithm at a time (optional)", action="store_true")

    args = parser.parse_args()

    # Error checking
    if not args.dataset:
        print('Specify the dataset you wish to evaluate')
        exit(1)
    if all((args.student, args.subset)):
        print('Conflict option!', '-su', '-st')
        exit(1)

    src_dir = args.dir

    # Build the projects
    if args.build:
        subprocess.call(['msbuild', tokenizerDir])
        subprocess.call(['msbuild', dupeDetectorDir])

    if args.dataset == 'CodeHunt':
        puzzle_CH = re.search('Sector\d-Level\d', src_dir).group(0)
        if args.algorithm:
            puzzle_CH += '/' + re.search('\w+Sorter', src_dir).group(0)
            algo_name = re.search('\w+Sorter', src_dir).group(0)
    elif args.dataset == 'Pex4Fun':
        puzzle_CH = src_dir[src_dir.find('Pex4Fun')+8:]
        puzzle_CH = puzzle_CH[:puzzle_CH.find('\\')]
    elif args.dataset == 'PKU':
        puzzle_CH = re.search('hw\d', src_dir).group(0)
    # Get relative name of dir
    dir = src_dir[::-1]
    dir = dir[: dir.find('\\')][::-1]

################## One subject below ##################
if args.student or args.eqclass or args.algorithm:
    # CodeHunt dataset
    if args.dataset == 'CodeHunt':
        # Create 'jsonl/[dir]/clusters' directory
        if args.eqclass:
            jsonlFiles = root + '/jsonl/' + args.dataset + '/single/' + puzzle_CH + '/' + dir
        elif args.algorithm:
            jsonlFiles = root + '/jsonl/' + args.dataset + '/single/' + puzzle_CH + '/' + dir
        else:
            jsonlFiles = root + '/jsonl/' + args.dataset + '/single/' + dir
        clustersDir = jsonlFiles + '/clusters'
        if args.algorithm:
            clustersDir += '/' + algo_name
        if not os.path.exists(clustersDir):
            os.makedirs(clustersDir)
        # Tokenize student's files
        subprocess.call(['dotnet', tokenizerDll, src_dir, jsonlFiles, 'false'])
        # Change curr working dir and call Dupe Detector on tokenized files
        os.chdir(clustersDir)
        if args.algorithm:
            subprocess.call(['dotnet', 'run', '--project',
                             dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
        else:
            subprocess.call(['dotnet', 'run', '--project',
                             dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
        exit(1)

    # Pex4Fun dataset
    if args.dataset == 'Pex4Fun':
         # Create 'jsonl/[dir]/clusters' directory
        if args.eqclass:
            jsonlFiles = root + '/jsonl/' + args.dataset + '/single/' + puzzle_CH + '/' + dir
            # Create cluster dir
            clustersDir = jsonlFiles + '/clusters/'
            if not os.path.exists(clustersDir):
                os.makedirs(clustersDir)
            # Tokenize student's files
            subprocess.call(
                ['dotnet', tokenizerDll, src_dir, jsonlFiles, 'false'])
        else:
            jsonlFiles = root + '/jsonl/' + args.dataset + '/single/' + dir
            winningDir = src_dir + '/winning'
            if not os.path.exists(winningDir):
                os.makedirs(winningDir)

            clustersDir = jsonlFiles + '/clusters/'
            if not os.path.exists(clustersDir):
                os.makedirs(clustersDir)
            winning = [x for x in os.listdir(src_dir) if 'win-' in x]
            # Copy 'win-X.cs' file into temp folder so tokenizer can run on it (if file exists)
            if winning:
                shutil.copy(src_dir + '/' +
                            winning[0], winningDir + '/' + winning[0])
            # Copy file to temp folder and prepend w/ 'win-'
            elif len(os.listdir(src_dir)) > 2:
                winning = [x for x in os.listdir(src_dir) if x.endswith('.cs')]
                shutil.copy(src_dir + '/' +
                            winning[-1], winningDir + '/win-' + winning[-1])
                os.rename(src_dir + '/' + winning[-1],
                          src_dir + '/win-' + winning[-1])
            # Tokenize student's files
            subprocess.call(
                ['dotnet', tokenizerDll, winningDir, jsonlFiles, 'false'])
            # Delete temp 'winning' directory
            shutil.rmtree(winningDir, ignore_errors=True)

        # Change curr working dir and call Dupe Detector on tokenized files
        os.chdir(clustersDir)
        subprocess.call(['dotnet', 'run', '--project',
                         dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
        exit(1)

     # PKU dataset
    if args.dataset == 'PKU':
        jsonlFiles = root + '/jsonl/PKU/single/' + puzzle_CH + '/' + dir
        clustersDir = jsonlFiles + '/clusters/'
        winningDir = src_dir + '/winning'
        if not os.path.exists(clustersDir):
            os.makedirs(clustersDir)
        if not os.path.exists(winningDir):
            os.makedirs(winningDir)

        # Copy all passing files into temp folder so tokenizer can run on them
        winning = [x for x in os.listdir(src_dir) if '_Passed' in x]
        if winning:
            for sub in winning:
                shutil.copy(src_dir + '/' + sub, winningDir + '/' + sub)
        # Tokenize student's files
        subprocess.call(
            ['dotnet', tokenizerDll, winningDir, jsonlFiles, 'false'])
        # Delete temp 'winning' directory
        shutil.rmtree(winningDir, ignore_errors=True)
        # Change curr working dir and call Dupe Detector on tokenized files
        os.chdir(clustersDir)
        subprocess.call(['dotnet', 'run', '--project',
                         dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
        exit(1)


################## Subset of subjects below ##################
if args.subset:
    # CodeHunt dataset
    if args.dataset == 'CodeHunt':
        if args.eqclass:
            jsonlFiles = root + '/jsonl/CodeHunt/subset/' + puzzle_CH
        else:
            jsonlFiles = root + '/jsonl/CodeHunt/subset/' + dir
        clustersDir = jsonlFiles + '/clusters'
        if not os.path.exists(clustersDir):
            os.makedirs(clustersDir)
        # Tokenize student's files
        subprocess.call(['dotnet', tokenizerDll, src_dir, jsonlFiles, 'false'])
        # Change curr working dir and call Dupe Detector on tokenized files
        os.chdir(clustersDir)
        subprocess.call(['dotnet', 'run', '--project',
                         dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
        exit(1)

    # Pex4Fun dataset
    if args.dataset == 'Pex4Fun':
        jsonlFiles = root + '/jsonl/Pex4Fun/subset/' + dir
        clustersDir = jsonlFiles + '/clusters/'
        winningDir = src_dir + '/winning'
        if not os.path.exists(clustersDir):
            os.makedirs(clustersDir)
        if not os.path.exists(winningDir):
            os.makedirs(winningDir)

        nEligible = 0
        # Get all winning files and put them in src_dir/winning
        for student in os.listdir(src_dir):
            if not os.path.isdir(src_dir + '/' + student):
                continue
            # If student is ineligible (i.e., didn't answer this puzzle correctly)...
            if ELIGIBLE_DICT.get(int(dir)) and student not in ELIGIBLE_DICT[int(dir)]:
                # print(student, ' didn\'t answer this puzzle correctly. Ineligible')
                continue
            nEligible += 1

            winning = [x for x in os.listdir(
                src_dir + '/' + student) if 'win-' in x]
            # Copy 'win-X.cs' file into temp folder so tokenizer can run on it (if file exists)
            if winning:
                shutil.copy(os.path.join(src_dir, student,
                                         winning[0]), winningDir + '/' + winning[0])
            # Copy file to temp folder and prepend w/ 'win-'
            elif len(os.listdir(src_dir + '/' + student)) > 2:
                winning = [x for x in os.listdir(
                    src_dir + '/' + student) if x.endswith('.cs')]
                shutil.copy(os.path.join(src_dir, student,
                                         winning[-1]), winningDir + '/win-' + winning[-1])
                os.rename(src_dir + '/' + winning[-1],
                          src_dir + '/win-' + winning[-1])

        # Tokenize student's files
        if nEligible >= 2:
            subprocess.call(
                ['dotnet', tokenizerDll, winningDir, jsonlFiles, 'false'])
            # Delete temp 'winning' directory
            shutil.rmtree(winningDir, ignore_errors=True)

        if nEligible >= 2:
            # Change curr working dir and call Dupe Detector on tokenized files
            os.chdir(clustersDir)
            subprocess.call(['dotnet', 'run', '--project',
                             dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
        exit(1)

    # PKU dataset
    if args.dataset == 'PKU':
        jsonlFiles = root + '/jsonl/PKU/subset/' + dir
        clustersDir = jsonlFiles + '/clusters/'
        winningDir = src_dir + '/winning'
        if not os.path.exists(clustersDir):
            os.makedirs(clustersDir)
        if not os.path.exists(winningDir):
            os.makedirs(winningDir)

        # Get all winning files and put them in src_dir/winning
        for student in os.listdir(src_dir):
            if not os.path.isdir(src_dir + '/' + student):
                continue

            # Copy all passing files into temp folder so tokenizer can run on them
            winning = [x for x in os.listdir(
                src_dir + '/' + student) if '_Passed' in x]
            if winning:
                for sub in winning:
                    shutil.copy(os.path.join(src_dir, student, sub),
                                winningDir + '/' + student + '_' + sub)

        # Tokenize student's files
        subprocess.call(
            ['dotnet', tokenizerDll, winningDir, jsonlFiles, 'false'])
        # Delete temp 'winning' directory
        shutil.rmtree(winningDir, ignore_errors=True)

        # Change curr working dir and call Dupe Detector on tokenized files
        os.chdir(clustersDir)
        subprocess.call(['dotnet', 'run', '--project',
                         dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
        exit(1)


################## All subjects below ##################

# CodeHunt dataset
if args.dataset == 'CodeHunt':
    for puzzle in os.listdir(src_dir):
        if not os.path.isdir(src_dir + '/' + puzzle) and 'win-' not in puzzle:
            continue
        jsonlFiles = root + '/jsonl/CodeHunt/full_dataset/' + puzzle
        clustersDir = jsonlFiles + '/clusters'
        if not os.path.exists(clustersDir):
            os.makedirs(clustersDir)
        # Tokenize student's files
        subprocess.call(['dotnet', tokenizerDll, src_dir +
                         '/' + puzzle, jsonlFiles, 'false'])
        # Change curr working dir and call Dupe Detector on tokenized files
        os.chdir(clustersDir)
        subprocess.call(['dotnet', 'run', '--project',
                         dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + puzzle])
    exit(1)

# Pex4Fun dataset
if args.dataset == 'Pex4Fun':
    jsonlFiles = root + '/jsonl/Pex4Fun/full_dataset'
    clustersDir = jsonlFiles + '/clusters/'
    if not os.path.exists(clustersDir):
        os.makedirs(clustersDir)

    nEligible = 0
    # For every puzzle
    for dir in os.listdir(src_dir):
        if not os.path.isdir(src_dir + '/' + dir):
            continue
        # Create temp winning dir
        winningDir = src_dir + '/winning'
        if not os.path.exists(winningDir):
            os.makedirs(winningDir)
        # Get all winning files and put them in src_dir/winning
        for student in os.listdir(src_dir + '/' + dir):
            if not os.path.isdir(os.path.join(src_dir, dir, student)):
                continue
            # If student is ineligible (i.e., didn't answer this puzzle correctly)...
            if ELIGIBLE_DICT.get(int(dir)) and student not in ELIGIBLE_DICT[int(dir)]:
                # print(student, ' didn\'t answer this puzzle correctly. Ineligible')
                continue
            nEligible += 1

            winning = [x for x in os.listdir(
                os.path.join(src_dir, dir, student)) if 'win-' in x]
            # Copy 'win-X.cs' file into temp folder so tokenizer can run on it (if file exists)
            if winning:
                shutil.copy(os.path.join(src_dir, dir, student,
                                         winning[0]), winningDir + '/' + student + '_' + winning[0])
            # Copy file to temp folder and prepend w/ 'win-'
            elif len(os.listdir(os.path.join(src_dir, dir, student))) > 2:
                winning = [x for x in os.listdir(os.path.join(
                    src_dir, dir, student)) if x.endswith('.cs')]
                shutil.copy(os.path.join(src_dir, dir, student,
                                         winning[-1]), winningDir + '/' + student + '_win-' + winning[-1])
                os.rename(os.path.join(src_dir, dir, student, winning[-1]), os.path.join(
                    src_dir, dir, student, 'win-' + winning[-1]))

        # Tokenize student's files
        if nEligible >= 2:
            subprocess.call(
                ['dotnet', tokenizerDll, winningDir, jsonlFiles, 'false'])
            # Delete temp 'winning' directory
            shutil.rmtree(winningDir, ignore_errors=True)

        if nEligible >= 2:
            # Change curr working dir and call Dupe Detector on tokenized files
            os.chdir(clustersDir)
            subprocess.call(['dotnet', 'run', '--project',
                             dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
    exit(1)


# PKU dataset
if args.dataset == 'PKU':
    jsonlFiles = root + '/jsonl/PKU/full_dataset'
    clustersDir = jsonlFiles + '/clusters/'
    if not os.path.exists(clustersDir):
        os.makedirs(clustersDir)

    nEligible = 0
    # For every puzzle
    for dir in os.listdir(src_dir):
        if not os.path.isdir(src_dir + '/' + dir):
            continue
        # Create temp winning dir
        winningDir = src_dir + '/winning'
        if not os.path.exists(winningDir):
            os.makedirs(winningDir)
        # Get all winning files and put them in src_dir/winning
        for student in os.listdir(src_dir + '/' + dir):
            if not os.path.isdir(os.path.join(src_dir, dir, student)):
                continue
            # Copy all passing files into temp folder so tokenizer can run on them
            winning = [x for x in os.listdir(os.path.join(
                src_dir, dir, student)) if '_Passed' in x]
            if winning:
                for sub in winning:
                    shutil.copy(os.path.join(src_dir, dir, student, sub),
                                winningDir + '/' + student + '_' + sub)

        # Tokenize student's files
        subprocess.call(
            ['dotnet', tokenizerDll, winningDir, jsonlFiles, 'false'])
        # Delete temp 'winning' directory
        shutil.rmtree(winningDir, ignore_errors=True)

        # Change curr working dir and call Dupe Detector on tokenized files
        os.chdir(clustersDir)
        subprocess.call(['dotnet', 'run', '--project',
                         dupeDetectorProj, '--dir=' + jsonlFiles, 'res_' + dir])
    exit(1)
