if __name__ == "__main__":
    import re
    import os
    import shutil
    import argparse
    import subprocess
    from pathlib import Path
    from config import *

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir', type=str, help='Root directory of where evaluation subjects reside')
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
    if (args.student and args.subset) or (args.student and args.eqclass) or (args.subset and args.eqclass):
        print('Conflict option!', '-st', '-ec', '-su')
        exit(1)

    src_dir = args.dir

    dest_dir = r'C:\Users\rayjo\Documents\dupFinder_Results'
    if args.eqclass:
        if args.dataset == 'CodeHunt':
            puzzle_CH = re.search('Sector\d-Level\d', src_dir).group(0)
        elif args.dataset == 'Pex4Fun':
            puzzle_CH = src_dir[src_dir.find('Pex4Fun')+8:]
            puzzle_CH = puzzle_CH[:puzzle_CH.find('\\')]
        elif args.dataset == 'PKU':
            puzzle_CH = re.search('hw\d', src_dir).group(0)
    if args.algorithm:
        if args.dataset == 'CodeHunt':
            puzzle_CH = re.search('Sector\d-Level\d', src_dir).group(0) + \
                '/' + re.search('\w+Sorter',
                                src_dir).group(0)

    # Get relative name of dir
    dir = src_dir[::-1]
    dir = dir[: dir.find('\\')][::-1]

################## One subject below ##################

    # If only evaluating one algorithm at a time in algorithms dataset
    if args.algorithm:
        if args.dataset == 'CodeHunt':
            if not os.path.exists(dest_dir + '/' + args.dataset + '/single/' + puzzle_CH):
                os.makedirs(dest_dir + '/' + args.dataset +
                            '/single/' + puzzle_CH)
            # Run if file doesn't already exist
            if not os.path.exists(dest_dir + '/' + args.dataset + '/single/' + puzzle_CH + '/res_' + dir + '.xml'):
                subprocess.call(['dupfinder', '--show-text', src_dir +
                                 '/**/*.cs', '-o=' + dest_dir + '/' + args.dataset + '/single/' + puzzle_CH + '/res_' + dir + '.xml'], shell=True)

    # If I'm only evaluating one subject (e.g., win-2-1/User000 or apcs/33/Student1)
    if args.student or args.eqclass:
         # CodeHunt dataset
        if args.dataset == 'CodeHunt':
            if args.eqclass:
                if not os.path.exists(dest_dir + '/' + args.dataset + '/single/' + puzzle_CH):
                    os.makedirs(dest_dir + '/' + args.dataset +
                                '/single/' + puzzle_CH)
                subprocess.call(['dupfinder', '--show-text', src_dir +
                                 '/**/*.cs', '-o=' + dest_dir + '/' + args.dataset + '/single/' + puzzle_CH + '/res_' + dir + '.xml'], shell=True)

            elif args.student:
                # Create dest dir if doesn't exist already
                if not os.path.exists(dest_dir + '/' + args.dataset + '/single/' + puzzle_CH):
                    os.makedirs(dest_dir + '/' + args.dataset +
                                '/single/' + puzzle_CH)
                # Call JetBrain's dupFinder tool on this one dir in CodeHunt's dataset
                subprocess.call(['dupfinder', '--show-text', src_dir +
                                 '/**/*.cs', '-o=' + dest_dir + '/' + args.dataset + '/single/' + puzzle_CH + 'res_' + dir + '.xml'], shell=True)
            exit(1)

        # Pex4Fun dataset
        if args.dataset == 'Pex4Fun':
            if args.eqclass:
                if not os.path.exists(dest_dir + '/' + args.dataset + '/single/' + puzzle_CH):
                    os.makedirs(dest_dir + '/' + args.dataset +
                                '/single/' + puzzle_CH)
                subprocess.call(['dupfinder', '--show-text', src_dir +
                                 '/**/*.cs', '-o=' + dest_dir + '/' + args.dataset + '/single/' + puzzle_CH + '/res_' + dir + '.xml'], shell=True)
                exit(1)

            # Create dest dir if doesn't exist already
            if not os.path.exists(dest_dir + '/' + args.dataset + '/single'):
                os.makedirs(dest_dir + '/' + args.dataset + '/single')

            # Find solution.cs or win-solution.cs one folder up
            parent = os.listdir(os.path.join(src_dir, '..'))
            if 'solution.cs' or 'win-solution.cs' in parent:
                # Prepend 'win-' to last .cs file, if not already done
                sortedSubs = sorted(os.listdir(src_dir), key=lambda f: int(
                    re.sub('\D', '', f)) if '.cs' in f else False)
                oldName = sortedSubs[-1]
                newName = 'win-' + oldName if 'win-' not in oldName else oldName
                os.rename(os.path.join(src_dir, oldName),
                          os.path.join(src_dir, newName))

                # Temporarily copy solution file to student dir
                solnSrc = os.path.join(src_dir, '..', parent[-1])
                solnDest = os.path.join(src_dir, parent[-1])
                shutil.copyfile(solnSrc, solnDest)
                subprocess.call(['dupfinder', '--show-text', src_dir + '/**/win-*.cs',
                                 '-o=' + dest_dir + '/' + args.dataset + '/single/' + puzzle_CH + '/res_' + dir + '.xml'], shell=True)
                # Delete solution file from student dir
                if os.path.exists(src_dir + '/' + parent[-1]):
                    os.remove(src_dir + '/' + parent[-1])
            exit(1)

        # PKU dataset
        if args.dataset == 'PKU':
            # Create dest dir if doesn't exist already
            if not os.path.exists(dest_dir + '/' + args.dataset + '/single'):
                os.makedirs(dest_dir + '/' + args.dataset + '/single')
            subprocess.call(['dupfinder', '--show-text', src_dir +
                             '/**/*_Passed.cs', '-o=' + dest_dir + '/' + args.dataset + '/single/' + puzzle_CH + '/res_' + dir + '.xml'], shell=True)
            exit(1)

