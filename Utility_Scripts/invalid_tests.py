
if __name__ == "__main__":
    import subprocess
    import argparse
    from config import *
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("sector", type=str, help="Sector")
    parser.add_argument("level", type=str, help="Level")
    parser.add_argument("-c", "--concrete_arg", type=str,
                        default='', help="Name of concrete test folder you wish to cluster by (optional)")

    # Example of how to run:
    #   py .\invalid_tests.py 2 5    <-- Sector 2, level 5

    args = parser.parse_args()

    # Get last modified folder in Results dir (newest result)
    resultsDir = PEX_OUTPUT_ROOT / \
        'Sector{}-Level{}'.format(args.sector, args.level)
    all_subdirs = [resultsDir / d for d in os.listdir(
        resultsDir) if os.path.isdir(resultsDir / d)]
    latest_subdir = resultsDir / max(all_subdirs, key=os.path.getmtime)
    union_dir = latest_subdir / UNION_RESULTS
    invalid_tests_dir = union_dir / 'InvalidTests.csv'

    # Print list of tests that cause (expression too big) and call those tests invalid
    subprocess.call(['powershell', 'Get-ChildItem -Path', str(union_dir), '-Recurse -Filter results.csv | Select-String "too big" -List | Select Path | Export-CSV', str(invalid_tests_dir)], shell=True)        