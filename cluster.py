import os
import re
import z3
import sys
import io
import csv
import time
import shutil
import multiprocessing as mp

from datetime import datetime
from lex_yacc import SimpleLexer, SimpleParser
from itertools import product
from collections import namedtuple, defaultdict
from pathlib import Path
from functools import reduce
from config import *


# PROJECT_PATH = r'C:\Users\Neil\OneDrive\Projects\CodeSimilarity'
# REL_PATH = os.path.relpath(os.getcwd(), PROJECT_PATH)

UserSubmission = namedtuple('UserSubmission', 'userID subID filename')

# def replaceBools(pc):
#     splitUp, temp, res = re.findall(r'\w+\ss\d*\s=.*', pc), '', pc
#     toDelete, toReplace = {}, {}
#     if len(splitUp) == 1: temp = splitUp[0].split('&&')
#     else: temp = splitUp
#     for ele in temp:
#         # Break early if first word is NOT a valid type (e.g., 'bool', 'int')
#         if ele.split(' ')[0] not in TYPES:  break # Break early
#         symb, exp = ele.split(' = ')
#         symb = symb.split(' ')[1]
#         # Build dicts that I'll later modify 'res' with
#         toDelete[ele+'&&'] = ''
#         # Add 'False' flag, signifying that entries have not been updated w/ recursively derived expressions
#         toReplace[symb] = (exp, False)

#     # Break early if overwhelming num variables (as not to yield MemoryError)
#     if len(toReplace) > 100: return pc

#     for k in toDelete:
#         # Reformatting string to make it regex-processable, then deleting var definitions (e.g., 'bool s0 = True')
#         res = re.sub(re.escape(k), toDelete[k], res)
#     for k in toReplace:
#         # If updated expression not already cached, recursively find it and cache it
#         if not toReplace[k][1]:
#             pred = getPredicateRecursive(toReplace[k][0], toReplace)
#             # Update mapping, 'True' => entry updated w/ recursively derived expression
#             toReplace[k] = (pred, True)
#         else:
#             pred = toReplace[k][0]
#         res = re.sub(r'\b' + k + r'\b', '(' + pred + ')', res)

#     return res

#  # Fetch lowest-level expression & bubble it upwards, recursively
#  def getPredicateRecursive(pred, toReplace):
#     symbolsToReplace = re.findall(r'\bs\d*\b', pred)
#     if not symbolsToReplace: return pred
#     for k in symbolsToReplace:
#         # Check cached results first to save computation
#         if not toReplace[k][1]:
#             ans =  getPredicateRecursive(toReplace[k], toReplace)
#             # Cache result, set updated flag to true
#             toReplace[k] = (ans, True)
#         else:
#             ans = toReplace[k][0]
#             pred= re.sub(r'\b' + k + r'\b', '(' + ans + ')', pred)
#     return pred

# Don't split the predicates with '&&' inside (i.e., those in the nested shorthand-if statements)


def cleanInteriorAnd(pc):
    # Don't split the preamble expressions by '&&'
    expressions = pc.split(';')
    preamble = []
    for expr in expressions:
        if set(expr.split()) & set(TYPES.keys()):
            preamble += [expr]
        else:
            truePC = expr
            break

    truePC.replace(';', '&&')
    level, x = 0, 0
    while x < len(truePC):
        if truePC[x] == '(':
            level += 1
        if truePC[x] == ')':
            level -= 1
        if truePC[x] == '&' and truePC[x+1] == '&':
            if level != 0:
                x += 1
            else:
                # Replace '&&' w/ '@@' if not nested inside parens
                truePC = truePC[:x] + '@@' + truePC[x+2:]
        x += 1
    return '@@'.join(preamble) + '@@' + truePC


