import os
import subprocess


def dupFinder_PKU():
    root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results\PKU'

    for puz in os.listdir(root):
        if 'hw4' in puz:
            continue
        for time in os.listdir(root+'/'+puz):
            try:
                for cluster in os.listdir(os.path.join(root, puz, time, 'Union', 'clusters(pc+rv)')):
                    if 'clean' in cluster:
                        continue
                    subprocess.call(['py', 'dupFinder.py', '-d', 'PKU', '-ec',
                                     os.path.join(root, puz, time, 'Union', 'clusters(pc+rv)', 'clean_' + cluster)])
            except FileNotFoundError:
                continue


def dupFinder_algorithms():
    root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results\Sector9-Level1\2020-5-7-17-57-17\Union\clusters(pc+rv)'
    try:
        for algo in os.listdir(os.path.join(root)):
            for cluster in os.listdir(os.path.join(root, algo)):
                subprocess.call(['py', 'dupFinder.py', '-d', 'CodeHunt',
                                 '-a', os.path.join(root, algo, cluster)])
    except FileNotFoundError:
        print('file not found!')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--algorithm", help="Run dupFinder on one algorithm at a time (optional)", action="store_true")
    args = parser.parse_args()

    if args.algorithm:
        dupFinder_algorithms()
    else:
        dupFinder_PKU()
