from pathlib import Path

# ==== Global settings ====
WORK_ROOT = Path.cwd()
DIR_BASE = Path(r"C:\Users\rayjo\Documents\GitHub\codesimilarity.v2")

# Starting to use relative path for paths under DIR_BASE
# ==== CodeHunt settings ====
CODEHUNT_ROOT = Path(
    r'C:\Users\rayjo\Documents\GitHub\Code-Hunt\Dataset\users')
CODEHUNT_OUTPUT_ROOT = DIR_BASE / Path(r'Collected')

# ==== Pex settings ====
PEX_SOLUTION_TEMPLATE = DIR_BASE / Path(r'Templates\Solution')
PEX_SOLUTION_NAME = 'Similarity.sln'
PEX_PUT_TEMPLATE = DIR_BASE / Path(r"Templates\PUT")
PEX_MAIN_PROJECT_NAME = 'Similarity'
PEX_MAIN_FILENAME = 'main.cs'
PEX_TEST_PROJECT_NAME = "Similarity.Tests"
PEX_TEST_BACKUP_PROJECT_NAME = 'Similarity.Tests.csproj.backup'
PEX_TEST_FILENAME = "ProgramTest.cs"
PEX_TMP_ROOT = DIR_BASE / Path(r'PexTmp')
PEX_OUTPUT_ROOT = DIR_BASE / Path(r'Results')
PEX_OUTPUT_NAME = 'results.csv'

# ==== Test union settings ====
UNION_CONCRETE_TESTS = 'Union_Concrete_Tests.txt'
UNION_RESULTS = 'Union'
DEVENV_EXE = r'C:\Program Files (x86)\Microsoft Visual Studio 10.0\Common7\IDE\devenv.exe'

# ==== Test union settings ====
RUNTIME_RESULTS = DIR_BASE / Path(r'Runtimes')


# --- DO NOT edit configurations below until "Cluster settings" unless you know what you are doing ! ---
PEX_REPORT_ROOT = Path(r'bin\Debug\reports')
PEX_REPORT_FILE = 'report.per'

VARNAME_SWITCH = {
    '1-4': ['x', 'y'],
    '1-6': ['s'],
    '2-1': ['a'],
    '2-2': ['s'],
    '2-3': ['s'],
    '2-4': ['a', 'b'],
    '2-5': ['a'],
    '2-6': ['n'],
    '3-1': ['a', 't'],
    '3-2': ['x'],
    '3-3': ['a', 'k'],
    '3-5': ['x', 'y'],
    '3-6': ['a', 'b'],
    '4-2': ['n', 'm'],
    '4-3': ['a', 'b'],
    '4-4': ['a'],
    '4-6': ['s'],

    '9-1': ['a'],  # Algorithms dataset

    'p4f-33': ['x'],  # Pex4Fun dataset
    'p4f-34': ['input'],
    'p4f-35': ['input'],
    'p4f-36': ['input'],
    'p4f-37': ['input'],
    'p4f-38': ['i', 's'],
    'p4f-39': ['t'],
    'p4f-40': ['s'],
    'p4f-41': ['s', 'x'],
    'p4f-42': ['upperBound'],
    'p4f-43': ['upperBound'],
    'p4f-44': ['number', 'power'],
    'p4f-45': ['i'],
    'p4f-46': ['lowerBound', 'upperBound'],
    'p4f-47': ['input'],
    'p4f-48': ['upperBound'],
    'p4f-49': ['word'],
    'p4f-50': ['s'],
    'p4f-53': ['i'],
    'p4f-55': ['i'],
    'p4f-56': ['i', 'j'],
    'p4f-57': ['i'],
    'p4f-58': ['i'],
    'p4f-59': ['i'],
    'p4f-60': ['i', 'x'],
    'p4f-61': ['i', 'j', 'k'],
    'p4f-62': ['i'],
    'p4f-63': ['s'],
    'p4f-64': ['i'],
    'p4f-65': ['a', 'b', 'c'],
    'p4f-73': ['i', 'j'],
    'p4f-74': ['s'],
    'p4f-75': ['s'],
    'p4f-83': ['a', 'b'],
    'p4f-84': ['a', 'b'],
    'p4f-93': ['input', 'a', 'b', 'c'],
    'p4f-105': ['list', 'i'],
    'p4f-106': ['i'],
    'p4f-107': ['i'],
    'p4f-109': ['s'],
    'p4f-110': ['i'],
    'p4f-111': ['numbers'],
    'p4f-112': ['numbers'],
    'p4f-116': ['a', 'b'],
    'p4f-132': ['numbers', 'x'],
    'p4f-133': ['words', 's'],
    'p4f-135': ['numbers', 'x'],
    'p4f-136': ['numbers', 'x'],
    'p4f-137': ['numbers', 'x', 'y'],
    'p4f-140': ['numbers'],
    'p4f-141': ['words'],
    'p4f-143': ['a'],
    'p4f-144': ['s'],
    'p4f-145': ['s'],
    'p4f-146': ['s'],
    'p4f-147': ['s'],
    'p4f-149': ['s'],
    'p4f-152': ['s'],
    'p4f-153': ['a', 'b'],
    'p4f-154': ['slope1', 'yintercept1', 'slope2'],
    'p4f-155': ['x'],

    'pku-hw1': ['input'], # PKU dataset
    'pku-hw2': ['input'],
    'pku-hw3': ['loop_len', 'loop_input'],
    'pku-hw4': ['in_1', 'in_2', 'in_3']
}

