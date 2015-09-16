#queue.py
import numpy as np
import matplotlib.pyplot as plt

class queue:
	def __init__(self, maxTime = 1000):
		self.customer = [ \
						(3, 4.5), \
						(3, 4), \
						(2, 2), \
						(4, 2), \
						(6, 4), \
						(2, 3), \
						(4, 4), \
						(8, 6), \
						(4, 4), \
						(5, 3), \
						]
		self.queue = []
		self.timer = 0
		self.timeTable = [] #record in queue customer (time, customer)
		self.waitTime = 0
		self.spentTimeover45 = 0
		self.emptyTime = 0
		self.moreThanOne = 0
		self.totalCustomers = 0
		self.maxTime = maxTime
		
	def chechAvail(self):
		#return 1 means full, 0 means avail, -1 means empty.
		pass
	
	def setServer(self, down):
		#count down
		pass
	
	def newServer(self, time):
		#new customer
		pass
		
	def countServer(self):
		pass
	
	def returnNextServerTime(self):
		pass
	
	def queueFindCustomer(self):
		#return a customer servering time and remove it.
		pass
		
	def countSpent(self, customer):
		outTime = self.timer + customer[1]
		outTime = min(outTime, self.maxTime)
		inTime = customer[0]
		if outTime - inTime > 4.5:
			self.spentTimeover45 += 1
			
	def checkQueueWaitTime(self):
		for i in self.queue:
			if i[0] - self.maxTime > 4.5:
				self.spentTimeover45 += 1
	
	def printData(self):
		print "Total Customer: ", self.totalCustomers
		print "Total Waiting Time: ", self.waitTime
		print "Over 4.5: ", self.spentTimeover45
		print "Empty Time: ", self.emptyTime
		print "More Than One Time: ", self.moreThanOne
	
	def eventPush(self):
		#run the timer to next event
		tc = (-1, -1)
		if self.customer:
			tc = self.customer.pop(0)
		tr = self.returnNextServerTime()
		if tc[0] > 0 and tr > 0:
			diff = min(tc[0], tr)
		else:
			diff = max(tc[0], tr)
		
		print "------------------------------------"
		if diff < 0 and len(self.queue) == 0:
			print "Simulation Finished."
			self.printData()
			return 1
		if self.timer + diff > self.maxTime:
			print "Time Up."
			diff = self.maxTime - self.timer
			self.waitTime += diff * len(self.queue)
			if self.chechAvail() < 0 and len(self.queue) == 0:
				self.emptyTime += diff
			if len(self.queue) > 1:
				self.moreThanOne += diff
			self.checkQueueWaitTime()
				
			self.printData()
			return 1
		
		self.timer += diff
		print "Time: ", self.timer
		self.waitTime += diff * len(self.queue)
		if self.chechAvail() < 0 and len(self.queue) == 0:
			self.emptyTime += diff
		if len(self.queue) > 1:
			self.moreThanOne += diff
		
		self.setServer(diff)
		if tc[0] - diff == 0:
			self.queue.append((self.timer, tc[1]))
			self.totalCustomers += 1
			print "A new customer %d enter the queue. Queue: %d, Customer: %d" %(tc[1], len(self.queue), len(self.customer))
		elif tc[0] > 0:
			self.customer.insert(0, (tc[0]-diff, tc[1]))
			print "No customer enter the queue. Queue: %d, Customer: %d" %(len(self.queue), len(self.customer))
		else:
			print "No customer. Queue: %d, Customer: %d" %(len(self.queue), len(self.customer))
			
		if self.chechAvail() <= 0:
			while self.chechAvail() <= 0 and len(self.queue) > 0:
				tt = self.queueFindCustomer()
				self.newServer(tt)
				print "A customer %d receive service. Queue: %d, Customer: %d" %(tt, len(self.queue), len(self.customer))
		
		self.timeTable.append((self.timer, len(self.queue) + self.countServer()))
			
		return 0
	
	def printCustomer(self):
		print self.customer
		
	def plotTimeTable(self):
		ax = plt.subplot(111)

		b = (0, 0)
		maxy = 0
		for i in self.timeTable:
			plt.plot((b[0], i[0]), (b[1], b[1]), "k-")
			plt.plot((i[0], i[0]), (b[1], i[1]), "k-")
			b = i
			if i[1] > maxy:
				maxy = i[1]
				
		plt.plot((i[0], i[0]), (i[1], 0), "k-")
		
		#plt.plot(x, y, "ro-")
		plt.plot((30, 30), (0, maxy + 0.5), "k--")
		#print y[500]
		ax.set_xticks(np.linspace(0, 50, 11))
		#ax.set_yticks(np.linspace(0, 2, 11))
		plt.show()
		
class FCFS(queue):
	def __init__(self, maxTime = 1000):
		queue.__init__(self, maxTime)
		self.server = -1
	
	def chechAvail(self):
		#0 means avail, -1 means empty.\
		return self.server
	
	def setServer(self, down):
		#count down
		self.server -= down
		if self.server == 0:
			print "A customer finished."
			self.server = -1
			
	def countServer(self):
		if self.server > 0:
			return 1
		return 0
	
	def newServer(self, time):
		#new customer
		self.server = time
		
	def returnNextServerTime(self):
		return self.server
		
	def queueFindCustomer(self):
		#return a customer servering time and remove it.
		if self.queue:
			t = self.queue.pop(0)
			self.countSpent(t)
			return t[1]
		else:
			return -1
			
class twoFCFS(queue):
	def __init__(self, maxTime = 1000):
		queue.__init__(self, maxTime)
		self.server1 = -1
		self.server2 = -1
	
	def chechAvail(self):
		#return nearest server time, 0 means avail, -1 means empty.\
		if self.server1 <= 0 and self.server2 <= 0:
			return -1
		elif self.server1 > 0 and self.server2 > 0:
			return min(self.server1, self.server2)
		else:
			return 0
	
	def setServer(self, down):
		#count down
		self.server1 -= down
		self.server2 -= down
		if self.server1 == 0 or self.server2 == 0:
			print "A customer finished."
	
	def countServer(self):
		if self.server1 > 0 and self.server2 > 0:
			return 2
		elif self.server1 <= 0 and self.server2 <= 0:
			return 0
		else:
			return 1
	
	def newServer(self, time):
		#new customer
		if self.server1 > 0 and self.server2 > 0:
			print "ERROR"
			exit()
		elif self.server1 > 0:
			self.server2 = time
		else:
			self.server1 = time
	
	def returnNextServerTime(self):
		if self.server1 > 0 or self.server2 > 0:
			return max(self.server1, self.server2)
		return -1
	
	def queueFindCustomer(self):
		#return a customer servering time and remove it.
		if self.queue:
			t = self.queue.pop(0)
			self.countSpent(t)
			return t[1]
		else:
			return -1
			
class SPT(FCFS):
	def queueFindCustomer(self):
		#return a customer servering time and remove it.
		t = 0
		if self.queue:
			for i in range(len(self.queue)):
				if self.queue[i][1] < self.queue[t][1]:
					t = i
			t = self.queue.pop(t)
			self.countSpent(t)
			return t[1]
		else:
			return -1
		
if __name__ == '__main__':
	#a = FCFS()
	#a = FCFS(30)
	#a = twoFCFS()
	#a = FCFS(30)
	#a = SPT()
	a = SPT(30)
	while not a.eventPush():
		pass
	a.plotTimeTable()