#!/usr/bin/python
# -*- coding: utf-8 -*-

# MainWindo.py

import wx
import model
from CorridorPanel import *
from ParametersDialog import *
from ResultsPanel import *
from SimulationPanel import *
from LogitDialog import *
from SuccessDialog import *

class MainWindow(wx.Frame):
	""" This class initializes the initial configuration and creates the main 
	structure of the user interface (menus and pages).
	"""
	
	def __init__(self, model):
		title = "Analyse de la pertinence de différents modes de transport"
		size = (1024,600)
		
		super(MainWindow, self).__init__(None, title=title, size=size)
  		self.model = model
  		self.model.main_window = self
  		
  		# Creating the panel which will contain all the others panels and its sizer
		self.panel = wx.Panel(self)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Creating the notebook and its different pages
		self.notebook = wx.Notebook(self.panel)
		self.corridor_panel = CorridorPanel.CorridorPanel(self.notebook, self.model)
															
		self.simulation_panel = SimulationPanel(self.notebook, self.model)
												
		self.results_panel = ResultsPanel(self.notebook, self.model)
	
		self.notebook.AddPage(self.corridor_panel, "Corridor et demande")
		self.notebook.AddPage(self.simulation_panel, "Options de simulation")
		self.notebook.AddPage(self.results_panel, "Résultats")
		
		# Creating the menu
		menu = wx.MenuBar()
		
		# File Menu
		fileMenu = wx.Menu()
		quit = fileMenu.Append(wx.ID_EXIT, 'Quittter', 'Quitter')
		self.Bind(wx.EVT_MENU, self.OnQuit, quit)
		
		# Parameters Menu
		paramMenu = wx.Menu()
		modify = paramMenu.Append(	wx.ID_ANY, 
									'Modifier les paramètres du modèle...', 
									'Modifier les paramètres du modèle')
		self.Bind(wx.EVT_MENU, self.OnModify, modify)
		
		logit = paramMenu.Append(wx.ID_ANY, 
								'Calibrer le modèle de choix modal...', 
								'Calibrer le modèle de choix modal')
		self.Bind(wx.EVT_MENU, self.OnLogit, logit)
		
		menu.Append(fileMenu, '&Fichier')
		menu.Append(paramMenu, '&Paramètres')
		self.SetMenuBar(menu)
		
		# Adding all the elements to the main panel through the sizer
		self.sizer.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 10)
		self.panel.SetSizer(self.sizer)
	
		self.Centre()
		self.Show()
		
			
	def OnQuit(self, e):
		self.Close()
		
	def OnModify(self, e):
		""" Open a dialog to modify the parameters of the model. """
		p = ParametersDialog(None, self.model.param)
		p.ShowModal()
		p.Destroy()
		
	def OnLogit(self, e):
		""" Open a dialog to modify the parameters of the logit model.
		
		These parameters are used in the function ModalSplit of the OD class.
		"""
		p = LogitDialog(None, self.model.param, self.model.reference)
		p.ShowModal()
		p.Destroy()
	
	def DeleteResults(self):
		self.results_panel.DeleteResults()
		
	def InsertResults(self):
		self.results_panel.InsertResults()
		
	def SuccessDialog(self, results_success):
		p = SuccessDialog(results_success)
		p.ShowModal()
		p.Destroy()
