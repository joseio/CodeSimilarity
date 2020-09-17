import os
import json


# Parse CodeClone's results on CodeHunt dataset
def parseCodeHunt():
    root = r'C:\Users\rayjo\Documents\GitHub\Near-Duplicate-Code-Detector\jsonl\CodeHunt\single'

    for puz in os.listdir(root):
        if puz == 'Sector9-Level1':
            continue
        for cluster in os.listdir(root+'/'+puz):
            for f in os.listdir(root + '/' + puz + '/' + cluster + '/clusters'):
                if not f.endswith('.json'):
                    continue
                arr = json.load(open(root+'/'+puz+'/'+cluster+'/clusters/'+f))
                clusterNum = 0
                for ele in arr:
                    clusterNum += 1
                    print(ele)
                    print(f, puz, 'Cluster {}'.format(
                        clusterNum), len(set(ele)))
                    with open(root+'/'+puz+'/distributions.csv', 'a+') as file:
                        file.write(f+','+puz+',Cluster {}'.format(clusterNum) +
                                   ','+str(len(set(ele))) + '\n')


# Parse Pex4Fun's results on Pex4Fun dataset
def parseP4F():
    root = r'C:\Users\rayjo\Documents\GitHub\Near-Duplicate-Code-Detector\jsonl\Pex4Fun\single'
    for puz in os.listdir(root):
        for cluster in os.listdir(root+'/'+puz):
            for f in os.listdir(root + '/' + puz + '/' + cluster + '/clusters'):
                if not f.endswith('.json'):
                    continue
                arr = json.load(open(root+'/'+puz+'/'+cluster+'/clusters/'+f))
                clusterNum = 0
                for ele in arr:
                    clusterNum += 1
                    print(ele)
                    print(f, puz, 'Cluster {}'.format(
                        clusterNum), len(set(ele)))
                    with open(root+'/'+puz+'/distributions.csv', 'a+') as file:
                        file.write(f+','+puz+',Cluster {}'.format(clusterNum) +
                                   ','+str(len(set(ele))) + '\n')


# Parse PKU's results on Pex4Fun dataset
def parsePKU():
    root = r'C:\Users\rayjo\Documents\GitHub\Near-Duplicate-Code-Detector\jsonl\PKU\single'
    for puz in os.listdir(root):
        for cluster in os.listdir(root+'/'+puz):
            for f in os.listdir(root + '/' + puz + '/' + cluster + '/clusters'):
                if not f.endswith('.json'):
                    continue
                arr = json.load(open(root+'/'+puz+'/'+cluster+'/clusters/'+f))
                clusterNum = 0
                for ele in arr:
                    clusterNum += 1
                    print(ele)
                    print(f, puz, 'Cluster {}'.format(
                        clusterNum), len(set(ele)))
                    with open(root+'/'+puz+'/'+cluster+'/distributions.csv', 'a+') as file:
                        file.write(f+','+puz+',Cluster {}'.format(clusterNum) +
                                   ','+str(len(set(ele))) + '\n')


# Parse results for Algorithms dataset
def parseAlgos():
    root = r'C:\Users\rayjo\Documents\GitHub\Near-Duplicate-Code-Detector\jsonl\CodeHunt\single\Sector9-Level1'
    for puz in os.listdir(root):
        for cluster in os.listdir(root+'/'+puz):
            for f in os.listdir(root + '/' + puz + '/' + cluster + '/clusters/' + puz):
                if not f.endswith('.json'):
                    continue
                arr = json.load(open(root+'/'+puz+'/'+cluster +
                                     '/clusters/' + puz + '/' + f))
                clusterNum = 0
                for ele in arr:
                    clusterNum += 1
                    print(ele)
                    print(f, puz, 'Cluster {}'.format(
                        clusterNum), len(set(ele)))
                    with open(root+'/'+puz+'/distributions.csv', 'a+') as file:
                        file.write(f+','+puz+',Cluster {}'.format(clusterNum) +
                                   ','+str(len(set(ele))) + '\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, default='',
                        help="Specify which dataset you'd like to parse dupFinder results on: CodeHunt, Pex4Fun, Algos, or PKU")
    args = parser.parse_args()

    if not args.dataset:
        print('Please enter a dataset you\'d like to parse the dupFinder results for')
        exit(1)
    if args.dataset == 'CodeHunt':
        parseCodeHunt()
        exit(1)
    elif args.dataset == 'Pex4Fun':
        parseP4F()
        exit(1)
    elif args.dataset == 'PKU':
        parsePKU()
        exit(1)
    elif args.dataset == 'Algos':
        parseAlgos()
        exit(1)
