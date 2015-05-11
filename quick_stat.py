import sys
import gen_lib_fast as gl

eve = gl.loadEve(sys.argv[1])
f = open(sys.argv[2],'r')

count = 0
for line in f:
	count += 1

f.close()

print "Eve length:", len(eve.keys()), "Number of humans:", count