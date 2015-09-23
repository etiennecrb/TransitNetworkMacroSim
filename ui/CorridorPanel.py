#!/usr/bin/python
# -*- coding: utf-8 -*-

# CorridorPanel.py

import wx
import wx.grid
from LineDialog import *

class CorridorPanel(wx.Panel):
	""" This class creates the interface (contained in a panel) that enables user 
	to define the main characteristics of the corridor (typology, demand...).
	"""
	
	def __init__(self, parent, model):		 
		super(CorridorPanel, self).__init__(parent)
		self.model = model
		
		self.InitUI()
			
	def InitUI(self):
		""" Initializes the interface.
		
		The panel is divided in two parts :
			- characteristics : length, typology and demand
			- lines : list of the existing lines
		"""
		sizer = wx.BoxSizer(wx.VERTICAL)
	  		
		sizer.Add(self.characteristics_sizer(), 0, wx.ALL|wx.EXPAND, 20)
		sizer.Add(self.lines_sizer(), 0, wx.ALL|wx.EXPAND, 20)
		
		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		sizer.Fit(self)
  		self.Show(True)
  		
  		self.UpdateUI()
	
	def UpdateUI(self):
		""" Update the interface if some attributes are modified.
		"""
		# List of lines
		self.lines_listbox.Clear()
		for line in self.model.reference.lines:
			self.lines_listbox.Append(line.name)
		
		# Total demand label
		total_demand = 0
		for OD in self.model.reference.demand:
			total_demand += OD.demand
				
		self.total_demand.SetLabel("Demande totale : "+str(int(round(total_demand))))
		self.Layout()
	
	def UpdateCorridor(self, event):
		""" Modify the attributes of the reference corridor.
		
		Called when length slider or OD matrix are modified.
		"""
		if self.model.length != self.length_slider.GetValue():
			self.model.SetLength(self.length_slider.GetValue())
			
		for i in range(self.model.reference.n):
			for j in range(self.model.reference.n):
				self.model.SetOD(i, j, float(self.demand.GetCellValue(i, j)))
		
		self.UpdateUI()
	   	
	def CreateLine(self, e):
		""" Opens a create line dialog and update the interface when closed. """
	   	create_line_dialog = CreateLineDialog(self.model.param, self.model.reference, 0)
	   	create_line_dialog.ShowModal()
	   	create_line_dialog.Destroy()
	   	self.UpdateUI()
	   	
	def ModifyLine(self, e):
		""" Opens a modify line dialog and update the interface when closed. """
	   	create_line_dialog = CreateLineDialog(self.model.param, self.model.reference, self.model.reference.lines[self.lines_listbox.GetSelection()])
	   	create_line_dialog.ShowModal()
	   	create_line_dialog.Destroy()
	   	self.UpdateUI()
	   		
	def DeleteLine(self, e):
		""" Deletes a line from the reference corridor. """
	   	l = self.lines_listbox.GetSelection()
	   	self.model.reference.lines.pop(l)
	   	self.UpdateUI()
	   	
	def OnNext(self, e):
		""" Changes the typology of the corridor. """
		if self.model.reference.typo < 2:
			self.DestroyChildren()
			self.model.SetTypology(self.model.reference.typo+1)
			self.InitUI()

	def OnPrev(self, e):
		""" Changes the typology of the corridor. """
		if self.model.reference.typo > 0:
			self.DestroyChildren()
			self.model.SetTypology(self.model.reference.typo-1)
			self.InitUI()
	
	def characteristics_sizer(self):
		""" Display text and buttons to define the characteristics of the reference. """
		characteristics_box = wx.StaticBox(self, label="Caractéristiques et typologie")
		characteristics_sizer = wx.StaticBoxSizer(characteristics_box, wx.VERTICAL)
			
		fgs = wx.FlexGridSizer(6,2)
			
		self.length_slider = wx.Slider(	self, 
										value=self.model.reference.length,
										minValue=0.1,
										maxValue=100,
										size=(300,-1),
										style=wx.SL_HORIZONTAL | wx.SL_LABELS)
		self.length_slider.Bind(wx.EVT_SCROLL, self.UpdateCorridor)

		self.demand = wx.grid.Grid(self, -1)
		self.demand.CreateGrid(self.model.reference.n, self.model.reference.n)
		
		# OD matrix
		alphabet = ["A", "B", "C", "D", "E"]
		total_demand = 0
		for i in range(self.model.reference.n):
			self.demand.SetRowLabelValue(i, alphabet[i])
			for j in range(self.model.reference.n):
				d = self.model.reference.GetOD(i, j).demand
				total_demand += d
				self.demand.SetCellValue(j, i, str(int(d)))
				
		self.demand.DisableDragRowSize()
		self.demand.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.UpdateCorridor)
		self.total_demand = wx.StaticText(self, label="Demande totale : "+str(total_demand))
		
		fgs.AddMany([(wx.StaticText(self, label="Typologie du corridor :"), 0, wx.ALIGN_CENTER_VERTICAL), 
				(self.typology_sizer()),
				(wx.StaticText(self, label="Longueur (km) :"), 0, wx.ALIGN_CENTER_VERTICAL),
				(self.length_slider),
				(wx.StaticText(self, label="Matrice origine - destination :"), 0, wx.ALIGN_CENTER_VERTICAL),
				(self.demand),
				(self.total_demand)])
			
		characteristics_sizer.Add(fgs, 1, wx.ALL, 10)
			
		return characteristics_sizer
	
	
	def typology_sizer(self):
		""" Creates the interface to choose the typology of the corridor.
		The returned sizer is contained in characteristics_sizer.
		"""
		typology_sizer = wx.BoxSizer(wx.HORIZONTAL)
			
		self.typology_image = wx.StaticBitmap(self, 1, wx.Bitmap("ui/images/"+str(self.model.reference.typo)+".png"))
		next_button = wx.Button(self, 1, ">", size=(20,30))
		next_button.Bind(wx.EVT_BUTTON, self.OnNext)
		prev_button = wx.Button(self, 1, "<", size=(20,30))
		prev_button.Bind(wx.EVT_BUTTON, self.OnPrev)
		typology_sizer.Add(prev_button, 0, wx.ALIGN_CENTER)
		typology_sizer.Add(self.typology_image, 1, wx.ALIGN_CENTER)
		typology_sizer.Add(next_button, 0, wx.ALIGN_CENTER)
			
		return typology_sizer
	
	
	def lines_sizer(self):
		""" Creates the interface to add, modify and remove lines of the corridor. """
		lines_box = wx.StaticBox(self, label="Lignes de transport collectif existantes")
		lines_sizer = wx.StaticBoxSizer(lines_box, wx.VERTICAL)
		listbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.lines_listbox = wx.ListBox(self, -1, size=(300,80))
		for line in self.model.reference.lines:
			self.lines_listbox.Append(line.name)
		
		listbox_sizer.Add(self.lines_listbox, wx.ALIGN_CENTER_VERTICAL)
		
		mod_button = wx.Button(self, 1, "Modifier")
		mod_button.Bind(wx.EVT_BUTTON, self.ModifyLine)
		del_button = wx.Button(self, 1, "Supprimer")
		del_button.Bind(wx.EVT_BUTTON, self.DeleteLine)
		buttons_sizer = wx.BoxSizer(wx.VERTICAL)
		buttons_sizer.Add(mod_button)
		buttons_sizer.Add(del_button)
		
		listbox_sizer.Add(buttons_sizer, wx.ALIGN_CENTER_VERTICAL)
		
		add_button = wx.Button(self, 1, "Ajouter une ligne")
		add_button.Bind(wx.EVT_BUTTON, self.CreateLine)
		
		lines_sizer.Add(listbox_sizer)	
		lines_sizer.Add(add_button)
			
		return lines_sizer
	
