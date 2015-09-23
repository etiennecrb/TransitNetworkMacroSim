#!/usr/bin/python
# -*- coding: utf-8 -*-

# Corridor.py

from OD import *

class Corridor():
	""" Contains the characteristics of the corridor.
	
		Attributes :
			- name -- Name of the corridor/scenario
			- length -- Length in km
			- demand -- A list of OD instances
			- lines -- A list of Line instances
			- typo -- An integer describing the typology (0 for homogenous,
				1 for city center and 2 for interurban). To add some typology models,
				modify the method SetTypology.
			- n -- Number of zones
			- zone_length -- Length of each zone in km
			- landmarks -- Abscisses of zones' limits
	"""
	def __init__(self, name, length, typo):
		self.name = str(name)
		self.length = float(length)
		self.demand = []
		self.lines = []
		
		self.typo = typo
		self.n = 1
		self.zone_length = []
		self.landmarks = []
		self.SetTypology(typo)
		self.ResetDemand()
	
	
	def SetLength(self, l):
		""" Modify the length of the corridor and update the attributes of OD (trip length).
		
		Has to be used to modify the length.
		"""
		self.length = l
		self.SetTypology(self.typo) # Updating zone length and landmarks
		# Updating od (trip length)
		for od in self.demand:
			od.Update()
		
	def SetTypology(self, typo):
		""" Modify the typology of the corridor, reset the OD and update lines.
		
		Has to be used to modify the typology.
		"""
		old_typo = self.typo
		self.typo = typo
		l = self.length
		
		# Homogenous
		if self.typo == 0:
			self.zone_length = [l]
			self.landmarks = [0, l]
			self.n = 1
					
		# City center
		if self.typo == 1:
			if 0.25*l>=3:
				a = l - 3
				b = 3
			else:
				a = 0.75*l
				b = 0.25*l
			self.zone_length = [a, b]
			self.landmarks = [0, a, l]
			self.n = 2	
			
		# Interurbain
		if self.typo == 2:
			if 0.1*l>=3:
				a = 3
				b = l-2*3
				c = 3
			else:
				a = 0.1*l
				b = 0.8*l
				c = 0.1*l
			self.zone_length = [a, b, c]
			self.landmarks = [0, a, a+b, l]
			self.n = 3
			
		if typo != old_typo:
			self.ResetDemand()
			self.ResetLines()
	
	def TotalDemand(self):
		""" Returns the total level of demand. """
		r = 0
		for od in self.demand:
			r += od.demand
		return r
		
	def Demand(self, param, line):
		""" Returns the demand for the specified line according to param.
		
		The given line has to be in self.lines.
		"""
		if not (line in self.lines):
			print("Programming error : line has to be in Corridor.lines for Corridor.Demand(self, param, line)")
			return 0
		
		r = 0
		for od in self.demand:
			r += od.demand * od.ModalSplit(param, self.lines, line)
		return r
	
	def ResetDemand(self):
		""" Resets the list of OD. """
		self.demand = []
		for i in range(self.n):
			for j in range(self.n):
				self.demand.append(OD(self, i, j, 0))
	
	def ResetLines(self):
		""" Resets the list of lines. """
		self.lines = []
	
	def GetOD(self, origin, dest):
		""" Returns the asked OD object and 0 if not founded. """
		for od in self.demand:
			if od.origin == origin and od.dest == dest:
				return od
		return 0
	
	def AvgTravelTime(self, param):
		""" Computes the average travel time on all OD with the existing lines. """
		t = 0.0 # Time
		q = 0.0 # Normalization factor
		for od in self.demand:
			for line in self.lines:
				p = od.demand * od.ModalSplit(param, self.lines, line) # Number of travelers
				if p != 0 and od.TravelTime(line) == float("inf"):
					return float("inf")
				else:
					t += p * od.TravelTime(line)
					q += p
			
		if q != 0:
			return t / q
		else:
			return float("inf")
	
	def MaxLoadA(self):
		""" Returns the maximum of the sum of all OD LoadA.
		
		It is the highest number of people traveling at the same time at the same
		place on the corridor in one direction.
		"""
		m = 0 # Current maximum
		for x in range(100):
			l = 0 # Load at abscisse x
			for od in self.demand:
				l += od.LoadA(self, x*self.length/100.0)
			if l > m:
				m = l
		return m
			
	def MaxLoadB(self):
		""" Returns the maximum of the sum of all OD LoadB.
		
		It is the highest number of people traveling at the same time at the same
		place on the corridor in one direction.
		"""
		m = 0 # Current maximum
		for x in range(100):
			l = 0 # Load at abscisse x
			for d in self.demand:
				l += d.LoadB(self, x*self.length/100.0)
			if l > m:
				m = l	
		return m
	
	def WeightedTravelTime(self, param):
		""" Computes the total weighted travel time for all the demand on the whole
		network.
		"""
		wtt = 0
		for od in self.demand:
			wtt += od.demand * od.WeightedTravelTime(param, self.lines)
		return wtt
	
	def GeneralizedCost(self, param):
		""" Computes the total generalized cost for all the demand on the whole
		network.
		"""
		gc = 0
		for od in self.demand:
			gc += od.demand * od.GeneralizedCost(param, self.lines)
		return gc
				
	def OperatingCost(self, param):
		""" Computes the total operating cost of the network. """
		oc = 0
		for line in self.lines:
			oc += line.OperatingCost(param)
		return oc
	
	def InfraCost(self, param):
		""" Computes the total infrastructure cost of the network. """
		ic = 0
		for line in self.lines:
			ic += line.InfraCost(param)
		return ic
	
	def OperatorCost(self, param):
		""" Computes the total operator cost of the network (operating + infra). """
		oc = 0
		for line in self.lines:
			oc += line.OperatorCost(param)
		return oc
		
	def TotalRevenues(self, param):
		""" Computes the total revenues of all operators. """
		r = 0
		for od in self.demand:
			for line in self.lines:
				if line.m != 0:
					r += od.ModalSplit(param, self.lines, line) * od.demand * line.price
		return r
		
	def Revenues(self, param, line):
		""" Computes the revenues for the given line. """
		r = 0
		if line.m != 0:
			for od in self.demand:
				r += od.ModalSplit(param, self.lines, line) * od.demand * line.price
			return r
		else:
			return 0

	def TotalCost(self, param):
		""" Computes the total cost of the network (travelers + operators). """
		return self.GeneralizedCost(param) + self.OperatorCost(param) - self.TotalRevenues(param)

	def GetElasticDemand(self, param, corridor):
		""" Return the demand if self.lines were replaced by 
		corridor.lines and if demand was elastic.
		"""
		demand = []
		c = param.captive
		for od in self.demand:
			if od.demand == 0:
				d = 0
			else:
				gc0 = od.GeneralizedCost(param, self.lines)
				gc = od.GeneralizedCost(param, corridor.lines)
				if gc0 == float("inf"):
					d = od.demand
				elif gc == float("inf"):
					d = 0
				else:
					d = od.demand * (c + (1 - c) * (gc0/gc)**(param.gamma))
			demand.append(OD(self, od.origin, od.dest, d))
		
		return demand

	def GetConsumerSurplus(self, param, corridor):
		""" Returns the consumer surplus of the given corridor where the reference is self. """
		cs = 0
		for od in corridor.demand:
			gc0 = od.GeneralizedCost(param, self.lines)
			gc = od.GeneralizedCost(param, corridor.lines)
			
			if gc == float("inf"):
				return -float("inf")
			elif gc0 == float("inf"):
				return float("inf")
			else:
				cs += od.demand * 0.5 * (gc0 - gc)
			
		return cs
	
	def TotalSurplus(self, param, corridor):
		""" Returns the total surplus of the given corridor where the reference is self. """
		return self.GetConsumerSurplus(param, corridor) + corridor.TotalRevenues(param) - corridor.OperatorCost(param)
	
	def Duplicate(self, name):
		""" Return a corridor with the same characteristics but no lines.
		"""
		c = Corridor(name, self.length, self.typo)
		for i in range(c.n):
			for j in range(c.n):
				c.GetOD(i, j).demand = self.GetOD(i,j).demand
		return c
	
