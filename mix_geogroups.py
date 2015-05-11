import sys
import os
import numpy as np

try:
	geo_1_fname = sys.argv[1]
	geo_2_fname = sys.argv[2]	
	mig_prob1 = float(sys.argv[3])
	mig_prob2 = float(sys.argv[4])
except:
	print "Usage: <group 1 file> <group 2 file> <migration 1:2 prob> <migration 2:1 prob>"

os.rename(geo_1_fname,'temp1')
os.rename(geo_2_fname,'temp2')

geo_1 = open(geo_1_fname,'w')
geo_2 = open(geo_2_fname,'w')
t1 = open('temp1', 'r')
t2 = open('temp2', 'r')

# move through first population
for line in t1:
	seed = np.random.uniform(1,100000)
	if seed < 100000 * mig_prob1:
		geo_1.write(line)
	else:
		geo_2.write(line)

for line in t2:
	seed = np.random.uniform(1,100000)
	if seed < 100000 * mig_prob2:
		geo_2.write(line)
	else:
		geo_1.write(line)

geo_1.close()
geo_2.close()
t1.close()
t2.close()
