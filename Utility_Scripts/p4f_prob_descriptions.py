import os

root = r'C:\Users\rayjo\Documents\Pex4Fun Dataset (clean)\apcs'
valid = os.listdir(
    r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Collected\Pex4Fun')
for puz in os.listdir(root):
    if puz not in valid:
        continue
    with open(root + '/' + puz + '/' + os.listdir(root+'/'+puz)[-1], 'r') as f:
        lines = f.readlines()
    print(puz, ': ', lines[0], lines[1])
