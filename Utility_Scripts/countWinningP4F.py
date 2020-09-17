if __name__ == '__main__':
	import os
	import sys

	probs = ['105', '107', '110', '111', '112', '132', '135', '140', '141', '143', '144', '152', '33', '34', '35', '36', '38', '40', '42', '43', '45', '47', '48', '49', '50', '53', '55', '57', '58', '59', '60', '61', '62', '63', '64', '65', '73', '74', '75', '83']
	root = r'C:\Users\rayjo\Documents\Pex4Fun Dataset (clean)\apcs'
	for puz in os.listdir(root):
		cs, tolCs = 0, 0
		if puz not in probs: continue
		if not os.path.isdir(root+'/'+puz): continue
		for user in os.listdir(root+'/'+puz):
			if not os.path.isdir(root+'/'+puz+'/'+user): continue
			for sub in os.listdir(root+'/'+puz+'/'+user):
				if 'win-' in sub: 
					if sub.endswith('.cs'): cs += 1
					# print(user, puz, sub)
				if sub.endswith('.cs'): tolCs += 1
		# print(puz + '\n', 'winning C#: ', cs, 'total C#: ', tolCs)
		print(puz, cs, tolCs)