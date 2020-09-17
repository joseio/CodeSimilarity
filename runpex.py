import os
import re
import sys
import csv
import time
import json
import shutil
import datetime
import subprocess

from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from config import *


class MSBuilder:
    def __init__(self, cwd, cs_path):
        self.cs_path = cs_path
        self.cwd = cwd
        self.CMD = ['MSBuild', '{}'.format(self.cwd / PEX_SOLUTION_NAME)]

    def run(self):
        shutil.copy(self.cs_path, self.cwd /
                    PEX_MAIN_PROJECT_NAME / PEX_MAIN_FILENAME)
        shutil.copy(self.cwd / PEX_TEST_PROJECT_NAME / PEX_TEST_BACKUP_PROJECT_NAME,
                    self.cwd / PEX_TEST_PROJECT_NAME / (PEX_TEST_PROJECT_NAME + '.csproj'))
        p = subprocess.run(self.CMD, shell=True, stdout=subprocess.PIPE)
        return False if p.returncode != 0 else True


class PexRunner:
    def __init__(self, cwd, des_path):
        self.des_path = des_path
        self.cwd = cwd
        self.TEST_ROOT = self.cwd / PEX_TEST_PROJECT_NAME
        self.CMD = ['pex.exe', '{}'.format(
            self.TEST_ROOT / r'bin\Debug\{}.dll'.format(PEX_TEST_PROJECT_NAME)), '/nor']
        self.REPORT_DIR = self.TEST_ROOT / PEX_REPORT_ROOT

    def run(self):
        shutil.rmtree(self.REPORT_DIR, ignore_errors=True)
        subprocess.run(self.CMD, shell=True, stdout=subprocess.PIPE)
        try:
            report = next(self.REPORT_DIR.iterdir())
            shutil.copytree(report, self.des_path)
            return self.des_path
        except StopIteration:
            return False


class ReportAnalyzer:
    def __init__(self, report_path, var_names):
        self.report_path = report_path
        self.xml_path = self.report_path / PEX_REPORT_FILE
        with self.xml_path.open() as f:
            self.content = f.read()
        self.soup = BeautifulSoup(self.content, features='html.parser')
        self.search_pattern = re.compile(
            r'Assert\.AreEqual<string>.*\("(.*)", s\);')
        self.test_inputs = [{j.get('name'): j.get_text().replace('"', '') for j in ti} for ti in zip(
            *[self.soup.find_all('value', {'name': v}) for v in var_names])]
        self.test_code = list(map(lambda x: ' '.join(
            x.get_text().split()), self.soup.find_all('code')))
        self.io_pairs = [(k, self.search_pattern.findall(v)[0].replace('"', '')) for k, v in zip(
            self.test_inputs, self.test_code) if len(self.search_pattern.findall(v)) > 0]

    def run(self):
        results = []
        for test_input, output in self.io_pairs:
            path_condition, ret_val = list(
                map(lambda x: ' '.join(x.strip().split()), output.split('RET_DIV')))
            results.append([json.dumps(test_input), path_condition, ret_val])
        return results


