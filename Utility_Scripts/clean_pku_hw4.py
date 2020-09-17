import os
import subprocess
# Removing those PKU subs that don't have same method signature and don't compile
root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Collected\PKU\hw4'
num = 0
for stu in os.listdir(root):
    for sub in os.listdir(root+'/'+stu):
        with open(os.path.join(root, stu, sub), 'r+', encoding='utf-8-sig') as f:
            lines = f.readlines()
            correct_sig = False
            for x in range(len(lines)):
                # substr = 'static string Main(int in_1, string in_2, int in_3)'
                substr = 'public static string Main(int in_1, string in_2, int in_3)'
                if substr in lines[x]:
                    correct_sig = True
                    break
                    # lines[x] = 'public static string Main' + lines[x][len(substr):]
                    # print(lines[x])
        if not correct_sig:
            print('Incorrect method sig: ', stu, sub)
            num += 1
            # os.remove(os.path.join(root, stu, sub))
        else:
            k = subprocess.call(['csc', '-target:library', '-out:'+os.path.join(root, stu, 'File2.dll'),
                                 '-warn:0', '-nologo', os.path.join(root, stu, sub)])
            # If successful, then delete the produced .d'' files
            if k == 0:
                os.remove(os.path.join(root, stu, 'File2.dll'))
                # If failed to compile...remove it
            else:
                print('Non-compiling sub: ', stu, sub)
                num += 1
                # os.remove(os.path.join(root, stu, sub))

    # If now empty...remove the dir
    if not os.listdir(root+'/'+stu):
        os.rmdir(root+'/'+stu)

print('Removed ', num, ' submissions')
