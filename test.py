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
			pen = 0
			hol = 0
			imp = 0
			#incoming inventory
			if orderflag == 1:
				self.inventory += orderquan
			orderflag -= 1
			
			#demand
			demand = int(random.gauss(45678.27, 2216.36))
			self.inventory -= demand
			
			if self.inventory < 0:
				pen = 0 - self.inventory * self.penalty
				neginv = self.inventory
				self.inventory = 0
			
			if self.inventory < self.small and orderflag <= 0 and i % self.checktime == 0:
				orderquan = self.large - self.inventory
				orderflag = random.randint(1, 2)
				imp = orderquan * self.price + self.orderingcost
			
			hol = self.inventory * self.holdingcost
			self.totalcost += pen + hol + imp
			#print(self.inventory, demand, pen, hol, imp, self.totalcost)
			if self.inventory > 0:
				self.result.append((self.inventory, self.totalcost))
			else:
				self.result.append((neginv, self.totalcost))
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
	small = 85000
	large = 140000
	initial = large
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
	ax1 = fig.add_subplot(211)
	ax1.set_title("Inventory")
	
	inv = cInventory(small, large, large, holdingcost, order, price, penalty, checktime, time)
	inv.simulator()
	result = inv.returnresult()
	x = [i for i in range(len(result)+1)]
	y = [result[i][0] for i in range(len(result))]
	y = [large] + y
	
	for i in range(1, len(x)):
		ax1.plot([x[i - 1], x[i]], [y[i - 1], y[i - 1]], 'b-')
		ax1.plot([x[i], x[i]], [y[i - 1], y[i]], 'b-')
	ax1.plot([0, 500], [0, 0], 'k--')

	ax2 = fig.add_subplot(212)
	ax2.set_title("Positive Inventory")
	
	for i in range(len(y)):
		if y[i] < 0:
			y[i] = 0
	
	for i in range(1, len(x)):
		ax2.plot([x[i - 1], x[i]], [y[i - 1], y[i - 1]], 'b-')
		ax2.plot([x[i], x[i]], [y[i - 1], y[i]], 'b-')
	
	plt.show()