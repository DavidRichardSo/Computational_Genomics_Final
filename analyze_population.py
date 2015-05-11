import sys
import matplotlib.pyplot as plt

print "Usage: <population file>"

f = open(sys.argv[1],'r')
counts  = {}
population_size = 1.0

for line in f:
	population_size += 1
	temp = line.strip().split()
	for i in range(len(temp)/2):
		try:
			counts[(temp[i*2], temp[i*2 + 1])] += 1
		except:
			counts[(temp[i*2], temp[i*2 + 1])] = 1

f.close()

output = []
for key in counts:
	output.append([counts[key],key])
output.sort()

percentages = {}

for i in output:
	print i[1], " ", i[0]
	try:
		percentages[i[0]/population_size] += 1
	except:
		percentages[i[0]/population_size] = 1

for per in percentages:
	print i, " ", percentages[per]

print percentages

x_dat = sorted(percentages.keys())
y = [percentages[x]/float(len(output)) for x in x_dat]

plt.plot(x_dat,y,'ro')
plt.axis([0,1,0,.02])
plt.ylabel('P2: Percentage of total mutations that are shared by P1 percent of humans')
plt.xlabel('P1: Percentage of humans that share mutation')
plt.show()