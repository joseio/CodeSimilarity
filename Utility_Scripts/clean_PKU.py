import os
import shutil

root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Results\PKU'

for puz in os.listdir(root):
    if 'hw4' in puz:
        continue
    for time in os.listdir(root+'/'+puz):
        for cluster in os.listdir(root+'/'+puz+'/'+time+'/Union/clusters(pc+rv)'):
            # Copy cluster to new dir w/ 'clean_' prepended to it
            shutil.copytree(root+'/'+puz+'/'+time+'/Union/clusters(pc+rv)/'+cluster,
                            root+'/'+puz+'/'+time+'/Union/clusters(pc+rv)/clean_'+cluster)
            # Remove the ConsoleInput class from each sub
            for sub in os.listdir(root+'/'+puz+'/'+time+'/Union/clusters(pc+rv)/clean_'+cluster):
                with open(root+'/'+puz+'/'+time+'/Union/clusters(pc+rv)/clean_'+cluster+'/'+sub, 'r+', encoding='utf8') as f:
                    lines = f.readlines()
                    txt = []
                    for l in lines:
                        if 'Helper class added by C++ to C# Converter' in l:
                            # Point to beginning, clear, then re-write file contents
                            f.seek(0)
                            f.truncate(0)
                            f.writelines(''.join(txt))
                            break
                        txt.append(l)
