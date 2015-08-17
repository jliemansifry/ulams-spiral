import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

num = 255**2 # must be an odd square so that 1 is in the center of image, generator "prime" will generate primes up to this num

def prime(num):
	factors = []
	for n in np.arange(1, num**.5+1, 1):
		if (num % n == 0) and (n not in factors):
			factors += [n] + [num/float(n)]
	#print np.unique(np.sort(factors))
	#could yield this list of ordered factors too if desired
	if len(np.unique(factors)) == 2: 
		yield num

def write_primes(num): # return the array of all primes up to specified num. good for efficiency analysis with %timeit also
	all_primes = []
	for i in range(num):
		for newprime in prime(i):
			all_primes += [newprime]
	return all_primes
all_primes = write_primes(num)

def double_primes(): #primes that have a neighbor 2 away
	for i in range(len(all_primes)-1):
		if all_primes[i] + 2 == all_primes[i+1]:
			yield all_primes[i],all_primes[i+1]

doubles = [] 
for low_double,high_double in double_primes():
	doubles += [low_double] + [high_double]
doubles = np.unique(doubles)
#overlap_index = np.searchsorted(all_primes,doubles) #not needed for ulams spiral, but is for other types of plotting I was playing with...


### ULAMS SPIRAL PLOTTING ###
prime_img = np.zeros((num**.5,num**.5)) # set img size

how_many_moves = np.repeat(np.arange(1,float(num)/num**0.5),2) # the number of moves in each direction necessary counting around... goes 1, 1, 2, 2, 3, 3, etc. 
how_many_moves = np.append(how_many_moves,[num**.5 - 1]) #add the last number again to complete the square
moves = itertools.cycle([[0, 1], [1,  0], [0, -1], [-1, 0]])
all_moves = [np.tile(moves.next(),(i,1)) for i in how_many_moves] 
np.insert(all_moves,moves.next(),1)

count = 1
loc = [np.floor(num**.5/2.),np.floor(num**.5/2.)] #starting loc, at the center of the image
for i in range(len(all_moves)):
	for j in np.arange(0,len(all_moves[i]),1):
		if count in all_primes: #set the color if the count is a prime
			prime_img[loc[0],loc[1]] = 1
		if count in doubles: #modify the color if the prime has a neighbor
			prime_img[loc[0],loc[1]] = 2
		loc += all_moves[i][j]
		count += 1
if count + 1 in all_primes: # for completeness even though last index will never be prime (ie. never any primes on this diagonal, it is the "square" diagonal, ie 9, 25, 49, 81, etc.)
	prime_img[loc[0],loc[1]] = 1

im = plt.pcolormesh(prime_img,cmap=cm.hot)
plt.xlim(0,num**.5) #set logical boundaries
plt.ylim(0,num**.5)
plt.gca().set_aspect('equal', adjustable='box')
plt.xticks([])
plt.yticks([])
plt.savefig('/Users/jliemansifry/Desktop/UlamsSpiral_255x255_200dpi',dpi=200)
plt.show()
