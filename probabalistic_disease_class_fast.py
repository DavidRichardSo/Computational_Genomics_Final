import sys
import gen_lib_fast as gl
import numpy as np

try: 
	eve = gl.loadEve(sys.argv[1])
	positive = open(sys.argv[2],'w')
	negative = open(sys.argv[3],'w')

	# make positive classification set
	temp = sys.argv[4].strip().split(":")
	classifier = []
	for line in temp:
		classifier.append(map(int,line.split(",")))

	prob = map(float,sys.argv[5].strip().split(":"))
except:
	print "Usage: <eve file> <positive file name> <negative file name> <disease string: commas in sets, sets broken with colons> <probability of diseases, colon seperated (classified: not classified)> <.........files to check>"

# go through each geo group
for i in range(6,len(sys.argv)):
	f = open(sys.argv[i])

	# check each individual in the population
	for line in f:

		temp = map(int,line.split())
		sub = {}

		# load subject ont a dictionary
		for j in range(len(temp)/2):
			sub[temp[j*2]] = temp[j*2+1]

		# see if it applies to any classifier
		for c in classifier:

			status = 1
			for j in range(len(c)/2):
				try:
					if sub[c[j*2]] != c[j*2+1]:
						status = 0
						break
				except:
					if eve[c[j*2]] != c[j*2+1]:
						status = 0
						break
			if status == 1:
				seed = np.random.uniform(1,100000)
				if seed < 100000 * prob[0]:
					positive.write(line)
				else:
					negative.write(line)
				break

		else:
			seed = np.random.uniform(1,100000)
			if seed < 100000 * prob[1]:
				positive.write(line)
			else:
				negative.write(line)

	f.close()

positive.close()
negative.close()