TYPE_SWITCH = {
    '1-4': {
        'x': 'int',
        'y': 'int'
    },
    '1-6': {
        's': 'intArray'
    },
    '2-1': {
        'a': 'intArray',
        'a.Length': 'int'
    },
    '2-2': {
        's': 'string'
    },
    '2-3': {
        's': 'intArray'
    },
    '2-4': {
        'a': 'int',
        'b': 'int'
    },
    '2-5': {
        'a': 'intArray',
    },
    '2-6': {
        'n': 'int'
    },
    '3-1': {
        'a': 'intArray',
        't': 'int'
    },
    '3-2': {
        'x': 'int'
    },
    '3-3': {
        'a': 'intArray',
        'k': 'int'
    },
    '3-5': {
        'x': 'int',
        'y': 'int'
    },
    '3-6': {
        'a': 'intArray',
        'b': 'intArray'
    },
    '4-2': {
        'n': 'int',
        'm': 'int'
    },
    '4-3': {
        'a': 'intArray',
        'b': 'intArray'
    },
    '4-4': {
        'a': 'intArray'
    },
    '4-6': {
        's': 'string'
    },

    '9-1': {  # Algorithms dataset
        'a': 'intArray'
    },

    'p4f-33': {  # Pex4Fun dataset
        'x': 'int'
    },
    'p4f-34': {
        'input': 'int'
    },
    'p4f-35': {
        'input': 'int'
    },
    'p4f-36': {
        'input': 'int'
    },
    'p4f-37': {
        'input': 'int'
    },
    'p4f-38': {
        'i': 'int',
        's': 'string'
    },
    'p4f-39': {
        't': 'int'
    },
    'p4f-40': {
        's': 'string'
    },
    'p4f-41': {
        's': 'string',
        'x': 'char'
    },
    'p4f-42': {
        'upperBound': 'int'
    },
    'p4f-43': {
        'upperBound': 'int'
    },
    'p4f-44': {
        'number': 'int',
        'power': 'int'
    },
    'p4f-45': {
        'i': 'int'
    },
    'p4f-46': {
        'lowerBound': 'int',
        'upperBound': 'int'
    },
    'p4f-47': {
        'input': 'int'
    },
    'p4f-48': {
        'upperBound': 'int'
    },
    'p4f-49': {
        'word': 'string'
    },
    'p4f-50': {
        's': 'string'
    },
    'p4f-53': {
        'i': 'int'
    },
    'p4f-55': {
        'i': 'int'
    },
    'p4f-56': {
        'i': 'int',
        'j': 'int'
    },
    'p4f-57': {
        'i': 'int'
    },
    'p4f-58': {
        'i': 'int'
    },
    'p4f-59': {
        'i': 'int'
    },
    'p4f-60': {
        'i': 'int',
        'x': 'int'
    },
    'p4f-61': {
        'i': 'int',
        'j': 'int',
        'k': 'int'
    },
    'p4f-62': {
        'i': 'int'
    },
    'p4f-63': {
        's': 'string'
    },
    'p4f-64': {
        'i': 'int'
    },
    'p4f-65': {
        'a': 'int',
        'b': 'int',
        'c': 'int'
    },
    'p4f-73': {
        'i': 'int',
        'j': 'int'
    },
    'p4f-74': {
        's': 'string'
    },
    'p4f-75': {
        's': 'string'
    },
    'p4f-83': {
        'a': 'string',
        'b': 'string'
    },
    'p4f-84': {
        'a': 'string',
        'b': 'string'
    },
    'p4f-93': {
        'input': 'string',
        'a': 'string',
        'b': 'string',
        'c': 'string'
    },
    'p4f-105': {
        'list': 'intArray',
        'i': 'int'
    },
    'p4f-106': {
        'i': 'int'
    },
    'p4f-107': {
        'i': 'int'
    },
    'p4f-109': {
        's': 'string'
    },
    'p4f-110': {
        'i': 'int'
    },
    'p4f-111': {
        'numbers': 'intArray'
    },
    'p4f-112': {
        'numbers': 'intArray'
    },
    'p4f-116': {
        'a': 'intArray',
        'b': 'intArray'
    },
    'p4f-132': {
        'numbers': 'intArray',
        'x': 'int'
    },
    'p4f-133': {
        'words': 'stringArray',
        's': 'string'
    },
    'p4f-135': {
        'numbers': 'intArray',
        'x': 'int'
    },
    'p4f-136': {
        'numbers': 'intArray',
        'x': 'int'
    },
    'p4f-137': {
        'numbers': 'intArray',
        'x': 'int',
        'y': 'int'
    },
    'p4f-140': {
        'numbers': 'intArray'
    },
    'p4f-141': {
        'words': 'stringArray'
    },
    'p4f-143': {
        'a': 'stringArray'
    },
    'p4f-144': {
        's': 'string'
    },
    'p4f-145': {
        's': 'string'
    },
    'p4f-146': {
        's': 'string'
    },
    'p4f-147': {
        's': 'string'
    },
    'p4f-149': {
        's': 'string'
    },
    'p4f-152': {
        's': 'string'
    },
    'p4f-153': {
        'a': 'string',
        'b': 'string'
    },
    'p4f-154': {
        'slope1': 'int',
        'yintercept1': 'int',
        'slope2': 'int'
    },
    'p4f-155': {
        'x': 'int'
    },

    'pku-hw1': { # PKU dataset
        'input' : 'int'
    }, 
    'pku-hw2': {
        'input': 'int'
    },
    'pku-hw3': {
        'loop_len': 'int',
        'loop_input': 'intArray'
    },
    'pku-hw4': {
        'in_1': 'int',
        'in_2': 'string',
        'in_3': 'int'
    }
}

