import os
root = r'C:\Users\rayjo\Documents\GitHub\codesimilarity.v2\Collected\PKU\hw4'

# Remove the 'static' from class and function definitions for scoping purposes
# for  in os.listdir(root):
for stu in os.listdir(root+'/'):
    for sub in os.listdir(root+'/'+'/'+stu):
        with open(os.path.join(root, stu, sub), 'r+', encoding='utf-8-sig') as f:
            lines = f.readlines()
            for x in range(len(lines)):
                substr = 'static string Main'
                # substr = 'Mainn'
                # substr = 'public static int Main'
                # substr = 'char newChar)'
                if substr in lines[x]:
                    lines[x] = 'public static string Main' + \
                        lines[x][len(substr)+1:]
                    # lines[x] = lines[x][: lines[x].find(substr)] + 'public static double Main' + lines[x][lines[x].find(substr)+len(substr):]
                    # lines[x] = lines[x][:lines[x].find(substr)] + 'int newChar)'
                    print(lines[x])
                # substr2 = 'newChar.ToString()'
                # if substr2 in lines[x]:
                #     lines[x] = lines[x][: lines[x].find(
                #         substr2)] + '((char)newChar).ToString()' + lines[x][lines[x].find(substr2) + len(substr2):]
                #     print(lines[x])
                # if 'public static class GlobalMembers' in lines[x]:
                #     lines[x] = 'public class GlobalMembers'
            f.seek(0)
            f.truncate(0)
            f.writelines(''.join(lines))
            # print(''.join(lines))
