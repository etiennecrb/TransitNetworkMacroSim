#!/usr/bin/python
# -*- coding: utf-8 -*-

# Parameters.py

import model

class Parameters():
	""" This class contains all the parameters needed to compute the model. """
	def __init__(self):
		# Modes paramaters
		self.nb_modes = 6
		self.mode_name = ["Voiture", "Bus", "BHNS", "Tramway", "Métro", "Train"]
		
		self.vmax = [90, 40, 50, 60, 80, 120]
		self.s = [0, 0.3, 0.5, 0.5, 1, 3]
		self.f = [1800, 10, 12, 15, 20, 10]
		self.k = [1.10, 70, 90, 150, 600, 700]
		
		self.dt = [0, 34.0/3600,34.0/3600,34.0/3600,45.0/3600,60.0/3600]
		self.alpha = [0, 0, 0, 0, 0, 0]
		self.car_price = 0.34
		self.price = [0, 0, 0, 0, 0, 0]
		
		self.cexp = [	0, 
						78, 
						78, 
						122, 
						446, 
						499]
		self.cinf = [	0, 
						0, 
						32, 
						24, 
						989, 
						646]
		self.csta = [0, 0, 0, 0, 0, 0]
		
		
		# Demand parameters
		self.ctime = 12
		
		self.wa = 1.5
		self.ww = 1.5
		self.wt = 1.0
		self.we = 1.0
		
		self.gamma = 1
		
		self.captive = 0.3
		
	def Duplicate(self):
		p = Parameters()
		for i in range(self.nb_modes):
			p.dt[i] = self.dt[i]
			p.alpha[i] = self.alpha[i]
		
		p.ctime = self.ctime
		
		p.wa = self.wa
		p.ww = self.ww
		p.wt = self.wt
		p.we = self.we
		
		p.gamma = self.gamma
		
		p.captive = self.captive
		
		return p
		
	def DefaultLine(self, corridor, mode):
		""" Returns a line with the default attributes for given mode and corridor. """
		line = model.Line(corridor,
						mode, 
						self.f[mode], 
						[self.s[mode]]*corridor.n, 
						[self.vmax[mode]]*corridor.n, 
						self.k[mode], 
						self.dt[mode],
						self.price[mode])
		return line
		
		
