import sys
import matplotlib.pyplot as plt

print "Usage: <population file...>"

counts  = {}
population_size = 0.0
for j in range(1,len(sys.argv)):
	f = open(sys.argv[j],'r')

	for line in f:
		population_size += 1
		temp = line.strip().split()
		for i in range(len(temp)/2):
			try:
				counts[(temp[i*2], temp[i*2 + 1])][j-1] += 1
			except:
				counts[(temp[i*2], temp[i*2 + 1])] = [0] * (len(sys.argv) - 1)
				counts[(temp[i*2], temp[i*2 + 1])][j-1] += 1

	f.close()

output = []
for key in counts:
	val = min(counts[key])
	output.append([val,key,counts[key]])
output.sort()

percentages = {}

for i in output:
	if i[0] > 0:
		print i[1], " ", i[0], "       ", i[2]
	try:
		percentages[(i[2][0]+i[2][1])/population_size] += 1
	except:
		percentages[(i[2][0]+i[2][1])/population_size] = 1

for per in percentages:
	print i, " ", percentages[per]

x_dat = sorted(percentages.keys())
y = [percentages[x]/float(len(output)) for x in x_dat]

plt.plot(x_dat,y,'ro')
plt.axis([0,1,0,.02])
plt.ylabel('P2: Percentage of total mutations that are shared by P1 percent of humans')
plt.xlabel('P1: Percentage of humans that share mutation')
plt.show()