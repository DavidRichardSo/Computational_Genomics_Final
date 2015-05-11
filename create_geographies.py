import sys
import os

print "Usage: <cp file> <number of geographic populations>"

f = open(sys.argv[1], 'r')
num_geo = int(sys.argv[2])
fileList = []

for i in range(num_geo):
	fileList.append(open("geo_group_" + str(i) + ".dat",'w'))

enum = 0
for line in f:
	fileList[enum].write(line)
	enum += 1
	if enum == num_geo:
		enum = 0

f.close()