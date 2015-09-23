#!/usr/bin/python
# -*- coding: utf-8 -*-

# Model.py

from scipy.optimize import minimize
import wx
from math import exp

from Corridor import *
from Line import *
from OD import *
from Parameters import *


class Model():
	""" This class contains all the objects and data needed to run the model.
	
	It enables to clearly separate the user interface and the visualization of 
	the results from the model. It also manages the interactions between the different
	components of the model.
	"""
	
	def __init__(self, main_window=None):
		self.main_window = main_window
		self.param = Parameters()
		
		# Defining the initial corridor which is the reference situation
		self.length = 15
		self.typo = 0
		self.reference = Corridor("Référence", self.length, self.typo)
		
		# Defining some lists that will contain the scenarios and their results
		# Structure :
		# 	- optimizations : [[corridor with lines which won't be optimized,
		#						[lines to optimize],
		#						elasticity (boolean)],...]
		#	- simulations : [[corridor to simulate, elasticity (boolean)],...]
		#	- optimizations_results : [corridor, ...]
		#	- simulations_results : [corridor, ...]
		self.optimizations = []
		self.simulations = []
		self.optimizations_results = []
		self.simulations_results = []
	
	def SetLength(self, length):
		""" Modify the length of all corridors. """
		self.reference.SetLength(length)
		for opt in self.optimizations:
			opt[0].SetLength(length)
		for sim in self.simulations:
			sim[0].SetLength(length)
			
	def SetOD(self, i, j, demand):
		""" Modify the demand for the given OD for all corridors. """
		self.reference.GetOD(i,j).demand = demand
		for opt in self.optimizations:
			opt[0].GetOD(i,j).demand = demand
		for sim in self.simulations:
			sim[0].GetOD(i,j).demand = demand
			
	def SetTypology(self, typo):
		""" Modify the typo of the reference corridor.
		
		It will erase all lines of the reference and all scenarios. """
		self.reference.SetTypology(typo)
		self.optimizations = []
		self.simulations = []
		self.optimizations_results = []
		self.simulations_results = []
		if self.main_window != None:
			self.main_window.simulation_panel.UpdateUI()
			self.main_window.DeleteResults()
	
	def Calculate(self):
		""" This class computes the model for the different scenarios and
		give the results to the user interface.
		"""
		
		# Opening a progess dialog and creating variables to estimate the progression
		if self.main_window != None:
			self.progress_dialog = wx.ProgressDialog(	"Simulation et optimisation", 
														"Calculs en cours")
			self.progress_dialog.Update(0)
		self.progress_total = 1 + len(self.simulations) + len(self.optimizations)
		self.progress_count = 0
		
		# Deleting all former results
		self.optimizations_results = []
		self.simulations_results = []
		if self.main_window != None:
			self.main_window.DeleteResults()
		self.results_success = [] # Elements : [name, success, message]
		
		# Computing the model
		self.Simulate()
		self.Optimize()	
					
		if self.main_window != None:
			self.main_window.InsertResults()
			self.progress_dialog.Update(100)
			if self.results_success:
				self.main_window.SuccessDialog(self.results_success)
	
	def Simulate(self):
		""" Computes all the simulation scenarios.
		
		Uses self.simulations as input and self.simulations_results as output.
		"""
		for sim in self.simulations:
			corridor = sim[0]
			elasticity = sim[1]
			# If demand is elastic, we calculate the new demand
			if elasticity:
				corridor.demand = self.reference.GetElasticDemand(self.param, corridor)
			self.simulations_results.append(corridor)
			# Updating progress dialog
			self.progress_count += 1
			if self.main_window != None:
				self.progress_dialog.Update(100*self.progress_count/self.progress_total)
	
	
	def	Optimize(self):
		""" Computes all the optimization scenarios.
		
		Uses self.optimizations as input and self.optimizations_results as output.
		"""
		for opt in self.optimizations:
			corridor = opt[0] # Corridor with lines which won't get optimized
			lines = opt[1] # List of lines which will be optimized
			elasticity = opt[2]
			
			def ObjectiveFunction(x):
				new_corridor = corridor.Duplicate("")
				
				# The argument x is a vector that contains the optimization variables
				# in their order of appearance in the list "lines".
				c = 0 # A counter to identify the elements of x
				
				# Construction of the set of lines for the new corridor
				# with the data contained in list lines and vector x.
				for i in range(len(lines)):
					# Frequency
					if lines[i].opt[0] == 0:
						f = lines[i].f
					else:
						f = x[c]
						c += 1
					
					# Stop spacing
					s = []
					for j in range(corridor.n):
						if lines[i].opt[1][j] == 0:
							s.append(lines[i].s[j])
						else:
							s.append(x[c])
							c += 1
			
					line = Line(new_corridor,
								lines[i].m,
								f,
								s,
								lines[i].v,
								lines[i].k,
								lines[i].dt,
								lines[i].price,
								lines[i].name,
								lines[i].opt)
					new_corridor.lines.append(line)
				
				for l in corridor.lines:
					new_corridor.lines.append(l.Duplicate())
					
				if elasticity:
					new_corridor.demand = self.reference.GetElasticDemand(self.param, new_corridor)
			
				# Capacity constraints are managed by giving a malus 
				# if a line is too crowded.
				malus = 0
				for l in new_corridor.lines:
					max_load = new_corridor.Demand(self.param, l) / new_corridor.TotalDemand() * \
									max(new_corridor.MaxLoadA(), new_corridor.MaxLoadB())
					capacity = l.f * l.k
					if max_load > capacity:
						malus += (max_load - capacity)**2
				
				if elasticity:
					r = -self.reference.TotalSurplus(self.param, new_corridor) + malus
				else:
					r = new_corridor.TotalCost(self.param) + malus
				return r
			
			# Defining the optimization program
			x0 = []
			bounds = []
			for i in range(len(lines)):
				# Frequency
				if lines[i].opt[0] == 1:
					x0.append(lines[i].f)
					bounds.append(lines[i].cons[0])
				# Stop spacing
				for j in range(corridor.n):
					if lines[i].opt[1][j] == 1:
						x0.append(lines[i].s[j])
						bounds.append(lines[i].cons[1][j])
			
			if len(x0) != 0:
				r = minimize(ObjectiveFunction, x0, method="L-BFGS-B", bounds=bounds)
				self.results_success.append([corridor.name, r.success, r.message])
				
				# Construction of the set of lines for the new corridor
				# with the data contained in list lines and optimized vector x.
				c = 0
				new_corridor = corridor.Duplicate(corridor.name)
				
				# Frequency
				for i in range(len(lines)):
					if lines[i].opt[0] == 0:
						f = lines[i].f
					else:
						f = r.x[c]
						c += 1
					# Stop spacing
					s = []
					for j in range(corridor.n):
						if lines[i].opt[1][j] == 0:
							s.append(lines[i].s[j])
						else:
							s.append(r.x[c])
							c += 1
					
					line = Line(corridor,
								lines[i].m,
								f,
								s,
								lines[i].v,
								lines[i].k,
								lines[i].dt,
								lines[i].price,
								lines[i].name,
								lines[i].opt)
					new_corridor.lines.append(line)
					
				for l in corridor.lines:
					new_corridor.lines.append(l.Duplicate())
				if elasticity:
					new_corridor.demand = self.reference.GetElasticDemand(self.param, new_corridor)
				
				# Updating progress dialog
				self.progress_count += 1
				if self.main_window != None:
					self.progress_dialog.Update(100*self.progress_count/self.progress_total)
				
				self.optimizations_results.append(new_corridor)
					
	
