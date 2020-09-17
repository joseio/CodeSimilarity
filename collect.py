from distutils.dir_util import copy_tree
import subprocess
import shutil
import sys
import os


def sector_filter(src, des, sector, level, winning=True, failing=False):
    sec_name = "Sector{}-Level{}".format(sector, level)

    print('Source Root Directory:', src, file=sys.stderr)
    print('Destination Root Directory', des, file=sys.stderr)
    print('Correct submissions:', winning, '|',
          'Incorrect submissions:', failing, file=sys.stderr)

    for user_path in (x for x in src.iterdir() if x.is_dir()):
        user = user_path.name
        print('USER=', user)
        sec_dir = user_path / sec_name
        if sec_dir.exists():
            for src_file in sec_dir.iterdir():
                file = src_file.name
                print('FILE', file)
                des_dir = des / user
                des_file = des_dir / file
                # Only consider the C# files
                cp = src_file.suffix == '.cs' and ('winning' in file or not winning) and (
                    'winning' not in file or not failing)
                if cp:
                    des_dir.mkdir(parents=True, exist_ok=True)
                    print('Copying {} to {}'.format(src_file.relative_to(
                        src), des_file.relative_to(des)), file=sys.stderr)
                    shutil.copy(src_file, des_file)


# Not needed for now--don't invoke
def java_filter(src, des, sector, level):
    sec_name = "Sector{}-Level{}".format(sector, level)
    print('Source Root Directory:', src)
    print('Destination Root Directory', des)

    for user in os.listdir(src):
        sec_dir = os.path.join(src, user, sec_name)
        if os.path.exists(sec_dir):
            for f in os.listdir(sec_dir):
                cp = f.endswith('.java') and 'winning' in f
                if cp:
                    src_file = os.path.join(sec_dir, f)
                    sharpen_file = os.path.join('sharpen', 'Program.java')
                    sharpen_CS_file = os.path.join(
                        'sharpen', 'sharpen.net', 'sharpen', 'Program.cs')
                    des_dir = os.path.join(des, user)
                    des_file = os.path.join(des_dir, f.replace('java', 'cs'))
                    p = subprocess.run(
                        'java -jar sharpen.jar sharpen\\', shell=True, stdout=subprocess.PIPE)
                    if not os.path.exists(sharpen_CS_file):
                        print('Error: cannot convert {}'.format(
                            os.path.relpath(src_file, src)))
                        continue

                    if not os.path.exists(des_dir):
                        os.makedirs(des_dir)

                    with open(sharpen_CS_file) as f:
                        data = f.read()

                    with open(sharpen_CS_file, 'w') as f:
                        data = data.replace(
                            'java.util.Arrays.sort', 'Array.Sort').split('\n')
                        data = [data[0], 'using System;',
                                'using System.Collections;'] + data[1:]
                        f.write('\n'.join(data))

                    print('Copying {} to {}'.format(os.path.relpath(
                        src_file, src), os.path.relpath(des_file, des)))
                    shutil.copy2(sharpen_CS_file, des_file)
                    os.remove(sharpen_CS_file)


# Copy the winning submissions from Pex4Fun dataset into /Collected/Pex4Fun
def copyP4F(src, des):
    # Copy everything
    for puzzle in os.listdir(src):
        if not os.path.isdir(src + '/' + puzzle) or 'winning' in puzzle:
            continue
        copy_tree(src + '/' + puzzle, des + '/' + puzzle)

    # Remove the puzzles and students who aren't eligible
    for puzzle in os.listdir(des):
        if not os.path.isdir(des + '/' + puzzle) or 'winning' in puzzle:
            continue
        # Remove puzzles with <2 winning students
        if not ELIGIBLE_DICT.get(int(puzzle)):
            shutil.rmtree(des + '/' + puzzle)
        if len(ELIGIBLE_DICT[int(puzzle)]) < 2:
            shutil.rmtree(des + '/' + puzzle)
        try:
            for student in os.listdir(des + '/' + puzzle):
                # Remove win-solution.cs
                if 'solution.cs' in student:
                    os.remove(des + '/' + puzzle + '/' + student)
                if not os.path.isdir(des + '/' + puzzle + '/' + student) or 'winning' in puzzle:
                    continue
                # Delete student dir if not eligible
                if student not in ELIGIBLE_DICT[int(puzzle)]:
                    shutil.rmtree(des + '/' + puzzle + '/' + student)
                    continue
                # Delete all non-winning submissions
                for sub in os.listdir(os.path.join(des, puzzle, student)):
                    if 'win-' not in sub:
                        os.remove(os.path.join(des, puzzle, student, sub))
        except FileNotFoundError:
            print(puzzle, ' deleted')

# Copy winning submissions from PKU dataset into /Collected/PKU


def copyPKU(src, des):
    # Copy everything
    for puzzle in os.listdir(src):
        if not os.path.isdir(src + '/' + puzzle):
            continue
        copy_tree(src + '/' + puzzle, des + '/' + puzzle)

    # Remove the puzzles and students who aren't eligible
    for puzzle in os.listdir(des):
        if not os.path.isdir(des + '/' + puzzle) or 'winning' in puzzle:
            continue
        for student in os.listdir(des + '/' + puzzle):
            # if os.path.isdir(des + '/' + puzzle + '/' + student):
            #     continue
            # Delete all non-winning submissions
            for sub in os.listdir(os.path.join(des, puzzle, student)):
                if '_Passed' not in sub:
                    os.remove(os.path.join(des, puzzle, student, sub))


if __name__ == '__main__':
    import argparse

    from config import *

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", "--winning", help="Only collect correct submissions", action="store_true")
    parser.add_argument(
        "-f", "--failing", help="Only collect incorrect submissions", action="store_true")
    parser.add_argument(
        "-p", "--prefix", help="Prefix for directory name", type=str)
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to run dupFinder on: CodeHunt, Pex4Fun, or PKU")
    parser.add_argument("sector",  nargs='?', type=str,
                        help="Sector number", default='')
    parser.add_argument("level", nargs='?', type=str,
                        help="Level number", default='')
    args = parser.parse_args()

    # Example of how to run:
    #   py .\collect.py 2 5       <-- Default
    #   py .\collect -w 2 5       <-- Winning only

    # Pex4Fun dataset
    if args.dataset == 'Pex4Fun':
        # Copy all dirs to /Collected/Pex4Fun
        copyP4F(P4F_ROOT, str(CODEHUNT_OUTPUT_ROOT / Path('Pex4Fun')))
        print(r'Collected all of the Pex4Fun dataset into /Collected/Pex4Fun')
        exit(1)

    # PKU dataset
    if args.dataset == 'PKU':
        # Copy all dirs to /Collected/Pex4Fun
        copyPKU(PKU_ROOT, str(CODEHUNT_OUTPUT_ROOT / Path('PKU')))
        print(r'Collected all of the PKU dataset into /Collected/PKU')
        exit(1)

    if all((args.winning, args.failing)):
        print('Conflict option!', '-w', '-f')
        exit(1)
    if not args.sector or not args.level:
        print('Enter sector and level.')
        exit(1)
    sector = args.sector
    level = args.level
    source = CODEHUNT_ROOT  # From config.py

    prefix = args.prefix if args.prefix else {(False, False): 'default', (
        True, False): 'win', (False, True): 'fail'}[(args.winning, args.failing)]
    destination = CODEHUNT_OUTPUT_ROOT / \
        '{}-{}-{}'.format(prefix, sector, level)
    sector_filter(source, destination, sector, level,
                  winning=args.winning, failing=args.failing)
