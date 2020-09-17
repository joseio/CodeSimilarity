if __name__ == '__main__':
	import os
	import sys

	probs = ['Sector2-Level1', 'Sector2-Level2', 'Sector2-Level5', 'Sector2-Level6', 'Sector3- Level1', 'Sector3- Level2', 'Sector3- Level3', 'Sector3- Level6', 'Sector4-Level2', 'Sector4-Level3', 'Sector4-Level4', 'Sector4-Level6']
	root = r'C:\Users\rayjo\Documents\GitHub\Code-Hunt\Dataset\users'
	cs, java, tolCs, tolJava = 0, 0, 0, 0
	for user in os.listdir(root):
		for puz in os.listdir(root+'/'+user):
			if sys.argv[1] not in puz: continue
			for sub in os.listdir(root+'/'+user+'/'+puz):
				if 'winning' in sub: 
					if sub.endswith('.java'): java += 1
					elif sub.endswith('.cs'): cs += 1
					# print(puz, user, sub)
				if sub.endswith('.java'): tolJava += 1
				elif sub.endswith('.cs'): tolCs += 1
	print(sys.argv[1] + '\n', 'winning C#: ', cs, 'total C#: ', tolCs, 'winning Java: ', java, 'total Java: ', tolJava)