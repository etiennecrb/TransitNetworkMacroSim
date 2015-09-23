#!/usr/bin/python
# -*- coding: utf-8 -*-

# Line.py

class Line():
	""" This class enables the definition of a transport line. """
	def __init__(	self, 
					corridor,
					mode,
					frequency,
					interstation,
					max_speed,
					capacity,
					dwell_time,
					price,
					name="",
					opt=0,
					cons=0):
		self.corridor = corridor
		self.m = int(mode)
		
		# Variables to know which variables have to be optimized
		if opt == 0:
			interstation_opt = [0]*self.corridor.n
			self.opt = [0, interstation_opt]
		else:
			self.opt = opt
		
		# Bounds for these variables
		if cons == 0:
			self.cons = []
			self.cons.append((1, 60))
			self.cons.append([(0.250, 20)]*self.corridor.n)
		else:
			self.cons = cons
		
		self.f = float(frequency)
		self.s = interstation
		self.v = max_speed
		self.k = float(capacity)
		self.dt = float(dwell_time)
		self.price = float(price)
		
		if name == "":
			self.name = str(self)
		else:
			self.name = name
	
	def GetCommercialSpeed(self, zone=-1):
		""" Computes the commercial speed (v=d/t + time lost at stations).
		If zone is specified and valid, returns the commercial speed in this zone.
		"""
		if zone >= 0 and zone < self.corridor.n:
			if self.m == 0:
				return self.v[zone]
			else:
				if self.s[zone] <= self.corridor.zone_length[zone]:
					return 1/(1/self.v[zone] + self.dt/self.s[zone])
				else:
					return self.v[zone]
		else:
			denom = 0
			for i in range(self.corridor.n):
				denom += self.corridor.zone_length[i]/self.GetCommercialSpeed(i)
		return self.corridor.length/denom
	
	def VehiclesNumber(self):
		""" Computes the number of vehicles needed to operate. """
		if self.m != 0:
			t = self.corridor.length / self.GetCommercialSpeed()
			return 2.0*self.f*t
		else:
			return 0
	
	def OperatingCost(self, param):
		""" Computes the operating cost (investment + operating). """
		return param.cexp[self.m] * self.VehiclesNumber()
	
	def InfraCost(self, param):
		""" Computes the infrastructure cost (infra + maintenance + operating station). """
		stations = 0
		if self.m != 0:
			for i in range(self.corridor.n):
				if self.s[i] < self.corridor.zone_length[i]:
					stations += param.csta[self.m]*self.corridor.zone_length[i]/self.s[i]
			return param.cinf[self.m] * self.VehiclesNumber() + stations
		else:
			return param.cinf[self.m]
	
	def OperatorCost(self, param):
		""" Computes the total operator cost. """
		return self.OperatingCost(param) + self.InfraCost(param)
	
	def Duplicate(self):
		""" Returns an identical line. """
		s = []
		v = []
		for i in range(len(self.s)):
			s.append(self.s[i])
			v.append(self.v[i])
		return Line(self.corridor, self.m, self.f, s, v, self.k, self.dt, self.price)
	
	def __str__(self):
		if self.m == 0:
			return "Voiture"
		if self.m == 1:
			return "Bus"
		if self.m == 2:
			return "BHNS"
		if self.m == 3:
			return "Tramway"
		if self.m == 4:
			return "Métro"
		if self.m == 5:
			return "Train"
		
