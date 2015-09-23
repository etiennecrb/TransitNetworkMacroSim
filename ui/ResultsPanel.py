#!/usr/bin/python
# -*- coding: utf-8 -*-

# ResultsPanel.py

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin
import math

class AutoWidthSortListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
		ListCtrlAutoWidthMixin.__init__(self)
		ColumnSorterMixin.__init__(self, 3)
		
	def GetListCtrl(self):
		return self


class ResultsPanel(wx.Panel):
	"""
	This class creates the interface (contained in a panel) that presents the results of the model.
	"""
	
	def __init__(self, parent, model):		 
			super(ResultsPanel, self).__init__(parent)
			self.model = model
			self.param = model.param
			self.corridor = model.reference
			self.InitUI()
			
	def InitUI(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		costs_box = wx.StaticBox(self, label="Coûts par scénario")
		costs_sizer = wx.StaticBoxSizer(costs_box, wx.VERTICAL)
		
		self.list = AutoWidthSortListCtrl(self)
		self.list.InsertColumn(0, "Scénario", width=150)
		self.list.InsertColumn(1, "Demande totale", width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list.InsertColumn(2, "Temps de trajet moyen", width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list.InsertColumn(3, "Coût généralisé moyen", width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list.InsertColumn(4, "Coûts d'infrastructure", width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list.InsertColumn(5, "Coût d'exploitation", width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list.InsertColumn(6, "Coût total", width=wx.LIST_AUTOSIZE_USEHEADER)
		self.list.InsertColumn(7, "Surplus total", width=wx.LIST_AUTOSIZE_USEHEADER)
		

		costs_sizer.Add(self.list, 1, wx.TOP|wx.EXPAND, 10)
		sizer.Add(costs_sizer, 1, wx.ALL|wx.EXPAND, 20)
		
		supply_box = wx.StaticBox(self, label="Offre de transport par scénario")
		supply_sizer = wx.StaticBoxSizer(supply_box, wx.VERTICAL)
		
		self.cb1 = wx.ComboBox(self, pos=(50, 30), choices=[self.corridor.name], style=wx.CB_READONLY)
		self.cb1.Bind(wx.EVT_COMBOBOX, self.OnSelect)
		
		self.cb2 = wx.ComboBox(self, pos=(50, 30), choices=[self.corridor.name], style=wx.CB_READONLY)
		self.cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect)
		
		self.supply = []
		self.supply.append(AutoWidthSortListCtrl(self))
		self.supply.append(AutoWidthSortListCtrl(self))
		
		for l in self.supply:
			l.InsertColumn(0, "Ligne", width=60)
			l.InsertColumn(1, "Demande", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(2, "Part modale", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(3, "Charge max/Capacité", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(4, "Fréquence", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(5, "Vitesse commerciale", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(6, "Interstation", width=150)
			l.InsertColumn(7, "Nombre véhicules", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(8, "Coûts d'infra.", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(9, "Coût d'exploitation", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(10, "Coût opérateur", width=wx.LIST_AUTOSIZE_USEHEADER)
			l.InsertColumn(11, "Recettes", width=wx.LIST_AUTOSIZE_USEHEADER)
		
		supply_sizer.Add(self.cb1)
		supply_sizer.Add(self.supply[0], 1, wx.EXPAND)
		supply_sizer.Add(self.cb2)
		supply_sizer.Add(self.supply[1], 1, wx.EXPAND)
		
		sizer.Add(supply_sizer, 1, wx.ALL|wx.EXPAND, 20)
		
		self.SetSizer(sizer)
		self.Layout()
		
	def OnSelect(self, e):
		all_sce = [self.corridor]
		for r in self.model.simulations_results:
			all_sce.append(r)
		for r in self.model.optimizations_results:
			all_sce.append(r)
		
		sce = [all_sce[self.cb1.GetSelection()], all_sce[self.cb2.GetSelection()]]
		
		for i in range(len(self.supply)):
			self.supply[i].DeleteAllItems()
			for line in sce[i].lines:
				demand = str_results(sce[i].Demand(self.param, line), 0)
				if sce[i].TotalDemand() != 0:
					split = str_results(100.0*sce[i].Demand(self.param, line)/sce[i].TotalDemand(), 0)
				else:
					split = "0"
				if sce[i].TotalDemand() != 0 and line.f != 0 and line.k != 0:
					max_load = str_results(sce[i].Demand(self.param, line)/sce[i].TotalDemand()*100.0*max(sce[i].MaxLoadA(), sce[i].MaxLoadB())/(line.f*line.k), 0)
				else:
					max_load = "0"
				f = str_results(line.f,1)
				vc = str_results(line.GetCommercialSpeed(), 0)
				
				s = ""
				abc = ["A", "B", "C", "D", "E"]
				for j in range(self.corridor.n):
					s_str = str_results(line.s[j]*1000, 0)
					s += abc[j] + " : "+s_str+" m "
						
				n_veh = str_results(line.VehiclesNumber(), 0)
				infra_cost = str_results(line.InfraCost(self.param), 0)
				op_cost = str_results(line.OperatingCost(self.param), 0)
				total_cost = str_results(line.InfraCost(self.param)+line.OperatingCost(self.param), 0)
				revenues = str_results(sce[i].Revenues(self.param, line), 0)
				
				index = self.supply[i].InsertStringItem(1000, line.name)
				self.supply[i].SetStringItem(index, 1, demand)
				self.supply[i].SetStringItem(index, 2, split+" %")
				self.supply[i].SetStringItem(index, 3, max_load+" %")
				self.supply[i].SetStringItem(index, 4, f+" véh./h")
				self.supply[i].SetStringItem(index, 5, vc+" km/h")
				self.supply[i].SetStringItem(index, 6, s)
				self.supply[i].SetStringItem(index, 7, n_veh)
				self.supply[i].SetStringItem(index, 8, infra_cost+" €/h")
				self.supply[i].SetStringItem(index, 9, op_cost+" €/h")
				self.supply[i].SetStringItem(index, 10, total_cost+" €/h")
				self.supply[i].SetStringItem(index, 11, revenues+" €/h")
		
	def DeleteResults(self):
		""" Delete the display of results. """
		self.scenarios = [self.corridor.name]
		self.list.DeleteAllItems()
		for i in range(len(self.supply)):
			self.supply[i].DeleteAllItems()
		
	def InsertResults(self):
		""" Display all the results of the model. """
		
		self.cb1.Clear()
		self.cb2.Clear()
		self.cb1.Append(self.corridor.name)
		self.cb2.Append(self.corridor.name)
		for r in self.model.simulations_results:
			self.cb1.Append(r.name)
			self.cb2.Append(r.name)
		for r in self.model.optimizations_results:
			self.cb1.Append(r.name)
			self.cb2.Append(r.name)
		
		self.cb1.SetSelection(0)
		self.OnSelect(None)
		
		# Creating a list of the results to be displayed
		results = [self.model.reference]
		for result in self.model.simulations_results:
			results.append(result)
		for result in self.model.optimizations_results:
			results.append(result)
		
		for r in results:
			index = self.list.InsertStringItem(1000, r.name)
			
			total_demand = str_results(r.TotalDemand(), 0)
			travel_time = str_results(r.AvgTravelTime(self.param)*60, 0)
			if r.TotalDemand() != 0:
				gen_cost_u = str_results(r.GeneralizedCost(self.param)/r.TotalDemand(),2)
			else:
				gen_cost_u = "0"
			infra_cost = str_results(r.InfraCost(self.param), 0)
			op_cost = str_results(r.OperatingCost(self.param), 0)
			total_cost = str_results(r.TotalCost(self.param), 0)
			total_surplus = str_results(self.model.reference.TotalSurplus(self.param, r), 0)
			
			self.list.SetStringItem(index, 1, total_demand)
			self.list.SetStringItem(index, 2, travel_time+" min")
			self.list.SetStringItem(index, 3, gen_cost_u+" €")
			self.list.SetStringItem(index, 4, infra_cost+" €/h")
			self.list.SetStringItem(index, 5, op_cost+" €/h")
			self.list.SetStringItem(index, 6, total_cost+" €/h")
			self.list.SetStringItem(index, 7, total_surplus+" €/h")
	
def str_results(value, decimals):
	if value == float("inf"):
		return "∞"
	elif value == -float("inf"):
		return "-∞"
	elif math.isnan(value):
		return "NaN"
	elif decimals == 0:
		return str(int(round(value)))
	else:
		return str(round(value, decimals))
