#s-S inventory simulator
#By MammothRider
#11-21-2015
#
#Version 0.01
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class cInventory:
	def __init__(self, small, large, initial, holdingcost, order, price, penalty, checktime, testtime):
		self.small = small
		self.large = large
		self.holdingcost  = holdingcost
		self.orderingcost = order
		self.price = price
		self.penalty = penalty
		self.testtime  = testtime
		self.checktime = checktime
		self.totalcost = 0
		self.result = []
		self.inventory = initial
		
	def simulator(self):
		orderflag = 0
		orderquan = 0
		for i in range(self.testtime):
			#incoming inventory
			if orderflag == 1:
				self.inventory += orderquan
			orderflag -= 1
			
			#demand
			demand = int(random.gauss(45678.27, 2216.36))
			self.inventory -= demand
			
			if self.inventory < 0:
				self.totalcost -= self.inventory * self.penalty
				self.inventory = 0
			
			if self.inventory < self.small and orderflag <= 0 and i % self.checktime == 0:
				orderquan = self.large - self.inventory
				orderflag = random.randint(1, 2)
				self.totalcost += orderquan * self.price + self.orderingcost
			
			self.totalcost += self.inventory * self.holdingcost
			#print(self.inventory, demand, self.totalcost)
			self.result.append((self.inventory, self.totalcost))
		return self.totalcost
			
	def output(self):
		f = open("{}_{}_{}.txt".format(self.small, self.large, self.checktime), "w")
		for i in range(len(self.result)):
			f.write("{}, {}\n".format(self.result[i][1], self.result[i][1]))
		f.close()
	
	def showresult(self):
		for i in range(len(self.result)):
			print("{}, {}".format(self.result[i][1], self.result[i][1]))
	
	def returnresult(self):
		return self.result
			
			
if __name__ == '__main__':
	#def __init__(self, small, large, initial, holdingcost, order, price, penalty, checktime, testtime):
	#small = 80000
	#large = 160000
	initial = 160000
	holdingcost = 0.4
	order = 10000
	price = 1
	penalty = 10
	checktime = 1
	time = 500
	mincost = 0
	minlarge = 0
	minsmall = 0
	x = []
	y = []
	z = []
	
	fig = plt.figure()
	
	ax = fig.add_subplot(111, projection = "3d")
	ax.set_title("checktime = {}".format(checktime))
	
	testtime = 20
	step = 1500
	for t in range(testtime):
		print("testtime {}".format(t))
		count = 0
		for large in range(90000, 201500, step):
			for small in range(45000, large, step):
				inv = cInventory(small, large, large, holdingcost, order, price, penalty, checktime, time)
				cost = inv.simulator()
				if t == 0:
					x.append(large)
					y.append(small)
					z.append(cost)
				else:
					z[count] += cost
					count += 1
				#inv.output()
				
	for i in range(len(z)):
		z[i] = z[i]/testtime
		if z[i] < mincost or mincost == 0:
			mincost = z[i]
			minlarge = x[i]
			minsmall = y[i]
			
	
	print(mincost, minlarge, minsmall)
	
	cm = plt.cm.get_cmap("RdYlGn_r")
	
	x = np.array(x)
	y = np.array(y)
	z = np.array(z)
	a = ax.plot_trisurf(x, y, z, cmap=cm, linewidth=0)
	ax.set_xlabel('Large S')
	ax.set_ylabel('Small S')
	ax.set_zlabel('Total Cost')
	#a = ax.scatter(x, y, z, cmap = cm, c = z, marker = ".")
	plt.colorbar(a)
	plt.show()
	