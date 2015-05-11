import os
import sys
import random
import numpy as np
import gen_lib_fast as gl

global parents
global gen_num

def run_generation(eve, pg_fname, cg_fname, reproduction_rate, genome_size, mutation_rate, recombination_rate, run_number):

	global parents
	global gen_num

	# load previous generation into memory
	if len(parents) == 0:
		# make current population the previous population
		# os.rename(cg_fname, pg_fname)
		parents =[]
		f = open(cg_fname,"r")
		for line in f:
			temp = map(int, line.strip().split())
			out = {}
			for i in range(len(temp)/2):
				out[temp[i*2]] = temp[i*2 + 1]
			parents.append(out)
		f.close()
	current_pop = len(parents)

	# new generation file (cg.dat)
	if gen_num == run_number + 1:
		out_file = open(cg_fname,"w")

	base_pairs = np.array([1, 2, 3, 4])

	num_offspring = int (reproduction_rate * current_pop)
	if reproduction_rate > 1 and num_offspring==current_pop:
		num_offspring += 1

	children = []

	for i in xrange(num_offspring):

		#first pick parents
		par = random.sample(xrange(0,current_pop), 2)

		# find recombination spots
		num_recombinations = np.random.binomial(genome_size-1,recombination_rate)
		recombination_indecies = random.sample(xrange(1,genome_size), num_recombinations)
		recombination_indecies.append(genome_size+1)
		recombination_indecies.sort()

		gene = {}

		# first parent
		in_recomb = 1
		j = 0
		upper_limit = recombination_indecies[j]

		for mut_site in sorted(parents[par[0]].keys()):
			if mut_site < upper_limit:
				if in_recomb == 1:
					gene[mut_site] = parents[par[0]][mut_site]
			else:
				while (mut_site >= upper_limit):
					in_recomb = in_recomb ^ 1
					j += 1
					upper_limit = recombination_indecies[j]

				if in_recomb == 1:
					gene[mut_site] = parents[par[0]][mut_site]

		# second parent
		in_recomb = 0
		j = 0
		upper_limit = recombination_indecies[j]

		for mut_site in sorted(parents[par[1]].keys()):
			if mut_site < upper_limit:
				if in_recomb == 1:
					gene[mut_site] = parents[par[1]][mut_site]
			else:
				while (mut_site >= upper_limit):
					in_recomb = in_recomb ^ 1
					j += 1
					upper_limit = recombination_indecies[j]

				if in_recomb == 1:
					gene[mut_site] = parents[par[1]][mut_site]

		# # assume father first parent
		# father_set = []
		# for j in xrange((len(recombination_indecies)/2)):
		# 	father_set.append([recombination_indecies[j*2], recombination_indecies[j*2+1]])

		# mother_set = []
		# for j in xrange(((len(recombination_indecies)-1)/2)):
		# 	mother_set.append([recombination_indecies[j*2+1], recombination_indecies[j*2+2]])

		# # recombination_index = random.sample(xrange(0,genome_size-1), 1)[0]

		# #create new crossbread gene
		# gene = {}
		# #father 
		# for mut in parents[par[0]]:
		# 	for bound in father_set:
		# 		if mut >= bound[0] and mut < bound[1]:
		# 			gene[mut] = parents[par[0]][mut]
		# 			break
		# for mut in parents[par[1]]:
		# 	for bound in mother_set:
		# 		if mut >= bound[0] and mut < bound[1]:
		# 			gene[mut] = parents[par[1]][mut]
		# 			break

		# add mutations
		num_mutations = np.random.binomial(genome_size, mutation_rate)
		mutation_indecies = random.sample(xrange(0,genome_size), num_mutations)
		for j in mutation_indecies:
			if j in gene.keys():
				temp_array = np.array(gene[j])
				temp_array = np.setdiff1d(base_pairs, temp_array)

				# remove mutations that return to Eve state
				mutation = np.random.choice(temp_array,1)[0]
				try:
					if mutation == eve[j]:
						gene.pop(mut_site,None)
					else:	
						gene[j] = mutation
				except:
					gene[j] = mutation
				break

			# mutation at new site
			else:
				# eve has data point at site
				try:
					temp_array = np.array([eve[j]])
					temp_array = np.setdiff1d(base_pairs, temp_array) # make sure mutations are true mutations
					gene[j] = np.random.choice(temp_array,1)[0]

				# eve does not have data point
				except:
					eve[j] = np.random.choice(base_pairs,1)[0]
					temp_array = np.array([eve[j]])
					temp_array = np.setdiff1d(base_pairs, temp_array) # make sure mutations are true mutations
					gene[j] = np.random.choice(temp_array,1)[0]

		if gen_num == run_number + 1:
			for mut in gene:
				out_file.write(str(mut) + " " + str(gene[mut]) + " ")
			out_file.write("\n")
		else:
			children.append(gene)

	if gen_num == run_number + 1:
		out_file.close()
	else:
		parents = children

# print "Usage: <eve file name> <current generation file name> <previous generation file name> <reproduction rate> <genome size> <mutation rate> <recombination rate> <number of generations>" 

# Load eve
eve = gl.loadEve(sys.argv[1])

# Move current population file to old population file
cg_fname = sys.argv[2]
pg_fname = sys.argv[3]
reproduction_rate = float (sys.argv[4])
genome_size = int (sys.argv[5])
mutation_rate = float (sys.argv[6])
recombination_rate = float(sys.argv[7])
gen_num = int(sys.argv[8])

parents = []

for i in range(gen_num):
	# print i
	# print len(eve.keys())
	run_generation(eve, pg_fname, cg_fname, reproduction_rate, genome_size, mutation_rate, recombination_rate, i)

# write out eve
f = open(sys.argv[1],'w')
for mut in eve:
	f.write(str(mut) + ' ' + str(eve[mut]) + ' ')
f.close()
# print "Eve Size:", len(eve.keys())