class CSVSaver:
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def write_row(self, line: list):
        # if not os.path.exists(self.file_path):
        #     return
        with open(self.file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(line)

    def write_rows(self, lines: list):
        # if not os.path.exists(self.file_path):
        #     return
        try:
            with open(self.file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for line in lines:
                    writer.writerow(line)
        except UnicodeDecodeError:
            print('Unicode decode error')
            # Try different encoding types
            for encode in ('cp1252', 'cp850', 'utf-8', 'utf8', 'Latin1'):
                try:
                    with open(self.file_path, 'a', newline='', encoding=encode) as csvfile:
                        writer = csv.writer(csvfile)
                        for line in lines:
                            writer.writerow(line)
                except UnicodeDecodeError:
                    print('Unicode decode error')
                    continue
                else:
                    print('Decode successful')
                    break


def pex_runner_wrapper(cwd, cs_path, des_path, vnames, user, tries, filename, counter, total_cnt):
    print('[{}/{}] Running the toolchain on {}\'s submission number {} at instance #{}. Note that I count submission numbers from 1 - n.'.format(
        counter, total_cnt, user, tries, cwd.name))
    funcs = [(MSBuilder, (cwd, cs_path)), (PexRunner, (cwd, des_path)),
             (ReportAnalyzer, (des_path, vnames))]
    errored = False
    results = [['#', user, tries, filename], ]
    # Only consider those C# submissions that compile.
    for c, ps in funcs:
        if not errored:
            try:
                ret = c(*ps).run()
                assert(ret is not False)
            except AssertionError:
                ret = [['FAILED'], ]
                print('Failed to execute {}. {}\'s submission number {} likley contains error and therefore fails to compile. Note that I count submission numbers from 1 - n.'.format(
                    c.__name__, user, tries))
                errored = True

    if not errored:
        shutil.copy(cs_path, des_path)
    results.extend(ret)
    return results


def pick_free(instances):
    for k, v in instances.items():
        if not v:
            return k
    return False


def clean_finished(submitted, instances, csv_wrapper):
    subs = set(as_completed(submitted))
    for sub in as_completed(submitted):
        key = submitted[sub]
        csv_wrapper.write_rows(sub.result())
        instances[key] = False

    for s in subs:
        del submitted[s]


def runpex_P4F_PKU(dataset, puzzle, parallelism):
    prefix = 'p4f' if dataset == 'Pex4Fun' else 'pku'
    input_dir = CODEHUNT_OUTPUT_ROOT / Path('{}/{}'.format(dataset, puzzle))
    template_PUT = PEX_PUT_TEMPLATE / Path(dataset) / '{}.cs'.format(puzzle)

    _dt_now = datetime.datetime.now()
    output_dir = PEX_OUTPUT_ROOT / Path(dataset) / puzzle / '{}-{}-{}-{}-{}-{}'.format(
        _dt_now.year, _dt_now.month, _dt_now.day, _dt_now.hour, _dt_now.minute, _dt_now.second)

    vnames = VARNAME_SWITCH['{}-{}'.format(prefix, puzzle)]

    # checkers
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    if not template_PUT.exists():
        print('Cannot find Pex PUT for Puzzle {} at {}'.format(
            puzzle, template_PUT), file=sys.stderr)

    if not input_dir.exists():
        print('Cannot find input data for Puzzle {} at {}'.format(
            puzzle, input_dir), file=sys.stderr)

    # Setup instances
    parallelism = parallelism if parallelism > 1 else 1
    shutil.rmtree(PEX_TMP_ROOT, ignore_errors=True)
    instances = {PEX_TMP_ROOT / str(tid): False for tid in range(parallelism)}
    for ins in instances:
        shutil.copytree(PEX_SOLUTION_TEMPLATE, ins)
        shutil.copy(template_PUT, ins /
                    PEX_TEST_PROJECT_NAME / PEX_TEST_FILENAME)

    shutil.copytree(next(iter(instances)), output_dir / 'Solution')

    if args.parallelism > 1:
        thread_pool = ThreadPoolExecutor(max_workers=args.parallelism)

    # Main part
    total_cnt = len([1 for root, dirs, files in os.walk(input_dir)
                     for f in files if f.endswith('.cs')])
    csv_wrapper = CSVSaver(output_dir / PEX_OUTPUT_NAME)
    counter = 0
    submitted = dict()
    for user_dir in input_dir.iterdir():
        user = user_dir.name
        for i, cs_path in enumerate(user_dir.iterdir(), start=1):
            counter += 1
            file = cs_path.name
            des_path = output_dir / '{}-Try{}'.format(user, i)
            if args.parallelism > 1:
                while True:
                    worker = pick_free(instances)
                    if worker:
                        break
                    else:
                        clean_finished(submitted, instances, csv_wrapper)
                        time.sleep(2)
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


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fake", type=str,
                        help="Only collect path conditions without running Pex (specify a Pex result directory")
    parser.add_argument("-j", "--parallelism", type=int,
                        default=1, help="Run Pex in parallel")
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to run dupFinder on: CodeHunt, Pex4Fun, or PKU")
    parser.add_argument("sector", type=str, help="Sector number")
    parser.add_argument("level", nargs='?', type=str,
                        help="Level number", default='')
    args = parser.parse_args()

    # Example of how to run:
    #   py .\runpex.py 2 5 win-2-5      <-- Winning only
    #   py .\runpex.py -j 4 2 5  win-2-5      <-- Winning only w/ 4 parallel threads

    # Pex4Fun or PKU datasets
    if args.dataset in ['Pex4Fun', 'PKU']:
        # Change all variable names and paths here
        runpex_P4F_PKU(args.dataset, args.sector, args.parallelism)
        exit(1)

    if not args.level:
        print('Enter sector, level.')
        exit(1)
    # assign values
    sector = args.sector
    level = args.level
    input_dir = CODEHUNT_OUTPUT_ROOT / 'win-{}-{}'.format(sector, level)
    parallelism = args.parallelism
    template_PUT = PEX_PUT_TEMPLATE / \
        'Sector{}-Level{}.cs'.format(sector, level)
    if args.fake:
        output_dir = PEX_OUTPUT_ROOT / args.fake
    else:
        _dt_now = datetime.datetime.now()
        output_dir = PEX_OUTPUT_ROOT / 'Sector{}-Level{}'.format(sector, level) / '{}-{}-{}-{}-{}-{}'.format(
            _dt_now.year, _dt_now.month, _dt_now.day, _dt_now.hour, _dt_now.minute, _dt_now.second)

    vnames = VARNAME_SWITCH['{}-{}'.format(sector, level)]

    # checkers
    if not output_dir.exists():
        if args.fake:
            print('Pex results:', output_dir,
                  'does not exist!', file=sys.stderr)
        else:
            output_dir.mkdir(parents=True)

    if not template_PUT.exists():
        print('Cannot find Pex PUT for Sector{}-Level{} at {}'.format(sector,
                                                                      level, template_PUT), file=sys.stderr)

    if not input_dir.exists():
        print('Cannot find input data for Sector{}-Level{} at {}'.format(sector,
                                                                         level, input_dir), file=sys.stderr)

    # Setup instances
    parallelism = args.parallelism if args.parallelism > 1 else 1
    shutil.rmtree(PEX_TMP_ROOT, ignore_errors=True)
    instances = {PEX_TMP_ROOT / str(tid): False for tid in range(parallelism)}
    for ins in instances:
        shutil.copytree(PEX_SOLUTION_TEMPLATE, ins)
        shutil.copy(template_PUT, ins /
                    PEX_TEST_PROJECT_NAME / PEX_TEST_FILENAME)

    shutil.copytree(next(iter(instances)), output_dir / 'Solution')

    if args.parallelism > 1:
        thread_pool = ThreadPoolExecutor(max_workers=args.parallelism)

    # Main part
    total_cnt = len([1 for root, dirs, files in os.walk(input_dir)
                     for f in files if f.endswith('.cs')])
    csv_wrapper = CSVSaver(output_dir / PEX_OUTPUT_NAME)
    counter = 0
    submitted = dict()
    for user_dir in input_dir.iterdir():
        user = user_dir.name
        for i, cs_path in enumerate(user_dir.iterdir(), start=1):
            counter += 1
            file = cs_path.name
            des_path = output_dir / '{}-Try{}'.format(user, i)
            if args.parallelism > 1:
                while True:
                    worker = pick_free(instances)
                    if worker:
                        break
                    else:
                        clean_finished(submitted, instances, csv_wrapper)
                        time.sleep(2)
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