# Func to check if each sub-predicate of PC1 is contained in PC2 (to loosen clustering constraints)
def deepCheck(preamble1, pc1, preamble2, pc2, parser1, parser2):
    parser1.clear_context()
    parser2.clear_context()
    for pred in preamble1:
        try:
            parser1.parse(pred)
        except:
            continue
    for pred in preamble2:
        try:
            parser2.parse(pred)
        except:
            continue

    solver, unique = z3.Solver(), []
    # Split pred1 into two sub-preds
    for pred1 in pc1:
        # If has question mark, just see if pred1 equals any pred in pc2
        if '?' in pred1:
            uniqueFlag = True
            for pred2 in pc2:
                solver.reset()
                # First check if the two preds are equiv
                try:
                    parsedPred1, parsedPred2 = parser1.predParse(
                        pred1), parser2.predParse(pred2)
                except:
                    continue
                solver.add(parsedPred1 != parsedPred2)
                if solver.check().r == -1:  # If they're equiv...
                    uniqueFlag = False
                    break
            if uniqueFlag:
                unique.append(pred1)
            continue

        indx = pred1.find('||')
        if indx != -1:
            leftExpr = pred1[: indx].strip()
            # Remove leftover '('
            if leftExpr[0] == '(':
                leftExpr = leftExpr[1:]
            rightExpr = pred1[indx+2:].strip()
            # Remove leftover ')'
            if rightExpr[-1] == ')':
                rightExpr = rightExpr[:-1]

            # If PC2 is empty
            if not pc2:
                return pc1
            # Compare both of PC1's sub-preds to PC2's pred
            isUnique = False
            for pred2 in pc2:
                if not leftExpr or not rightExpr or not pred2:
                    continue
                solver.reset()

                # First check if the two preds are equiv
                try:
                    parsedPred1, parsedPred2 = parser1.predParse(
                        pred1), parser2.predParse(pred2)
                except:
                    continue  # Very hacky...
                solver.add(parsedPred1 != parsedPred2)
                if solver.check().r == -1:  # If they're equiv...
                    break

                # Then break up pred1 into subpreds and see if either of them equal pred2
                print('pred1 = ', pred1)
                print('pred2 = ', pred2)
                print('leftExpr = ', leftExpr)
                print('rightExpr = ', rightExpr)
                try:
                    parsedLeft, parsedRight,  = parser1.predParse(
                        leftExpr), parser1.predParse(rightExpr)
                except:
                    continue  # Very hacky...
                solver.add(parsedLeft != parsedPred2)
                # If leftExpr doesn't match pred2, then check rightExpr
                if solver.check().r != -1:
                    solver.reset()
                    solver.add(parsedRight != parsedPred2)
                    # If neither expressions match pred2, add pred1 to unique list
                    if solver.check().r != -1:
                        isUnique = True
                    else:
                        # Break if they match
                        isUnique = False
                        break
                else:
                    isUnique = False
                    break
                # If neither of pred1's subpreds match pred2, then pred1 is unique
                if isUnique:
                    unique.append(pred1)

    return unique


def implication(a_clean, b_clean, parser1, parser2):
     # Clear contexts in preparation for run
    parser1.clear_context()
    parser2.clear_context()
    a_preamble, b_preamble, a_rem, b_rem = [], [], [], []
    # Get preambles for both PCs
    for i in range(len(a_clean)):
        expr = a_clean[i]
        if set(expr.split()) & set(TYPES.keys()):
            a_preamble += [expr]
        else:
            a_rem = a_clean[i:]
            break

    for i in range(len(b_clean)):
        expr = b_clean[i]
        if set(expr.split()) & set(TYPES.keys()):
            b_preamble += [expr]
        else:
            b_rem = b_clean[i:]
            break

    # Do deeper check..remove preds shared b/t the two PCs
    a_remNew, b_remNew = [], []
    for xPred in a_rem:
        if xPred not in b_rem:
            a_remNew.append(xPred)
    for yPred in b_rem:
        if yPred not in a_rem:
            b_remNew.append(yPred)

    # allUnique = #unique preds in a_remNew and b_remNew, excluding the empty ('') pred
    allUnique = set(a_remNew) | set(b_remNew)
    allUnique = len(set(filter(lambda x: x != '', allUnique)))
    currUnique, s = set(), z3.Solver()

    for pred1 in a_remNew:
        for pred2 in b_remNew:
            # Check if pred1 -> pred2 and pred2 -> pred1
            s.reset()
            if not pred1 or not pred2:
                continue
            try:
                parsedPred1 = parser1.predParse(pred1)
                parsedPred2 = parser2.predParse(pred2)
            except:
                continue  # Very hacky...

            s.add(z3.Or(z3.Not(parsedPred1), parsedPred2) != True)
            res1 = s.check().r == -1
            s.reset()
            s.add(z3.Or(z3.Not(parsedPred2), parsedPred1) != True)
            res2 = s.check().r == -1
            if res1 and res2:
                print(pred1, ' EQUALS ', pred2)
                currUnique.update([pred1, pred2])
            elif res1:
                print(pred1, ' IMPLIES ', pred2)
                currUnique.update([pred1, pred2])
            elif res2:
                print(pred2, ' IMPLIES ', pred1)
                currUnique.update([pred1, pred2])

    # If num. preds matched == total num. unique preds, then CLUSTER them
    if len(currUnique) == allUnique:
        # print('CLUSTER THESE')
        return True
    # Default return
    return False

