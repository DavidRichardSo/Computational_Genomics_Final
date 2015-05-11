#!/bin/bash

genome_length=3000000000
mutation_rate=.000000025
reproduction_rate=1.0
geo_generations=10
recombination_rate=.000000013
init_generations=10
init_pop=100
disease_prob="1:0"
num_geo=2

rm -f *.dat
touch eve.dat
python initialize_population_fast.py eve.dat cg.dat pg.dat $init_pop $genome_length $mutation_rate
time python simulate_generations.py eve.dat cg.dat pg.dat $reproduction_rate $genome_length $mutation_rate $recombination_rate $init_generations
python create_geographies.py cg.dat $num_geo
for ((i=0; i<$num_geo; i++));
do
	python simulate_generations.py eve.dat "geo_group_$i.dat" pg.dat $reproduction_rate $genome_length $mutation_rate $recombination_rate $geo_generations
done
python mix_geogroups.py geo_group_0.dat geo_group_1.dat .2 .2
for ((i=0; i<$num_geo; i++));
do
	python simulate_generations.py eve.dat "geo_group_$i.dat" pg.dat $reproduction_rate $genome_length $mutation_rate $recombination_rate $geo_generations
done

# need to analyze the data to make sure valid disease choice
# python analyze_population.py geo_group_0.dat
# python analyze_population.py geo_group_1.dat
# python joint_analysis.py geo_group_*
# echo "Choose classification types"
# read pos_class
# python probabalistic_disease_class_fast.py eve.dat positive.dat negative.dat $pos_class $disease_prob geo_group_* 
# python probabalistic_disease_class_fast.py eve.dat positive_0.dat negative_0.dat $pos_class $disease_prob geo_group_0.dat
# python probabalistic_disease_class_fast.py eve.dat positive_1.dat negative_1.dat $pos_class $disease_prob geo_group_1.dat

# classification
# python cluster_log_reg.py eve.dat positive.dat negative.dat $genome_length .1
# python my_broken_logistic_regression.py eve.dat positive_0.dat negative_0.dat 300 .1
# python my_broken_logistic_regression.py eve.dat positive_1.dat negative_1.dat 300 .1  ('1365507161', '3')   14

