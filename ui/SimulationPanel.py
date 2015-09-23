#!/usr/bin/python
# -*- coding: utf-8 -*-

# SimulationPanel.py

import wx
from ScenarioDialog import *
from model import Model

class SimulationPanel(wx.Panel):
	""" This class creates the interface (contained in a panel) that enables user 
	to choose the options of simulation and optimization.
	"""
	
	def __init__(self, parent, model):		 
		super(SimulationPanel, self).__init__(parent)
		self.parent = parent
		self.model = model
		self.InitUI()
			
	def InitUI(self):
		""" Creates the interface which is divided in two parts :
				- simulations
				- optimizations
		"""
		sizer = wx.BoxSizer(wx.VERTICAL)
	   
		sizer.Add(self.simulation_sizer(), 0, wx.ALL|wx.EXPAND, 20)
		sizer.Add(self.optimization_sizer(), 0, wx.ALL|wx.EXPAND, 20)			
		calculate_sizer = wx.BoxSizer(wx.HORIZONTAL)
		calculate_button = wx.Button(self, label="Calculer")
		calculate_button.Bind(wx.EVT_BUTTON, self.OnCalculate)
		calculate_sizer.Add(calculate_button)
		sizer.Add(calculate_sizer, 0, wx.ALL, 20)
		
		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		sizer.Fit(self)
   		self.Show(True)
   		
   		self.UpdateUI()
		
	def UpdateUI(self):
		""" Updates the lists of simulations and optimizations. """
		self.sim_listbox.Clear()
		for s in self.model.simulations:
			self.sim_listbox.Append(s[0].name)
		self.opt_listbox.Clear()
		for o in self.model.optimizations:
			self.opt_listbox.Append(o[0].name)
		self.Layout()
		
	def OnCalculate(self, e):
		self.model.Calculate()
	   	
	def CreateSimScenario(self, e):
		""" Create a simulation scenario creation dialog. """
	   	create_scenario_dialog = CreateSimScenarioDialog(self.model, self.model.reference, 0)
	   	create_scenario_dialog.ShowModal()
	   	create_scenario_dialog.Destroy()
	   	self.UpdateUI()
	   	
	def ModifySimScenario(self, e):
		""" Create a simulation scenario modification dialog. """
	   	create_scenario_dialog = CreateSimScenarioDialog(self.model, self.model.simulations[self.sim_listbox.GetSelection()][0], 1)
	   	create_scenario_dialog.ShowModal()
	   	create_scenario_dialog.Destroy()
	   	self.UpdateUI()
	   		
	def DeleteSimScenario(self, e):
	   	s = self.sim_listbox.GetSelection()
	   	self.model.simulations.pop(s)
	   	self.UpdateUI()
	   	
	def CreateOptScenario(self, e):
		""" Create an optimization scenario creation dialog. """
	   	create_scenario_dialog = CreateOptScenarioDialog(self.model, self.model.reference, [], 0)
	   	create_scenario_dialog.ShowModal()
	   	create_scenario_dialog.Destroy()
	   	self.UpdateUI()
	   	
	def ModifyOptScenario(self, e):
		""" Create an optimization scenario modification dialog. """
	   	create_scenario_dialog = CreateOptScenarioDialog(self.model, self.model.optimizations[self.opt_listbox.GetSelection()][0], self.model.optimizations[self.opt_listbox.GetSelection()][1], 1)
	   	create_scenario_dialog.ShowModal()
	   	create_scenario_dialog.Destroy()
	   	self.UpdateUI()
	   		
	def DeleteOptScenario(self, e):
	   	o = self.opt_listbox.GetSelection()
	   	self.model.optimizations.pop(o)
	   	self.UpdateUI()

	def optimization_sizer(self):
		box = wx.StaticBox(self, label="Scénarios d'optimisation")
		sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
		opt_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.opt_listbox = wx.ListBox(self, -1, size=(300,80))
		for sce in self.model.optimizations:
			self.opt_listbox.Append(sce.name)
		
		opt_sizer.Add(self.opt_listbox, wx.ALIGN_CENTER_VERTICAL)
		
		mod_button = wx.Button(self, 1, "Modifier")
		mod_button.Bind(wx.EVT_BUTTON, self.ModifyOptScenario)
		del_button = wx.Button(self, 1, "Supprimer")
		del_button.Bind(wx.EVT_BUTTON, self.DeleteOptScenario)
		buttons_sizer = wx.BoxSizer(wx.VERTICAL)
		buttons_sizer.Add(mod_button)
		buttons_sizer.Add(del_button)
		
		opt_sizer.Add(buttons_sizer, wx.ALIGN_CENTER_VERTICAL)
		
		add_button = wx.Button(self, 1, "Ajouter un scénario")
		add_button.Bind(wx.EVT_BUTTON, self.CreateOptScenario)
		
		sizer.Add(opt_sizer)	
		sizer.Add(add_button)
			
		return sizer
		
	def simulation_sizer(self):
		box = wx.StaticBox(self, label="Scénarios de simulation")
		sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
		sim_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sim_listbox = wx.ListBox(self, -1, size=(300,80))
		for sce in self.model.simulations:
			self.sim_listbox.Append(sce.name)
		
		sim_sizer.Add(self.sim_listbox, wx.ALIGN_CENTER_VERTICAL)
		
		mod_button = wx.Button(self, 1, "Modifier")
		mod_button.Bind(wx.EVT_BUTTON, self.ModifySimScenario)
		del_button = wx.Button(self, 1, "Supprimer")
		del_button.Bind(wx.EVT_BUTTON, self.DeleteSimScenario)
		buttons_sizer = wx.BoxSizer(wx.VERTICAL)
		buttons_sizer.Add(mod_button)
		buttons_sizer.Add(del_button)
		
		sim_sizer.Add(buttons_sizer, wx.ALIGN_CENTER_VERTICAL)
		
		add_button = wx.Button(self, 1, "Ajouter un scénario")
		add_button.Bind(wx.EVT_BUTTON, self.CreateSimScenario)
		
		sizer.Add(sim_sizer)	
		sizer.Add(add_button)
			
		return sizer