# def orToAnd(pc):
#     for x in range(len(pc)):
#         pred = pc[x]
#         indx = pred.find('||')
#         if indx != -1:
#             # leftExpr still has leftover '('
#             leftExpr = pred[: indx].strip()
#             # rightExpr still has leftover ')'
#             rightExpr = pred[indx+2:].strip()
#             # Conv OR -> AND and replace current pred
#             pc[x] = '!(!' + leftExpr + ') && !(' + rightExpr + ')'
#     return pc


class TestCase:
    def __init__(self, test_input: str, path_condition: str, ret_val: str, parser, parser2):
        # Conv PC + RV from `"{""x"": ""0""}",return x == 0;,return 0;` => PC: `x=0&&`, RV: `0&&`
        self.orig_pc = path_condition
        self.orig_rv = ret_val
        self.test_input, (path_condition, ret_val) = test_input, map(lambda x: x.replace('\\r', '').replace(
            '\\n', '').replace("\\'", "'").replace('return', '').replace('\\\\', '\\').strip(), [path_condition, ret_val])
        path_condition = cleanInteriorAnd(path_condition)
        # Replacing boolean 'sX' with expressions they represent
        # print('RAW PC = \n', path_condition)
        # path_condition = replaceBools(path_condition)
        # print('simplified PC = \n', path_condition)

        self.path_condition = list(
            map(lambda x: x.strip(), path_condition.split('@@')))

        # Testing following line:
        # self.path_condition = orToAnd(self.path_condition)

        self.ret_val = list(map(lambda x: x.strip(), ret_val.split('&&')))
        self.parser = parser
        self.parser2 = parser2
        # print('self.path_condition = \n', self.path_condition)
        self.string, self.z3 = self._parsepc(self.path_condition)
        # self.ret_string, self.ret_z3 = self._parserv(self.ret_val)

    def _parsepc(self, pc):
        errors = []
        models = []
        #print('arr pc: ', self.path_condition)
        #print('arr rv: ', self.ret_val)
        toAdd = False
        for c in pc:
            if not c:
                continue
            # Very hacky...but for works for array puzzles. Doesn't add preamble to PC
            # if '(int[])null' in c:
                # toAdd = True
            try:
                # print(c)
                self.parser.errored = False
                ret = self.parser.parse(c)
                # print(ret)
                # Had sort mismatch errors b/c ArithRefs mixed in with BoolRefs. Conv to BoolRef here (normalization).
                if type(ret) == z3.z3.ArithRef:
                    ret = z3.If(ret == 0, True, False)
                # self.parser.parse(c)
            except (ValueError, KeyError) as e:
                ret = None
            except z3.z3types.Z3Exception as e:
                ret = None
                print('Z3 error', e)

            # Changed 'ret == False' -> 'ret is False' to avoid triggering int 0
            if ret is False or ret == None:
                errors.append(c)
            else:
                #print('ret: ', ret)
                models.append(ret)
        self.parser.clear_context()
        # Checks if all eles in `models` eval to True
        retVal = '&&'.join(sorted(errors)), z3.simplify(
            reduce(z3.And, models, True)) if len(models) > 0 else z3.BoolVal(True)
        return retVal

    # Unused
    # def _parserv(self, rv):
    #     errors = []
    #     models = []
    #     #print('arr pc: ', self.path_condition)
    #     #print('arr rv: ', self.ret_val)
    #     for c in rv:
    #         if not c:
    #             continue
    #         try:
    #             # print(c)
    #             self.parser.errored = False
    #             ret = self.parser.parse(c)
    #             # print(ret)
    #             # self.parser.parse(c)
    #         except (ValueError, KeyError) as e:
    #             ret = None
    #         except z3.z3types.Z3Exception as e:
    #             ret = None
    #             print('Z3 error', e)

    #         # if type(ret) == z3.BoolRef and ret == False or ret == None:
    #         # Changed 'ret == False' -> 'ret is False' to avoid triggering int 0
    #         if ret is False or ret == None:
    #             errors.append(c)
    #         else:
    #             #print('ret: ', ret)
    #             models.append(ret)
    #     self.parser.clear_context()
    #     # If RV is var or arith expr:
    #     try:
    #         retVal = '&&'.join(sorted(errors)), z3.simplify(
    #             models[0]) if models else z3.BoolVal(True)
    #     # If RV is just an int val:
    #     except z3.z3types.Z3Exception:
    #         retVal = '&&'.join(sorted(errors)), z3.simplify(
    #             z3.Int(models[0])) if models else z3.BoolVal(True)
    #     return retVal

    def __eq__(self, at):
        # Relax constraints if the PCs don't exactly match
        # s = z3.Solver()
        # Check if both PCs are equal, w/ no need to relax constraints
        # s.add(self.z3 != at.z3)
        # if s.check().r == -1:
        #     print('Both PCs are exactly equal, no need to relax constraints to cluster them together.')
        #     return True

        # xPreds, yPreds = self.z3.children(), at.z3.children()
        # nEqPreds, nTotalPreds = 0, len(set(xPreds) | set(yPreds))
        # # Loop through each predicate and return True if >= 70% PC matches, else False
        # for x in xPreds:
        #     for y in yPreds:
        #         s.reset()
        #         s.add(x != y)
        #         # If preds are equal...
        #         if s.check().r == -1:
        #             nEqPreds += 1
        #             break
        # # Both PCs are approximately equal if ratio >= 0.8
        # return nEqPreds / nTotalPreds >= 0.8

        # Traditional clustering technique
        s = z3.Solver()
        s.add(self.z3 != at.z3)
        res = s.check().r
        # The two PCs are INEQUIV
        if res == 1:
            print('PC1:\n', self.path_condition, '\nPC2:\n', at.path_condition,
                  "\nDON'T MATCH...\n")  # Running z3.solve(self.z3 != at.z3):\n", z3.solve(self.z3 != at.z3))
            if self.string != at.string:
                print('STRING1:\n', self.string, '\nSTRING2:\n',
                      at.string, "\nDON'T MATCH\n")
            time.sleep(1)  # In case solve takes while to print

            # Implication approach, 100% of preds need to match
            return implication(self.path_condition, at.path_condition,
                               self.parser, self.parser2)
            # Code to perform deep check on sub-predicates to loosen clustering constraints below
            # self_preamble, at_preamble, self_rem, at_rem = [], [], [], []
            # # Get preambles for both PCs
            # for i in range(len(self.path_condition)):
            #     expr = self.path_condition[i]
            #     if set(expr.split()) & set(TYPES.keys()):
            #         self_preamble += [expr]
            #     else:
            #         self_rem = self.path_condition[i:]
            #         break

            # for i in range(len(at.path_condition)):
            #     expr = at.path_condition[i]
            #     if set(expr.split()) & set(TYPES.keys()):
            #         at_preamble += [expr]
            #     else:
            #         at_rem = at.path_condition[i:]
            #         break

            # # Do deeper check..remove preds shared b/t the two PCs
            # self_remNew, at_remNew = [], []
            # for xPred in self_rem:
            #     if xPred not in at_rem:
            #         self_remNew.append(xPred)
            # for yPred in at_rem:
            #     if yPred not in self_rem:
            #         at_remNew.append(yPred)

            # # Check if sub-pred of PC1 is in PC2, and vice-versa

            # a_unique = deepCheck(self_preamble, self_remNew,
            #                      at_preamble, at_remNew, self.parser, self.parser2)
            # b_unique = deepCheck(at_preamble, at_remNew,
            #                      self_preamble, self_remNew, self.parser, self.parser2)

            # # Consider the two PCs matching if >= 90% of preds match after doing deep check
            # if float(len(a_unique) + len(b_unique)) / len(set(self.path_condition) | set(at.path_condition)) <= 0.1:
            #     print(">= 90% MATCH")
            #     print('PC1\'s unique preds: ', a_unique)
            #     print('PC2\'s unique preds: ', b_unique)
            #     return True

        # s.check.r(): 1 (eq is true...PCs are inqeuiv) or -1 (eq is false...PCSs are equiv)
        return res == -1

    def __hash__(self):
        return id(self)

    def __str__(self):
        return self.string + '; Z3: ' + str(self.z3)

    def __repr__(self):
        return self.__str__()


