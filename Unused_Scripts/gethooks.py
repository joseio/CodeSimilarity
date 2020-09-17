# Utility script to get all function hooks from CodeHunt dataset that I'll need to account for in lex_yacc.py
if __name__ == "__main__":
    import os
    import shutil
    import argparse
    import subprocess
    from pathlib import Path
    from config import *
    import re

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir', type=str, help='Root directory of where evaluation subjects reside')
    args = parser.parse_args()
    root = args.dir

    hooks = set()
    for puzzle in os.listdir(root):
        if not os.path.isdir(root + '/' + puzzle):
            continue
        for student in os.listdir(root + '/' + puzzle):
            if not os.path.isdir(os.path.join(root, puzzle, student)):
                continue
            for sub in os.listdir(os.path.join(root, puzzle, student)):
                if not sub.endswith('.cs'):
                    continue
                with open(os.path.join(root, puzzle, student, sub), 'r') as f:
                    lines = f.readlines()
                    for l in lines:
                        match = re.search('\w+\.\w+\(', l)
                        if match:
                            # Add func hook to set and remove trailing paren '(''
                            hooks.add(match.group()[:-1])

    print(hooks)
