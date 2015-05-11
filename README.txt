David So
Human Evolution Simulator

Note: Before beginning any simulation, you must create an empty eve file

========
REQUIRES
========

numpy
autograd
schikit learn
matplotlib

==============
PYTHON SCRIPTS
==============

analyze_population.py: Provides file analytics (prints out mutation and count and graph)
Usage: <population file>

cluster_log_reg.py: Applies standard logistic regression and clustered logistic regression to pos and neg files
Usage:  <eve file> <positive class file> <negative class file> <genome length> <test_percent> <k mean k>

create_geographies.py: Creates geographic group files from first argument file
Usage: <file to split> <number of geographic populations>

gen_lib_fast.py: Holds loadeve

initialize_population_fast.py: Creates first population of people (one mutational generation away from eve)
Usage: <eve file name> <current generation file name> <previous generation file name> <population size> <genome size> <mutation rate>

joint_analysis.py: Analyzes the sahred mutations between different geo groups
Usage: <population files...>

log_reg_fast.py Performs standard logistic regression (used for explicit case)
Usage: <eve file> <positive class file> <negative class file> <genome length> <test_percent>

mix_geogroups.py: Moves subjects betweeen geo_groups
Usage: <group 1 file> <group 2 file> <migration 1:2 prob> <migration 2:1 prob>

probabalistic_disease_class_fast.py: Creates positive and negative lael files for some probabalistic disease
Usage: <eve file> <positive file name> <negative file name> <disease string: commas in sets, sets broken with colons> <probability of diseases, colon seperated (classified: not classified)> <.........files to check>

quick_stat.py: Reports current eve size and number of humans in population
Usage: <eve file> <current population file>

simulate_generations.py: simulates generations of reproduction
Usage: <eve.dat> <current population file name> <previous population file name> <reproduction rate> <genome size> <mutation rate> <recombination rate> <generation number>

============
BASH SCRIPTS
============

benchmark_time.sh: skeleton of script used for performance benchmarking

test.sh: skeleton of script used to run classsifiction tests

run_demo.sh: example of population generation (with mobility)