################## Subset of subjects below ##################

    # If I'm only evaluating a subset of subjects (e.g., win-2-1 or apcs/33)...
    if args.subset:
        # CodeHunt dataset
        if args.dataset == 'CodeHunt':
            # Create dest dir if doesn't exist already, run if in equivalence class mode
            if args.eqclass:
                if not os.path.exists(dest_dir + '/' + args.dataset + '/subset/' + puzzle_CH):
                    os.makedirs(dest_dir + '/' + args.dataset +
                                '/subset/' + puzzle_CH)
                subprocess.call(['dupfinder', '--show-text', src_dir +
                                 '//**/*.cs', '-o=' + dest_dir + '/' + args.dataset + '/subset/res_' + dir + '.xml'], shell=True)
            # Run if in subset mode
            elif args.subset:
                if not os.path.exists(dest_dir + '/' + args.dataset + '/subset'):
                    os.makedirs(dest_dir + '/' + args.dataset + '/subset')
                subprocess.call(['dupfinder', '--show-text', src_dir +
                                 '//**/*.cs', '-o=' + dest_dir + '/' + args.dataset + '/subset/res_' + dir + '.xml'], shell=True)
            exit(1)

        # Pex4Fun dataset
        if args.dataset == 'Pex4Fun':
            # Create dest dir if doesn't exist already
            if not os.path.exists(dest_dir + args.dataset + '/subset'):
                os.makedirs(dest_dir + '/' + args.dataset + '/subset')
            nEligible = 0
            for student in os.listdir(src_dir):
                if not os.path.isdir(src_dir + '/' + student):
                    continue
                # If student is ineligible (i.e., didn't answer this puzzle correctly)...
                if ELIGIBLE_DICT.get(int(dir)) and student not in ELIGIBLE_DICT[int(dir)]:
                    # print(student, ' didn\'t answer this puzzle correctly. Ineligible')
                    continue
                nEligible += 1
                # Prepend 'win-' to solution.cs. Else skip.
                if not os.path.isdir(src_dir + '/' + student):
                    if 'solution.cs' in student:
                        # Don't rename if solution already has 'win-' prepended to it
                        if 'win-' not in student:
                            os.rename(src_dir + '/' + student,
                                      src_dir + '/win-' + student)
                    continue
                try:
                    # Prepend 'win-' to last .cs file
                    sortedSubs = sorted(os.listdir(
                        src_dir + '/' + student), key=lambda f: int(re.sub('\D', '', f)) if '.cs' in f else False)
                    oldName = sortedSubs[-1]
                    # Skip if second to last is not C# file
                    if not oldName.endswith('.cs'):
                        continue
                    newName = 'win-' + oldName if 'win-' not in oldName else oldName
                    os.rename(os.path.join(src_dir, student, oldName),
                              os.path.join(src_dir, student, newName))
                except IndexError:
                    continue

            if nEligible >= 2:
                # Get relative name of dir (for CodeHunt)
                subprocess.call(['dupfinder', '--show-text', src_dir + '//**/win-*.cs',
                                 '-o=' + dest_dir + '/' + args.dataset + '/subset/res_' + dir + '.xml'], shell=True)
            exit(1)

        # PKU dataset
        if args.dataset == 'PKU':
            # Create dest dir if doesn't exist already
            if not os.path.exists(dest_dir + '/' + args.dataset + '/subset'):
                os.makedirs(dest_dir + '/' + args.dataset + '/subset')
            subprocess.call(['dupfinder', '--show-text', src_dir +
                             '//**/*_Passed.cs', '-o=' + dest_dir + '/' + args.dataset + '/subset/res_' + dir + '.xml'], shell=True)
            exit(1)