class Submission:
    def __init__(self, user_sub, testcases):
        self.userID, self.subID, self.filename = user_sub
        self.testcases = testcases

    # '==' operator overload
    def __eq__(self, sub):
        # Put all keys from both self and sub into allKeys set
            # Note: '*' unpacks into list
        allKeys = set().union(*(d.keys() for d in self.testcases))
        allKeys.update(set().union(*(d.keys() for d in sub.testcases)))

        my_cases_dict = {
            k: v for ele in self.testcases for k, v in ele.items()}
        your_cases_dict = {
            k: v for ele in sub.testcases for k, v in ele.items()}

        # failed, nValidTests = 0, len(allKeys)
        for concreteTest in allKeys:
            # Skip concrete test if either dict doesn't have it. Cluster on the tests that each sub DOES have.
            if concreteTest not in my_cases_dict or concreteTest not in your_cases_dict:
                # failed += 1
                # nValidTests -= 1
                continue
            if my_cases_dict[concreteTest] != your_cases_dict[concreteTest]:
                # Print to file and terminal
                print(self.userID + '-attempt' + str(int(self.subID)-1) + '\'s PC doesn\'t match ' + sub.userID +
                                    '-attempt' + str(int(sub.subID)-1) + '\'s PC.\n')
                with open(latest_subdir / UNION_RESULTS / 'failedComparisons.txt', 'a+') as f:
                    f.write(self.userID + '-attempt' + str(int(self.subID)-1) + '\'s PC doesn\'t match ' + sub.userID +
                            '-attempt' + str(int(sub.subID)-1) + '\'s PC.\n' + self.userID + '-attempt' + str(int(self.subID)-1) + '\'s PC on ' + concreteTest + ':\n')
                    f.write(str(my_cases_dict[concreteTest].z3) + '\n')
                    f.write('\n' + sub.userID +
                            '-attempt' + str(int(sub.subID)-1) + '\'s PC:\n')
                    f.write(str(your_cases_dict[concreteTest].z3) + '\n')
                # failed += 1
                return False
        return True
        # Return true if they agree on >= 80% of concrete test cases, else false
        # return True if (failed / nValidTests) < 0.20 else False

    def __str__(self):
        return '{}-{}-{}'.format(self.userID, self.subID, self.filename)

    def __hash__(self):
        return id(self)


