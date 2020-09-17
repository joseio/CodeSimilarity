import os
import subprocess


def neardupe_P4F():
    root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results\Pex4Fun'

    for puz in os.listdir(root):
        if 'ignoring' in puz:
            continue
        for time in os.listdir(root+'/'+puz):
            try:
                for cluster in os.listdir(os.path.join(root, puz, time, 'Union', 'clusters(pc+rv)')):
                    subprocess.call(['py', 'neardupe.py', '-d', 'Pex4Fun', '-ec',
                                     os.path.join(root, puz, time, 'Union', 'clusters(pc+rv)', cluster)])
            except FileNotFoundError:
                continue


def neardupe_PKU():
    root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results\PKU'

    for puz in os.listdir(root):
        if 'hw4' in puz:
            continue
        for time in os.listdir(root+'/'+puz):
            try:
                for cluster in os.listdir(os.path.join(root, puz, time, 'Union', 'clusters(pc+rv)')):
                    if 'clean' in cluster:
                        continue
                    subprocess.call(['py', 'neardupe.py', '-d', 'PKU', '-ec',
                                     os.path.join(root, puz, time, 'Union', 'clusters(pc+rv)', 'clean_' + cluster)])
            except FileNotFoundError:
                continue


def neardupe_algorithms():
    root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results\Sector9-Level1\2020-5-7-17-57-17\Union\clusters(pc+rv)'
    try:
        for algo in os.listdir(os.path.join(root)):
            for cluster in os.listdir(os.path.join(root, algo)):
                subprocess.call(['py', 'neardupe.py', '-d', 'CodeHunt',
                                 '-a', os.path.join(root, algo, cluster)])
    except FileNotFoundError:
        print('file not found!')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--algorithm", help="Run neardupe on one algorithm at a time (optional)", action="store_true")
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to run dupFinder on: CodeHunt, Pex4Fun, or PKU")
    args = parser.parse_args()

    if args.algorithm:
        neardupe_algorithms()
        exit(1)
    elif args.dataset == 'PKU':
        neardupe_PKU()
        exit(1)
    elif args.dataset == 'Pex4Fun':
        neardupe_P4F()
        exit(1)
