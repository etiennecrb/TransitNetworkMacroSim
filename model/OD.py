#!/usr/bin/python
# -*- coding: utf-8 -*-

# OD.py

import time
import math

class OD():
	""" Define a particular type of demand on a certain OD trip.
	
	Attributes:
		- corridor -- Corridor
		- origin (int) -- Origin
		- dest (int) -- Destination
		- demand (float) -- Level of demand
		- fd (float) -- Demand distribution factor (1 if uniformly distributed demand, around 0 if station-centered demand)
		- fw (float) -- Waiting time factor (0.5 if passengers arrive at the station randomly)
		- fe (float) -- Egress time factor (1 if uniformly distributed destinations, 0 if stations are destinations)
		- va (float) -- Access speed from origin to departure station (km/h)
		- ve (float) -- Egress speed from arrival station to destination (km/h)
	"""
	
	def __init__(self, corridor, origin, dest, demand, fd=1.0, fw=0.5, fe=1.0, va=5.0, ve=5.0):
		self.corridor = corridor
		self.origin = int(origin)
		self.dest = int(dest)
		self.demand = float(demand)
		
		self.fd = float(fd)
		self.fw = float(fw)
		self.fe = float(fe)
		self.va = float(va)
		self.ve = float(ve)
		
		self.trip_length = self.GetTripLength(self.origin, self.dest)
	
	
	def Update(self):
		""" Updates attributes that depend on corridor's attributes
		(called each time the corridor is modified).
		"""
		self.trip_length = self.GetTripLength(self.origin, self.dest)
	
	def GetTripLength(self, o, d):
		""" Returns default trip length (i.e. under the hypothesis of homogenous
		distribution of origins and destinations inside each zone.
		"""
		if o == d:
			return self.corridor.zone_length[o]/4.0
		
		else:
			# Abscisse of the center of the origin zone
			o_abs = self.corridor.landmarks[o] + 0.5*(self.corridor.landmarks[o+1] - self.corridor.landmarks[o])
			# Abscisse of the center of the destination zone
			d_abs = self.corridor.landmarks[d] + 0.5*(self.corridor.landmarks[d+1] - self.corridor.landmarks[d])
			return abs(o_abs - d_abs)
	
	def LoadA(self, corridor, x):
		""" Returns the number of people traveling at the same time 
		at abscisse x on the corridor in one direction (right to left).
		"""
		if self.origin > self.dest:
			if x < corridor.landmarks[self.dest] or x > corridor.landmarks[self.origin+1]:
				return 0
			elif x > corridor.landmarks[self.dest] and x < corridor.landmarks[self.dest+1]:
				return self.demand * (x - corridor.landmarks[self.dest]) / corridor.zone_length[self.dest]
			elif x > corridor.landmarks[self.origin] and x < corridor.landmarks[self.origin+1]:
				return self.demand * (- x + corridor.landmarks[self.origin+1]) / corridor.zone_length[self.origin]
			else:
				return self.demand
		elif self.origin == self.dest:
			return self.demand * x * (1 - x/self.trip_length) / self.trip_length
		else:
			return 0
	
	def LoadB(self, corridor, x):
		""" Returns the number of people traveling at the same time 
		at abscisse x on the corridor in one direction (left to right).
		"""
		if self.origin < self.dest:
			if x > corridor.landmarks[self.dest+1] or x < corridor.landmarks[self.origin]:
				return 0
			elif x > corridor.landmarks[self.dest] and x < corridor.landmarks[self.dest+1]:
				return self.demand * (- x + corridor.landmarks[self.dest+1]) / corridor.zone_length[self.dest]
			elif x > corridor.landmarks[self.origin] and x < corridor.landmarks[self.origin+1]:
				return self.demand * (x - corridor.landmarks[self.origin]) / corridor.zone_length[self.origin]
			else:
				return self.demand
		elif self.origin == self.dest:
			return self.demand * x * (1 - x/self.trip_length) / self.trip_length
		else:
			return 0
			
	def AccessTime(self, line):
		"""  Returns the access time from origin to the given line. """
		if line.m == 0:
			return 0
		else:
			return self.fd*line.s[self.origin]/(2*self.va)
		
	def EgressTime(self, line):
		"""  Returns the egress time from the given line to destination. """
		if line.m == 0:
			return 0
		else:
			return self.fe*line.s[self.dest]/(2*self.ve)
		
	def WaitingTime(self, line):
		""" Returns the waiting time. """
		if line.m == 0:
			return 0
		return self.fw/line.f
		
	def InVehicleTime(self, line):
		""" Returns the in-vehicle time. """
		
		r = 0
		a = min(self.origin, self.dest)
		b = max(self.origin, self.dest)
		
		if a == b:
			r += self.corridor.zone_length[a]/(4*line.GetCommercialSpeed(a))
		else:
			# Origin zone
			r += self.corridor.zone_length[a]/(2*line.GetCommercialSpeed(a))
			# Destination zone
			r += self.corridor.zone_length[b]/(2*line.GetCommercialSpeed(b))
			# Between them
			for i in range(b - a - 1):
				r += self.corridor.zone_length[a+i+1] / line.GetCommercialSpeed(a+i+1)
		return r
		
	def TravelTime(self, line):
		""" Returns the total travel time. """
		return self.AccessTime(line) + self.WaitingTime(line) + self.InVehicleTime(line) + self.EgressTime(line)
	
	def LineWeightedTravelTime(self, param, line):
		""" Computes the weighted travel time for the given line."""
		wtt = 0
		wtt += param.wa * self.AccessTime(line)
		wtt += param.ww * self.WaitingTime(line)
		wtt += param.wt * self.InVehicleTime(line)
		wtt += param.we * self.EgressTime(line)
		return wtt
		
	def WeightedTravelTime(self, param, lines):
		""" Computes the total weighted travel time for the demand on the given network."""
		wtt = 0
		for line in lines:
			p = self.ModalSplit(param, lines, line)
			wtt += p * self.LineWeightedTravelTime(param, line)
		
		if len(lines) == 0:
			return float("inf")
		else:
			return wtt
	
	def LineGeneralizedCost(self, param, line):
		""" Returns the observable utility for given line. """
		gc = param.ctime * self.LineWeightedTravelTime(param, line) + line.price + param.alpha[line.m]
		if line.m == 0:
			gc += param.car_price * self.trip_length
		return gc
	
	def GeneralizedCost(self, param, lines):
		""" Computes the generalized cost for the demand on the given network. """
		if self.demand == 0:
			return 0
		if len(lines) == 0:
			return float("inf")
		logsum = 0
		for line in lines:
			logsum += math.exp(-self.LineGeneralizedCost(param, line))
		if logsum != 0:
			logsum = math.log(logsum)
		else:
			logsum = -float("inf")
		return -logsum
	
	
	def ModalSplit(self, param, lines, line):
		""" Compute the modal split of line given in argument in the set choice "lines". """
		if self.demand != 0 and len(lines) != 0 :
			v = self.LineGeneralizedCost(param, line)
			
			num = math.exp(-v)
			denom = 0
			for l in lines:
				v = self.LineGeneralizedCost(param, l)
				denom += math.exp(-v)
			
			if denom != 0:
				return num / denom
			else:
				return 0
		else:
			return 0
	
	def __str__(self):
		return "("+str(self.origin)+","+str(self.dest)+")"
	
