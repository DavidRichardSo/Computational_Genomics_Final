import sys
import math
import gen_lib_fast as gl
import copy
import decimal
import numpy as np
from sklearn import linear_model, datasets
from sklearn.cluster import KMeans

global y_neg_start, index_guide

# can be done with a hash map for eve instead
def mut_to_binary(data_matrix,row_index,gene):
	global index_guide

	if len(gene) == 0:
			return

	gene.sort()

	cur_index = 0
	for col_index in xrange(len(index_guide)):
		if index_guide[col_index] == gene[cur_index][0]:
			data_matrix[row_index,col_index] = gene[cur_index][1]
			cur_index += 1
			if cur_index >= len(gene):
				break

def get_y(index):
	global y_neg_start
	if index < y_neg_start:
		return 1
	return 0

try: 
	eve = gl.loadEve(sys.argv[1])
	positive = open(sys.argv[2],'r')
	negative = open(sys.argv[3],'r')
	genome_length = int(sys.argv[4])
	test_percent = float(sys.argv[5])
	k_val = int(sys.argv[6])
except:
	print "Usage: <eve file> <positive class file> <negative class file> <genome length> <test_percent> <k mean k>"
	sys.exit()

dimensions=len(eve.keys())
index_guide = sorted(eve.keys())

pos_num = 0
neg_num = 0

for line in positive:
	pos_num += 1

for line in negative:
	neg_num += 1

positive.seek(0)
negative.seek(0)

# train_seed = int( * (1 - test_percent))
# train_index = np.random.randint(len(x),size=train_seed)
# test_index = np.setdiff1d(np.arange(len(x)),train_index)

pos_test_num = int(pos_num * test_percent) 
neg_test_num = int(neg_num * test_percent)
test_num = pos_test_num + neg_test_num
train_num = pos_num + neg_num - test_num

x_train = np.zeros((train_num,dimensions))
y_train = np.zeros(train_num)

x_test = np.zeros((test_num,dimensions))
y_test = np.zeros(test_num)

# get test data
for i in xrange(test_num):
	if i < pos_test_num:
		line = map(int,positive.readline().strip().split())
		line = [(line[j*2],line[j*2+1]) for j in range(len(line)/2)]
		mut_to_binary(x_test,i,line)
		y_test[i] = 1
	# time to do the negatives
	else:
		line = map(int,negative.readline().strip().split())
		line = [(line[j*2],line[j*2+1]) for j in range(len(line)/2)]
		mut_to_binary(x_test,i,line)

# get training data
for i in xrange(train_num):
	if i < pos_num - pos_test_num:
		line = map(int,positive.readline().strip().split())
		line = [(line[j*2],line[j*2+1]) for j in range(len(line)/2)]
		mut_to_binary(x_train,i,line)
		y_train[i] = 1
	# time to do the negatives
	else:
		line = map(int,negative.readline().strip().split())
		line = [(line[j*2],line[j*2+1]) for j in range(len(line)/2)]
		mut_to_binary(x_train,i,line)

logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(x_train,y_train)

y_prime = logreg.predict(x_test)
count = 0.0
correct_count = 0.0
for boo in y_prime == y_test:
	count += 1
	if boo:
		correct_count += 1

print "Standard Logistic Regression:", correct_count/count

kmeans = KMeans(init='k-means++', n_clusters=k_val, n_init=10)
kmeans.fit(x_train) # make two different subgroups
train_labels_mask = kmeans.labels_ # these labels
test_labels_mask = kmeans.predict(x_test)

train_labels = np.where(train_labels_mask)
not_train_labels = np.where([i ^ 1 for i in train_labels_mask])

test_labels = np.where(test_labels_mask)
not_test_labels = np.where([i ^ 1 for i in test_labels_mask])

cluster_x_train_0 = x_train[not_train_labels]
cluster_y_train_0 = y_train[not_train_labels]
cluster_x_train_1 = x_train[train_labels]
cluster_y_train_1 = y_train[train_labels]

cluster_x_test_0 = x_test[not_test_labels]
cluster_x_test_1 = x_test[test_labels]
cluster_y_test_0 = y_test[not_test_labels]
cluster_y_test_1 = y_test[test_labels]

# first classify 0'
logreg.fit(cluster_x_train_0,cluster_y_train_0)
y_prime_0 = logreg.predict(cluster_x_test_0)

count = 0.0
correct_count = 0.0
for boo in y_prime_0 == cluster_y_test_0:
	count += 1
	if boo:
		correct_count += 1

logreg.fit(cluster_x_train_1,cluster_y_train_1)
y_prime_1 = logreg.predict(cluster_x_test_1)

for boo in y_prime_1 == cluster_y_test_1:
	count += 1
	if boo:
		correct_count += 1

print
print "Clustered Logistic Regression:", correct_count/count



