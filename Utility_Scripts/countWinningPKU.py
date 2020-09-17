if __name__ == '__main__':
	import os
	import sys

	root = r'C:\Users\rayjo\Documents\PKU Dataset\introclassoutput (C#)'
	for puz in os.listdir(root):
		cs, tolCs = 0, 0
		if not os.path.isdir(root+'/'+puz): continue
		for user in os.listdir(root+'/'+puz):
			if not os.path.isdir(root+'/'+puz+'/'+user): continue
			for sub in os.listdir(root+'/'+puz+'/'+user):
				if 'Passed' in sub: 
					if sub.endswith('.cs'): cs += 1
					# print(user, puz, sub)
				if sub.endswith('.cs'): tolCs += 1
		# print(puz + '\n', 'winning C#: ', cs, 'total C#: ', tolCs)
		print(puz, cs, tolCs)