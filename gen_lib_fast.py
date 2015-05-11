# Loads Eve from file and returns a list of her genome as a list
def loadEve(file_name):
	f = open(file_name,'r')
	temp = map(int,f.readline().strip().split())
	output = {}
	for i in range(len(temp)/2):
		output[temp[i*2]] = temp[i*2+1]
	return output