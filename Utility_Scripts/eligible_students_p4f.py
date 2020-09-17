from collections import defaultdict
file = r'C:\Users\rayjo\Documents\Pex4Fun Dataset (clean)\apcs\students.txt'
nums = list(enumerate(['name', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64,
                       65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 83, 84, 87, 88, 91, 92, 93, 94, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 116, 122, 123, 124, 132, 133, 134, 135, 136, 137, 140, 141, 142, 143, 144, 145, 146, 147, 149, 152, 153, 154, 155]))

with open(file, 'r') as f:
    lines = f.readlines()

probs_dict = defaultdict(list)
for x in range(1, len(lines)):
    l = lines[x].split(',')
    for y in range(1, len(l)):
        # Add student ID to dict for that puzzle
        ele = l[y]
        if 'won' in ele:
            probs_dict[nums[y][1]] += [l[0]]

print(probs_dict)
