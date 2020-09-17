import os
import xml.etree.ElementTree as ET

# Parse results for CodeHunt dataset


def parseCodeHunt(args):
    root = r'C:\Users\rayjo\Documents\dupFinder_Results\CodeHunt\single'
    for puz in os.listdir(root):
        if puz == 'Sector9-Level1':
            continue
        for f in os.listdir(root+'/'+puz):
            if not f.endswith('.xml'):
                continue
            tree = ET.parse(root+'/'+puz+'/'+f)
            parent = tree.getroot()[1]
            clusterNum = 0
            for dupe in parent:
                unique = set()
                for frag in dupe:
                    print(frag[0].text)
                    unique.add(frag[0].text)
                clusterNum += 1
                print(f, puz, ' Cluster # {}'.format(clusterNum), len(unique))
                with open(root+'/'+puz+'/'+'distributions.csv', 'a+') as file:
                    file.write(
                        f + ',' + puz + ',' + 'Cluster {}'.format(clusterNum) + ',' + str(len(unique)) + '\n')


# Parse results for Pex4Fun dataset
def parseP4F(args):
    root = r'C:\Users\rayjo\Documents\dupFinder_Results\Pex4Fun\single'
    for puz in os.listdir(root):
        if 'ignoring' in puz:
            continue
        for f in os.listdir(root+'/'+puz):
            if not f.endswith('.xml'):
                continue
            tree = ET.parse(root+'/'+puz+'/'+f)
            parent = tree.getroot()[1]
            clusterNum = 0
            for dupe in parent:
                unique = set()
                for frag in dupe:
                    print(frag[0].text)
                    unique.add(frag[0].text)
                clusterNum += 1
                print(f, puz, ' Cluster # {}'.format(clusterNum), len(unique))
                with open(root+'/'+puz+'/'+'distributions.csv', 'a+') as file:
                    file.write(
                        f + ',' + puz + ',' + 'Cluster {}'.format(clusterNum) + ',' + str(len(unique)) + '\n')


# Parse results for PKU dataset
def parsePKU(args):
    root = r'C:\Users\rayjo\Documents\dupFinder_Results\PKU\single'
    for puz in os.listdir(root):
        for f in os.listdir(root+'/'+puz):
            if not f.endswith('.xml'):
                continue
            tree = ET.parse(root+'/'+puz+'/'+f)
            parent = tree.getroot()[1]
            clusterNum = 0
            for dupe in parent:
                unique = set()
                for frag in dupe:
                    print(frag[0].text)
                    unique.add(frag[0].text)
                clusterNum += 1
                print(f, puz, ' Cluster # {}'.format(clusterNum), len(unique))
                with open(root+'/'+puz+'/'+'distributions.csv', 'a+') as file:
                    file.write(
                        f + ',' + puz + ',' + 'Cluster {}'.format(clusterNum) + ',' + str(len(unique)) + '\n')


# Parse results for Algorithms dataset
def parseAlgos(args):
    root = r'C:\Users\rayjo\Documents\dupFinder_Results\CodeHunt\single\Sector9-Level1'
    for puz in os.listdir(root):
        for f in os.listdir(root+'/'+puz):
            if not f.endswith('.xml'):
                continue
            tree = ET.parse(root+'/'+puz+'/'+f)
            parent = tree.getroot()[1]
            clusterNum = 0
            for dupe in parent:
                unique = set()
                for frag in dupe:
                    print(frag[0].text)
                    unique.add(frag[0].text)
                clusterNum += 1
                print(f, puz, ' Cluster # {}'.format(clusterNum), len(unique))
                with open(root+'/'+puz+'/'+'distributions.csv', 'a+') as file:
                    file.write(
                        f + ',' + puz + ',' + 'Cluster {}'.format(clusterNum) + ',' + str(len(unique)) + '\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to parse dupFinder results on: CodeHunt, Pex4Fun, Algos, or PKU")
    parser.add_argument('-s', '--single', action='store_true',
                        help='Evaluate only on a specific equivalence class')
    args = parser.parse_args()

    if not args.dataset:
        print('Please enter a dataset you\'d like to parse the dupFinder results for')
        exit(1)
    if args.dataset == 'CodeHunt':
        parseCodeHunt(args)
        exit(1)
    elif args.dataset == 'Pex4Fun':
        parseP4F(args)
        exit(1)
    elif args.dataset == 'PKU':
        parsePKU(args)
        exit(1)
    elif args.dataset == 'Algos':
        parseAlgos(args)
        exit(1)
