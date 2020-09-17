if __name__ == "__main__":
    import lizard
    import os
    import subprocess
    import sys
    import argparse
    from config import *

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--exp_type", type=str, default='',
                        help="Select which experiment type you'd like cyclomatic complexity numbers for, `pc` or `pc+rv`.")
    parser.add_argument("sector", type=str, help="Sector")
    parser.add_argument("level", type=str, help="Level")
    args = parser.parse_args()

    # Example of how to run:
    #   py .\cyclomatic.py 2 5 -c 'pc'    <-- Sector 2, level 5, PC experiment

    if not args.exp_type or (args.exp_type != 'pc' and args.exp_type != 'pc+rv'):
        print('Expected "pc" or "pc+rv" as an argument for -c or --exp_type.')
        sys.exit(0)

    exp_type = 'clusters(' + args.exp_type + ')'
    resultsDir = PEX_OUTPUT_ROOT / \
        'Sector{}-Level{}'.format(args.sector, args.level)
    all_subdirs = [resultsDir / d for d in os.listdir(
        resultsDir) if os.path.isdir(resultsDir / d)]
    latest_subdir = resultsDir / max(all_subdirs, key=os.path.getmtime)

    # Run Lizard cyclomatic complexity tool on each cluster to get average complexity for each cluster
    # This helps assign semantic meaning to clusters
    for clusterDir in os.listdir(latest_subdir / UNION_RESULTS / exp_type):
        working_dir = latest_subdir / UNION_RESULTS / exp_type / clusterDir
        out_file = working_dir / "Cyclomatic_Complexity.txt"
        subprocess.call(['lizard', str(working_dir), '-l',
                         'csharp', '-o', str(out_file)])