################## All subjects below ##################

    # Procedure for CodeHunt's full dataset
    if args.dataset == 'CodeHunt':
        # Create dest dir if doesn't exist already
        if not os.path.exists(dest_dir + '/' + args.dataset + '/full_dataset'):
            os.makedirs(dest_dir + '/' + args.dataset + '/full_dataset')
        # Loop through all sub-dirs if I'm evaluating ALL subjects in root dir
        for dir in os.listdir(src_dir):
            # Skip non-directories
            if not os.path.isdir(src_dir + '/' + dir):
                continue
                # Call JetBrain's dupFinder tool on this dir
            subprocess.call(['dupfinder', '--show-text', src_dir + '/' + dir + '//**/*.cs',
                             '-o=' + dest_dir + '/' + args.dataset + '/full_dataset/res_' + dir + '.xml'], shell=True)
        exit(1)

    # Procedure for Pex4Fun's full dataset
    if args.dataset == 'Pex4Fun':
        # Create dest dir if doesn't exist already
        if not os.path.exists(dest_dir + '/' + args.dataset + '/full_dataset'):
            os.makedirs(dest_dir + '/' + args.dataset + '/full_dataset')
        # Loop through all sub-dirs, labeling last submission as the winning one
        for dir in os.listdir(src_dir):
            if not os.path.isdir(src_dir + '/' + dir):
                continue
            nEligible = 0
            for student in os.listdir(src_dir + '/' + dir):
                # If student is ineligible (i.e., didn't answer this puzzle correctly)...
                if ELIGIBLE_DICT.get(int(dir)) and student not in ELIGIBLE_DICT[int(dir)]:
                    # print(student, ' didn\'t answer this puzzle correctly. Ineligible')
                    continue
                nEligible += 1
                # Prepend 'win-' to solution.cs. Else skip.
                if not os.path.isdir(os.path.join(src_dir, dir, student)):
                    if 'solution.cs' in student:
                        # Don't rename if solution already has 'win-' prepended to it
                        if 'win-' not in student:
                            os.rename(os.path.join(src_dir, dir, student),
                                      os.path.join(src_dir, dir, 'win-' + student))
                    continue
                try:
                    # Prepend 'win-' to second to last .cs file
                    sortedSubs = sorted(os.listdir(os.path.join(src_dir, dir, student)), key=lambda f: int(
                        re.sub('\D', '', f)) if '.cs' in f else False)
                    oldName = sortedSubs[-1]
                    # Skip if last file is not C# file
                    if not oldName.endswith('.cs'):
                        continue
                    newName = 'win-' + oldName if 'win-' not in oldName else oldName
                    os.rename(os.path.join(src_dir, dir, student, oldName),
                              os.path.join(src_dir, dir, student, newName))
                except IndexError:
                    continue

            # Call JetBrain's dupFinder tool on this dir if num students who answered puzzle correctly >= 2
            if nEligible >= 2:
                subprocess.call(['dupfinder', '--show-text', src_dir + '/' + dir + '//**/win-*.cs',
                                 '-o=' + dest_dir + '/' + args.dataset + '/full_dataset/res_' + dir + '.xml'], shell=True)
        exit(1)

    # PKU dataset
    if args.dataset == 'PKU':
        # Create dest dir if doesn't exist already
        if not os.path.exists(dest_dir + '/' + args.dataset + '/full_dataset'):
            os.makedirs(dest_dir + '/' + args.dataset + '/full_dataset')
        for dir in os.listdir(src_dir):
            # Skip non-directories
            if not os.path.isdir(src_dir + '/' + dir):
                continue
            subprocess.call(['dupfinder', '--show-text', src_dir + '/' + dir +
                             '//**/*_Passed.cs', '-o=' + dest_dir + '/' + args.dataset + '/full_dataset/res_' + dir + '.xml'], shell=True)
        exit(1)
