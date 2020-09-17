import os

# root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results\Pex4Fun'
root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results'

# Print out the distribution of submissions per cluster for our tool
for puz in os.listdir(root):
    # if 'ignoring' in puz:
    if 'Sector9-Level1' in puz:
        continue
    print('\n')
    for time in os.listdir(root+'/'+puz):
        try:
            for cluster in os.listdir(root+'/'+puz+'/'+time+'/Union/clusters(pc+rv)'):
                print(puz, cluster, len(os.listdir(root+'/'+puz +
                                                   '/'+time+'/Union/clusters(pc+rv)/'+cluster)))
        except FileNotFoundError:
            if os.path.exists(root+'/'+puz+'/'+time+'/Union/clusters(pc+rv).csv'):
                print(puz, cluster, 0)
            else:
                print(puz, 'failed to produce clusters!')