def clustering(submissions):
    startedClustering = datetime.now().strftime("%H:%M:%S")
    print('Began clustering at', startedClustering)
    if len(submissions) == 0:
        return []

    clusters = defaultdict(set)
    # Try to match each submission to a cluster, pairwise
    for sub in submissions:
        found = False
        for k in clusters:
            # Aka `if sub.__eq__(k):`
            if sub == k:
                print(sub.userID, sub.filename,
                      ' getting added to ', k.userID, k.filename)
                clusters[k].add(sub)
                found = True
                # I found cluster to place sub into, move onto next sub
                break
        if not found:
            print('Creating new cluster for ', sub.userID, sub.filename,)
            clusters[sub].add(sub)

    print('Began clustering at', startedClustering)
    print('Finished clustering at', datetime.now().strftime("%H:%M:%S"))
    return clusters


def algorithm_clustering(submissions):
    # Get all algorithm types:
    algos = set(re.search('\w+\.cs', x).group(0)
                [:-3] for x in [y.filename for y in submissions])
    clusters = defaultdict(set)
    # Try to match each submission to a cluster, pairwise
    for a in algos:
        for sub in submissions:
            # Skip those submissions not pertaining to same algo
            if a not in sub.filename:
                continue
            found = False
            for k in clusters:
                # Only compare like algorithms
                if a not in k[1].filename:
                    continue
                # Aka `if sub.__eq__(k):`
                if sub == k[1]:
                    print(sub.userID, sub.filename,
                          ' getting added to ', k[1].userID, k[1].filename)
                    clusters[a, k[1]].add(sub)
                    found = True
                    # I found cluster to place sub into, move onto next sub
                    break
            if not found:
                print('Creating new cluster for ', sub.userID, sub.filename,)
                clusters[a, sub].add(sub)
    return clusters


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    import argparse

    from config import TYPE_SWITCH

    # print(os.getcwd())

    parser = argparse.ArgumentParser()
    # parser.add_argument("-j", "--parallelism", type=int,
    #                     default=1, help="Cluster submissions in parallel")
    parser.add_argument("sector", type=str, help="Sector number")
    parser.add_argument("level", nargs='?', type=str,
                        help="Level number", default='')
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to run get concrete tests for")
    parser.add_argument(
        "-a", "--algorithm", help="Cluster one algorithm at a time (optional)", action="store_true")
    parser.add_argument("-c", "--concrete_arg", type=str,
                        default='', help="Name of concrete test folder you wish to cluster by (optional)")

    # Example of how to run:
    #   py .\cluster.py 2 5 win-2-5     <-- Sector 2, level 5 (winning only)

    args = parser.parse_args()

    if not args.level and not args.dataset:
        print('Enter sector and level.')
        exit(1)

    if args.dataset == 'Pex4Fun':
        input_dir = CODEHUNT_OUTPUT_ROOT / args.dataset / args.sector
        resultsDir = PEX_OUTPUT_ROOT / args.dataset / args.sector
        typeSwitch = 'p4f-{}'.format(args.sector)
    elif args.dataset == 'PKU':
        input_dir = CODEHUNT_OUTPUT_ROOT / args.dataset / args.sector
        resultsDir = PEX_OUTPUT_ROOT / args.dataset / args.sector
        typeSwitch = 'pku-{}'.format(args.sector)
    else:
        input_dir = CODEHUNT_OUTPUT_ROOT / \
            'win-{}-{}'.format(args.sector, args.level)
        resultsDir = PEX_OUTPUT_ROOT / \
            'Sector{}-Level{}'.format(args.sector, args.level)
        typeSwitch = '{}-{}'.format(args.sector, args.level)
    # Path handles case where concrete_arg empty. No problems
    concrete_arg = args.concrete_arg

    # Get last modified folder in Results dir (newest result)
    all_subdirs = [resultsDir / d for d in os.listdir(
        resultsDir) if os.path.isdir(resultsDir / d)]
    latest_subdir = resultsDir / max(all_subdirs, key=os.path.getmtime)

    # Initialize and expose outside of for-loop
    submissions_dict = defaultdict(list)
    for concreteDir in os.listdir(latest_subdir / UNION_RESULTS / concrete_arg):
        # Skip if in invalidTestList
        if os.path.isdir(latest_subdir / UNION_RESULTS / concrete_arg / concreteDir) and 'Solution' not in concreteDir and concreteDir:
            csv_path = latest_subdir / UNION_RESULTS / concrete_arg / \
                PEX_OUTPUT_NAME if concrete_arg else latest_subdir / \
                UNION_RESULTS / concreteDir / PEX_OUTPUT_NAME
            if not csv_path.exists():
                print('Cannot find ', csv_path)

            parser = SimpleParser(
                SimpleLexer().lexer, types=TYPE_SWITCH[typeSwitch], hooks={'Math.Abs': lambda x: z3.If(x >= 0, x, -x)})

            # Need second parser for sub-pred deep check exp
            parser2 = SimpleParser(
                SimpleLexer().lexer, types=TYPE_SWITCH[typeSwitch], hooks={'Math.Abs': lambda x: z3.If(x >= 0, x, -x)})

            # Loop over all .csv's per submission. Store all unique PCs into dict.
            with open(csv_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                lines = list(csv_reader)

            current_sub = None
            for l in lines:
                if len(l) not in {3, 4}:
                    continue
                if l[0].startswith('#'):
                    current_sub = UserSubmission(*l[1:])
                else:
                    submissions_dict[current_sub].append(
                        {concreteDir: TestCase(*l, parser=parser, parser2=parser2)})

    # Process submissions
    submissions = [Submission(s, ts)
                   for s, ts in submissions_dict.items()]

    # If I'm clustering one algo at a time:
    if args.algorithm:
        clusters = algorithm_clustering(submissions)
        print('Began clustering at', datetime.now().strftime("%H:%M:%S"))
        print('Finished clustering at', datetime.now().strftime("%H:%M:%S"))
    else:
        clusters = clustering(submissions)

    # res_dir, *_ = os.path.split(csv_path)
    res_dir = latest_subdir / UNION_RESULTS
    res_path = os.path.join(res_dir, 'clusters(pc+rv).csv')
    with open(res_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for k, v in clusters.items():
            writer.writerow([str(sub) for sub in v])
        writer.writerow([])
        if args.algorithm:
            for i, k in enumerate(clusters):
                for j, case in enumerate(k[1].testcases):
                    # Get dict key, providing dict has only one entry
                    concreteTest = next(iter(case.keys()))
                    writer.writerow(
                        ['cluster-{}'.format(i), k[1].testcases[j][concreteTest].string, str(k[1].testcases[j][concreteTest].z3)])
        else:
            for i, k in enumerate(clusters):
                for j, case in enumerate(k.testcases):
                    # Get dict key, providing dict has only one entry
                    concreteTest = next(iter(case.keys()))
                    writer.writerow(
                        ['cluster-{}'.format(i), k.testcases[j][concreteTest].string, str(k.testcases[j][concreteTest].z3)])

    clusters_dir = os.path.join(res_dir, 'clusters(pc+rv)')
    if os.path.exists(clusters_dir):
        shutil.rmtree(clusters_dir)

    if args.algorithm:
        for i, (k, v) in enumerate(clusters.items()):
            sub_cluster_dir = os.path.join(
                clusters_dir, k[0], 'cluster-{}'.format(i))
            for sub in v:
                if not os.path.exists(sub_cluster_dir):
                    os.makedirs(sub_cluster_dir)
                shutil.copy(os.path.join(input_dir, sub.userID, sub.filename), os.path.join(
                    sub_cluster_dir, str(sub).replace('\n', '')))
        exit(1)

    for i, (k, v) in enumerate(clusters.items()):
        sub_cluster_dir = os.path.join(
            clusters_dir, 'cluster-{}'.format(i))
        for sub in v:
            if not os.path.exists(sub_cluster_dir):
                os.makedirs(sub_cluster_dir)
            shutil.copy(os.path.join(input_dir, sub.userID, sub.filename), os.path.join(
                sub_cluster_dir, str(sub).replace('\n', '')))
