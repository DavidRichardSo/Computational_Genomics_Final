import sys
import random
import numpy as np
import gen_lib_fast as gl

print "Usage: <eve file name> <current generation file name> <previous generation file name> <population size> <genome size> <mutation rate>"

# unloading
eve_file = open(sys.argv[1],'w')
f = open(sys.argv[2], 'w')
t = open(sys.argv[3], 'w')
population_size = int (sys.argv[4])
genome_size = int (sys.argv[5])
mutation_rate = float (sys.argv[6])

base_pairs = np.array([1, 2, 3, 4])

eve = {}

for i in xrange(population_size):
	num_mutations = np.random.binomial(genome_size, mutation_rate)
	mutation_indecies = random.sample(xrange(0,genome_size), num_mutations)
	if (mutation_indecies):
		mutation_indecies.sort()
	for j in mutation_indecies:
		if j in eve:
			temp_array = np.array([eve[j]])
			temp_array = np.setdiff1d(base_pairs, temp_array) # make sure mutations are true mutations
			mutation_value = np.random.choice(temp_array,1)[0]
			f.write(str(j) + " " + str(mutation_value) + " ")
		else:
			eve[j] = np.random.choice(base_pairs,1)[0]
			temp_array = np.array([eve[j]])
			temp_array = np.setdiff1d(base_pairs, temp_array) # make sure mutations are true mutations
			mutation_value = np.random.choice(temp_array,1)[0]
			f.write(str(j) + " " + str(mutation_value) + " ")
	f.write("\n")

f.close()

t.write("Intentionally Left Blank")
t.close()

for i in eve:
	eve_file.write(str(i) + " " + str(eve[i]) + " ")

eve_file.close()