TYPES = {
    'bool': 'bool',
    'int': 'int',
    'char': 'char',
    'unsigned': 'unsigned',
    'long': 'long',
    'short': 'short',
    'uint': 'uint',
    'ulong': 'ulong',
    'uchar': 'uchar',
    'ushort': 'ushort',
    'double': 'double',
    'float': 'float'
}

# ==== Students who answered Pex4Fun puzzles correctly ====
P4F_ROOT = r'C:\Users\rayjo\Documents\Pex4Fun Dataset (clean)\apcs'
# Eligible students for Pex4Fun:
ELIGIBLE_DICT = {33: ['Alveries', 'Big Ol Mitch', 'Boofhead', 'InternetBird', 'Lhscompsci', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'hkovacik', 'rockrose'], 0: ['Anthony', 'Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'InternetBird', 'Lhscompsci', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'Senor Pelon', 'ShawnavonR', 'TheRama', 'chrissharp80', 'codeconfessions', 'cwx1611', 'hedoluna', 'hfrog713', 'hkovacik', 'kgashok', 'lapalejandro', 'rockrose', 'sebmaldo', 'user3'], 1: ['Anthony', 'Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'InternetBird', 'Lhscompsci', 'Lymia', 'Nurio', 'Ramya', 'Sadlic', 'Senor Pelon', 'ShawnavonR', 'TheRama', 'chrissharp80', 'codeconfessions', 'cwx1611', 'hedoluna', 'hfrog713', 'hkovacik', 'kgashok', 'rockrose', 'sebmaldo', 'user3'], 20: ['Anthony', 'Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'hkovacik', 'kgashok', 'rockrose'], 21: ['Anthony', 'Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'hkovacik', 'kgashok', 'rockrose'], 22: ['Anthony', 'Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'hkovacik', 'kgashok', 'rockrose'], 23: ['Anthony', 'Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'hkovacik', 'kgashok', 'rockrose'], 25: ['Anthony', 'Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'hkovacik', 'kgashok'], 26: ['Anthony', 'Big Ol Mitch', 'Boofhead', 'Mr I', 'Nurio', 'Sadlic', 'TheRama', 'hkovacik'], 32: ['Anthony', 'Big Ol Mitch', 'Mr I', 'Nurio', 'Ramya', 'hkovacik', 'kgashok'], 42: ['Anthony', 'InternetBird', 'Mr I', 'Nurio', 'Sadlic', 'rockrose'], 43: ['Anthony', 'Mr I', 'Nurio', 'Sadlic', 'rockrose'], 50: ['Anthony', 'Mr I', 'Nurio', 'ShawnavonR', 'hedoluna', 'rockrose'], 2: ['Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'InternetBird', 'Lhscompsci', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'Senor Pelon', 'ShawnavonR', 'TheRama', 'chrissharp80', 'codeconfessions', 'cwx1611', 'hedoluna', 'hfrog713', 'hkovacik', 'rockrose', 'sebmaldo', 'user3'], 3: ['Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'InternetBird', 'Lhscompsci', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'Senor Pelon', 'ShawnavonR', 'TheRama', 'chrissharp80', 'codeconfessions', 'cwx1611', 'hedoluna', 'hfrog713', 'hkovacik', 'rockrose', 'sebmaldo', 'user3'], 4: ['Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'InternetBird', 'Lhscompsci', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'Senor Pelon', 'ShawnavonR', 'TheRama', 'chrissharp80', 'codeconfessions', 'cwx1611', 'hedoluna', 'hfrog713', 'hkovacik', 'rockrose', 'sebmaldo', 'user3'], 5: ['Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'InternetBird', 'Lhscompsci', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'Senor Pelon', 'ShawnavonR', 'TheRama', 'chrissharp80', 'codeconfessions', 'cwx1611', 'hedoluna', 'hfrog713', 'hkovacik', 'rockrose', 'sebmaldo', 'user3'], 6: ['Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'InternetBird', 'Lhscompsci', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'chrissharp80', 'codeconfessions', 'cwx1611', 'hedoluna', 'hfrog713', 'hkovacik', 'rockrose', 'sebmaldo', 'user3'], 7: ['Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'InternetBird', 'Lhscompsci', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'Senor Pelon', 'ShawnavonR', 'TheRama', 'chrissharp80', 'codeconfessions', 'hedoluna', 'hkovacik', 'rockrose', 'sebmaldo', 'user3'], 8: ['Big Ol Mitch', 'Cockpit Trooper', 'Lhscompsci', 'Lymia', 'Mr I', 'Nurio', 'Sadlic', 'TheRama', 'chrissharp80', 'codeconfessions', 'hedoluna', 'hkovacik', 'user3'], 9: ['Big Ol Mitch', 'Boofhead', 'Cockpit Trooper', 'Lhscompsci', 'Mr I', 'Nurio', 'Sadlic', 'chrissharp80', 'hedoluna', 'hkovacik', 'rockrose', 'user3'], 10: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Lhscompsci', 'Love2Code', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'chrissharp80', 'hkovacik', 'jcpanopio', 'kgashok', 'rockrose', 'sebmaldo', 'user3'], 11: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Lhscompsci', 'Love2Code', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'chrissharp80', 'hkovacik', 'kgashok', 'rockrose', 'sebmaldo', 'user3'], 12: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Lhscompsci', 'Love2Code', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'TheRama', 'Uklid', 'chrissharp80', 'hkovacik', 'kgashok', 'rockrose', 'sebmaldo', 'user3'], 13: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'TheRama', 'Uklid', 'chrissharp80', 'hkovacik', 'kgashok', 'rockrose', 'user3'], 14: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'TheRama', 'Uklid', 'chrissharp80', 'hkovacik', 'kgashok', 'rockrose', 'user3'], 15: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Lymia', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'chrissharp80', 'hkovacik',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              'kgashok', 'rockrose', 'user3'], 16: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'chrissharp80', 'hkovacik', 'kgashok', 'rockrose', 'user3'], 17: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'TheRama', 'Uklid', 'chrissharp80', 'hkovacik', 'kgashok', 'rockrose', 'user3'], 18: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Lymia', 'Mr I', 'Nurio', 'Sadlic', 'chrissharp80', 'hkovacik', 'kgashok', 'rockrose'], 19: ['Big Ol Mitch', 'Boofhead', 'Lymia', 'Mr I', 'Sadlic', 'TheRama', 'hkovacik', 'kgashok'], 24: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'hkovacik', 'rockrose'], 27: ['Big Ol Mitch', 'Mr I', 'TheRama', 'hkovacik'], 28: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'ShawnavonR', 'TheRama', 'Uklid', 'kgashok'], 29: ['Big Ol Mitch', 'Lhscompsci', 'Mr I', 'Nurio', 'Sadlic', 'TheRama', 'hkovacik', 'kgashok'], 30: ['Big Ol Mitch', 'Boofhead', 'InternetBird', 'Love2Code', 'Mr I', 'Nurio', 'Ramya', 'Sadlic', 'TheRama', 'Uklid', 'hkovacik', 'kgashok'], 31: ['Big Ol Mitch', 'Boofhead', 'Mr I', 'Ramya', 'TheRama', 'hedoluna', 'hkovacik', 'kgashok'], 34: ['Boofhead', 'InternetBird', 'Lhscompsci', 'Mr I', 'Nurio', 'Sadlic', 'ShawnavonR', 'TheRama', 'hkovacik', 'rockrose'], 35: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Sadlic', 'TheRama', 'rockrose'], 51: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR', 'rockrose'], 52: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'ShawnavonR'], 53: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR'], 54: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR', 'rockrose'], 55: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR', 'rockrose'], 56: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR', 'rockrose'], 57: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'ShawnavonR', 'rockrose'], 58: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR'], 59: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR'], 60: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR'], 61: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya'], 62: ['Boofhead', 'InternetBird', 'Mr I', 'ShawnavonR'], 65: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio'], 66: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR'], 67: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR'], 69: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio'], 70: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya'], 71: ['Boofhead', 'InternetBird', 'Mr I', 'Nurio', 'Ramya'], 38: ['InternetBird', 'Mr I', 'Nurio', 'Sadlic', 'ShawnavonR', 'TheRama', 'rockrose'], 40: ['InternetBird', 'Mr I', 'Nurio', 'Sadlic', 'ShawnavonR', 'rockrose'], 41: ['InternetBird', 'Mr I', 'Nurio', 'Sadlic', 'ShawnavonR', 'rockrose'], 44: ['InternetBird', 'Mr I'], 45: ['InternetBird', 'Mr I', 'Nurio', 'rockrose'], 46: ['InternetBird', 'Mr I', 'Nurio'], 49: ['InternetBird', 'Mr I', 'Nurio', 'hedoluna', 'rockrose'], 63: ['InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR'], 64: ['InternetBird', 'Mr I', 'Nurio', 'ShawnavonR', 'hedoluna'], 72: ['InternetBird', 'Mr I', 'Nurio', 'Ramya'], 73: ['InternetBird', 'Mr I', 'Ramya'], 74: ['InternetBird', 'Mr I', 'Nurio', 'Ramya', 'ShawnavonR'], 75: ['InternetBird', 'Mr I', 'Nurio'], 78: ['InternetBird', 'Nurio', 'Ramya', 'ShawnavonR'], 103: ['InternetBird', 'Ramya', 'ShawnavonR'], 104: ['InternetBird', 'Ramya', 'ShawnavonR'], 105: ['InternetBird', 'Ramya', 'ShawnavonR'], 106: ['InternetBird', 'Ramya', 'ShawnavonR'], 107: ['InternetBird', 'Ramya'], 108: ['InternetBird', 'Ramya', 'ShawnavonR'], 109: ['InternetBird', 'Ramya'], 110: ['InternetBird', 'Ramya'], 111: ['InternetBird', 'Ramya'], 112: ['InternetBird', 'Ramya', 'ShawnavonR'], 116: ['InternetBird'], 132: ['Love2Code', 'Ramya', 'ShawnavonR', 'Uklid', 'hedoluna', 'kgashok'], 133: ['Love2Code', 'Ramya', 'ShawnavonR', 'Uklid', 'hedoluna', 'kgashok'], 144: ['Lymia', 'ShawnavonR', 'hedoluna'], 122: ['MichelÃ\xa0s', 'ShawnavonR'], 123: ['MichelÃ\xa0s'], 124: ['MichelÃ\xa0s'], 36: ['Mr I', 'Sadlic', 'TheRama', 'rockrose'], 37: ['Mr I', 'Nurio', 'TheRama', 'rockrose'], 39: ['Mr I', 'Sadlic', 'TheRama'], 47: ['Mr I', 'Nurio'], 48: ['Mr I', 'Nurio'], 68: ['Mr I', 'Nurio', 'ShawnavonR'], 77: ['Nurio', 'Ramya', 'ShawnavonR'], 79: ['Nurio', 'Ramya'], 154: ['Nurio'], 83: ['Ramya', 'ShawnavonR'], 84: ['Ramya'], 87: ['Ramya', 'ShawnavonR'], 88: ['Ramya', 'ShawnavonR'], 91: ['Ramya', 'ShawnavonR'], 92: ['Ramya', 'ShawnavonR'], 94: ['Ramya', 'ShawnavonR'], 113: ['Ramya', 'ShawnavonR'], 134: ['Ramya', 'ShawnavonR', 'Uklid', 'hedoluna'], 135: ['Ramya', 'ShawnavonR', 'Uklid', 'hedoluna'], 137: ['Ramya'], 140: ['Ramya', 'ShawnavonR', 'Uklid'], 141: ['Ramya', 'ShawnavonR'], 142: ['Ramya', 'ShawnavonR'], 143: ['Ramya', 'ShawnavonR'], 93: ['ShawnavonR'], 152: ['ShawnavonR', 'Uklid'], 153: ['ShawnavonR'], 136: ['hedoluna'], 145: ['hedoluna'], 146: ['hedoluna'], 147: ['hedoluna'], 155: ['hedoluna'], 149: ['kgashok']}


# ==== Students who answered PKU puzzles correctly ====
PKU_ROOT = r'C:\Users\rayjo\Documents\PKU Dataset\introclassoutput (C#)'
