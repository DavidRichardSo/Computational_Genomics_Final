#!/bin/bash

genome_length=3000000000
mutation_rate=.000000025
reproduction_rate=1.0
geo_generations=100
recombination_rate=.000000013
init_generations=20
init_pop=1000
disease_prob="1:0"
num_geo=2
test_percent=.2

python joint_analysis.py geo_group_*
echo "Choose classification types"
read pos_class

python probabalistic_disease_class_fast.py eve.dat positive.dat negative.dat $pos_class $disease_prob geo_group_* 
for ((i=0; i<$num_geo; i++));
do
	python probabalistic_disease_class_fast.py eve.dat "positive_$i.dat" "negative_$i.dat" $pos_class $disease_prob "geo_group_$i.dat"
done

# classification
python cluster_log_reg.py eve.dat positive.dat negative.dat $genome_length .1 $num_geo
for ((i=0; i<$num_geo; i++));
do
	python log_reg_fast.py eve.dat "positive_$i.dat" "negative_$i.dat" $genome_length $test_percent
done