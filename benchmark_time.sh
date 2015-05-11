#!/bin/bash

# statics
genome_length=3000000000
mutation_rate=.000000025
recombination_rate=.000000013

init_pop=( 10 )
reproduction_rate=( 1.05 )
generations=( 200 300 400 500 )

for pop in "${init_pop[@]}"
	do
		for gen in "${generations[@]}"
			do
				for rep in "${reproduction_rate[@]}"
					do
						rm -f *.dat
						touch eve.dat
						echo "=========" >> benchmark_results.data
						echo "New Trial" >> benchmark_results.data
						echo "=========" >> benchmark_results.data
						echo >> benchmark_results.data
						echo "Init Pop: $pop, Generations: $gen, Reproduction rate: $rep" >> benchmark_results.data
						python initialize_population_fast.py eve.dat cg.dat pg.dat $pop $genome_length $mutation_rate
						(time python simulate_generations.py eve.dat cg.dat pg.dat $reproduction_rate $genome_length $mutation_rate $recombination_rate $gen) >> benchmark_results.data 2>&1
						echo >> benchmark_results.data
						python quick_stat.py eve.dat cg.dat >> benchmark_results.data
						echo >> benchmark_results.data
					done
			done
	done

