#!/usr/bin/python
# -*- coding: utf-8 -*-

# CreateScenarioDialog.py

import wx
import model
from LineDialog import *
import CorridorPanel

class CreateSimScenarioDialog(wx.Dialog):
	"""
	Create a new dialog that enables user to create a new set of lines for the
	given corridor to define a simulation scenario.
	"""
	def __init__(self, model, corridor, modify):
		super(CreateSimScenarioDialog, self).__init__(None)
		
		self.model = model
		self.param = self.model.param
		self.modify = modify
		
		if self.modify == 0:
			self.SetTitle("Créer un scénario de simulation")
			self.corridor = corridor.Duplicate("Scénario de simulation")
			for line in corridor.lines:
				self.corridor.lines.append(line.Duplicate())
		else:
			self.old_corridor = corridor
			for c in self.model.simulations:
				if c[0] == corridor:
					self.old_elasticity = c[1]
			self.SetTitle("Modifier un scénario de simulation")
			self.corridor = corridor.Duplicate(corridor.name)
			for line in corridor.lines:
				self.corridor.lines.append(line.Duplicate())
		
		self.InitUI()
		self.SetSize((640,480))
		 
	def InitUI(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		name_sizer = wx.BoxSizer(wx.HORIZONTAL)
		name_sizer.Add(wx.StaticText(self, label="Nom du scénario :"), 0, wx.ALIGN_CENTER_VERTICAL)
		self.name = wx.TextCtrl(self, value=self.corridor.name, size=(300,-1))
		self.name.Bind(wx.EVT_TEXT, self.UpdateCorridor)
		name_sizer.Add(self.name, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer.Add(name_sizer, 0, wx.ALL|wx.EXPAND, 20)
		
		self.elasticity = wx.CheckBox(self, label="Élasticité de la demande")
		if self.modify == 0:
			self.elasticity.SetValue(1)
		else:
			self.elasticity.SetValue(self.old_elasticity)
		sizer.Add(self.elasticity, 0, wx.ALL|wx.EXPAND, 20)
		
		sizer.Add(self.lines_sizer(), 0, wx.ALL|wx.EXPAND, 20)
		
		# Buttons
		if self.modify == 0:
			ok_label = "Créer"
		else:
			ok_label = "Modifier"
		
		buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
		ok_button = wx.Button(self, label=ok_label)
		close_button = wx.Button(self, label='Annuler')
		ok_button.Bind(wx.EVT_BUTTON, self.OnOK)
		close_button.Bind(wx.EVT_BUTTON, self.OnClose)
		buttons_sizer.Add(ok_button, wx.ALIGN_RIGHT)
		buttons_sizer.Add(close_button, wx.ALIGN_RIGHT)
		
		sizer.Add(buttons_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		self.SetSizer(sizer)
		
	def UpdateUI(self):
		""" Update some labels (lines and demand) after some attributes are modified.
		"""
		self.lines_listbox.Clear()
		for line in self.corridor.lines:
			self.lines_listbox.Append(line.name)
		self.Layout()
	
	def UpdateCorridor(self, event):
		""" Modify the attributes of the corridor. """
		self.corridor.name = self.name.GetValue().encode("utf-8")
		self.UpdateUI()
	
	def lines_sizer(self):
		lines_box = wx.StaticBox(self, label="Lignes de transport collectif existantes")
		lines_sizer = wx.StaticBoxSizer(lines_box, wx.VERTICAL)
		listbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.lines_listbox = wx.ListBox(self, -1, size=(500,80))
		for line in self.corridor.lines:
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
	
	def OnOK(self, e):
		if self.modify != 0:
			self.model.simulations.remove([self.old_corridor, self.old_elasticity])
		self.model.simulations.append([self.corridor, self.elasticity.GetValue()])
		self.Destroy()	
		
	def OnClose(self, e):
		self.Destroy()

	def CreateLine(self, e):
	   	create_line_dialog = CreateLineDialog(self.param, self.corridor, 0)
	   	create_line_dialog.ShowModal()
	   	create_line_dialog.Destroy()
	   	self.UpdateUI()
	   	
	def ModifyLine(self, e):
	   	create_line_dialog = CreateLineDialog(self.param, self.corridor, self.corridor.lines[self.lines_listbox.GetSelection()])
	   	create_line_dialog.ShowModal()
	   	create_line_dialog.Destroy()
	   	self.UpdateUI()	
	
	def DeleteLine(self, e):
	   	l = self.lines_listbox.GetSelection()
	   	self.corridor.lines.pop(l)
	   	self.UpdateUI()
		
		
class CreateOptScenarioDialog(wx.Dialog):
	"""
	Create a new dialog that enables user to create a new set of lines for the
	given corridor to define an optimization scenario.
	"""
	def __init__(self, model, corridor, lines, modify):
		super(CreateOptScenarioDialog, self).__init__(None)
		
		self.model = model
		self.param = self.model.param
		self.modify = modify
		self.lines = lines
		
		if self.modify == 0:
			self.SetTitle("Créer un scénario d'optimisation")
			self.corridor = corridor.Duplicate("Scénario d'optimisation")
			for line in corridor.lines:
				self.corridor.lines.append(line.Duplicate())
		else:
			self.SetTitle("Modifier un scénario d'optimisation")
			self.old_corridor = corridor
			self.old_lines = lines
			for c in self.model.optimizations:
				if c[0] == corridor:
					self.old_elasticity = c[2]
			self.old_elasticity
			self.corridor = corridor.Duplicate(corridor.name)
			for line in corridor.lines:
				self.corridor.lines.append(line.Duplicate())
		
		self.InitUI()
		self.SetSize((640,540))
		 
	def InitUI(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		name_sizer = wx.BoxSizer(wx.HORIZONTAL)
		name_sizer.Add(wx.StaticText(self, label="Nom du scénario :"), 0, wx.ALIGN_CENTER_VERTICAL)
		self.name = wx.TextCtrl(self, value=self.corridor.name, size=(300,-1))
		self.name.Bind(wx.EVT_TEXT, self.UpdateCorridor)
		name_sizer.Add(self.name, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer.Add(name_sizer, 0, wx.ALL|wx.EXPAND, 20)
		
		self.elasticity = wx.CheckBox(self, label="Élasticité de la demande")
		if self.modify == 0:
			self.elasticity.SetValue(0)
		else:
			self.elasticity.SetValue(self.old_elasticity)
		sizer.Add(self.elasticity, 0, wx.ALL|wx.EXPAND, 20)
		
		sizer.Add(self.lines_sizer(), 0, wx.ALL|wx.EXPAND, 20)
		
		sizer.Add(self.lines_opt_sizer(), 0, wx.ALL|wx.EXPAND, 20)
		
		# Buttons
		if self.modify == 0:
			ok_label = "Créer"
		else:
			ok_label = "Modifier"
		
		buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
		ok_button = wx.Button(self, label=ok_label)
		close_button = wx.Button(self, label='Annuler')
		ok_button.Bind(wx.EVT_BUTTON, self.OnOK)
		close_button.Bind(wx.EVT_BUTTON, self.OnClose)
		buttons_sizer.Add(ok_button, wx.ALIGN_RIGHT)
		buttons_sizer.Add(close_button, wx.ALIGN_RIGHT)
		
		sizer.Add(buttons_sizer, 0, wx.ALL|wx.EXPAND, 10)
		self.SetSizer(sizer)
		
	def UpdateUI(self):
		""" Update some labels (lines and demand) after some attributes are modified.
		"""
		self.lines_listbox.Clear()
		for line in self.corridor.lines:
			self.lines_listbox.Append(line.name)
			
		self.lines_opt_listbox.Clear()
		for line in self.lines:
			self.lines_opt_listbox.Append(line.name)
		
		self.Layout()
	
	
	def UpdateCorridor(self, event):
		""" Modify the attributes of the corridor. """
		self.corridor.name = self.name.GetValue().encode("utf-8")
		self.UpdateUI()
	
	
	def lines_sizer(self):
		lines_box = wx.StaticBox(self, label="Lignes de transport collectif existantes")
		lines_sizer = wx.StaticBoxSizer(lines_box, wx.VERTICAL)
		listbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.lines_listbox = wx.ListBox(self, -1, size=(500,80))
		for line in self.corridor.lines:
			self.lines_listbox.Append(line.name)
		
		listbox_sizer.Add(self.lines_listbox, wx.ALIGN_CENTER_VERTICAL)
		
		opt_button = wx.Button(self, 1, "Optimiser")
		opt_button.Bind(wx.EVT_BUTTON, self.OptimizeLine)
		mod_button = wx.Button(self, 1, "Modifier")
		mod_button.Bind(wx.EVT_BUTTON, self.ModifyLine)
		del_button = wx.Button(self, 1, "Supprimer")
		del_button.Bind(wx.EVT_BUTTON, self.DeleteLine)
		buttons_sizer = wx.BoxSizer(wx.VERTICAL)
		buttons_sizer.Add(opt_button)
		buttons_sizer.Add(mod_button)
		buttons_sizer.Add(del_button)
		
		listbox_sizer.Add(buttons_sizer, wx.ALIGN_CENTER_VERTICAL)
		
		add_button = wx.Button(self, 1, "Ajouter une ligne")
		add_button.Bind(wx.EVT_BUTTON, self.CreateLine)
		
		lines_sizer.Add(listbox_sizer)	
		lines_sizer.Add(add_button)
			
		return lines_sizer
	
	
	def lines_opt_sizer(self):
		""" A line sizer with specificities for optimizations. """
		lines_box = wx.StaticBox(self, label="Lignes de transport collectif à optimiser")
		lines_sizer = wx.StaticBoxSizer(lines_box, wx.VERTICAL)
		listbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.lines_opt_listbox = wx.ListBox(self, -1, size=(500,80))
		for line in self.lines:
			self.lines_opt_listbox.Append(line.name)
		
		listbox_sizer.Add(self.lines_opt_listbox, wx.ALIGN_CENTER_VERTICAL)
		
		mod_button = wx.Button(self, 1, "Options")
		mod_button.Bind(wx.EVT_BUTTON, self.OptOptions)
		del_button = wx.Button(self, 1, "Retirer")
		del_button.Bind(wx.EVT_BUTTON, self.NonOptLine)
		buttons_sizer = wx.BoxSizer(wx.VERTICAL)
		buttons_sizer.Add(mod_button)
		buttons_sizer.Add(del_button)
		
		listbox_sizer.Add(buttons_sizer, wx.ALIGN_CENTER_VERTICAL)
		lines_sizer.Add(listbox_sizer)	
		return lines_sizer
	
	def OnOK(self, e):
		if self.modify != 0:
			self.model.optimizations.remove([self.old_corridor, self.old_lines, self.old_elasticity])
		self.model.optimizations.append([self.corridor, self.lines, self.elasticity.GetValue()])
		self.Destroy()		
		
	def OnClose(self, e):
		self.Destroy()
		
	def CreateLine(self, e):
	   	create_line_dialog = CreateLineDialog( self.param, self.corridor, 0)
	   	create_line_dialog.ShowModal()
	   	create_line_dialog.Destroy()
	   	self.UpdateUI()
	   	
	def ModifyLine(self, e):
	   	create_line_dialog = CreateLineDialog(self.param, self.corridor, self.corridor.lines[self.lines_listbox.GetSelection()])
	   	create_line_dialog.ShowModal()
	   	create_line_dialog.Destroy()
	   	self.UpdateUI()
	   		
	def OptOptions(self, e):
		""" Opens a special line dialog that enables to specify which variables
		have to be optimized.
		"""
		create_line_dialog = OptOptionsDialog(self.param, self.corridor, self.lines[self.lines_opt_listbox.GetSelection()], self.lines)
	   	create_line_dialog.ShowModal()
	   	create_line_dialog.Destroy()
	   	self.UpdateUI()
	
	def DeleteLine(self, e):
	   	l = self.lines_listbox.GetSelection()
	   	self.corridor.lines.pop(l)
	   	self.UpdateUI()
	   	
	def OptimizeLine(self, e):
		""" Set a line in the optimization list. """
	   	l = self.lines_listbox.GetSelection()
	   	line = self.corridor.lines.pop(l)
	   	self.lines.append(line)
	   	self.UpdateUI()
		
	def NonOptLine(self, e):
		""" Remove a line from the optimization list. """
	   	l = self.lines_opt_listbox.GetSelection()
	   	line = self.lines.pop(l)
	   	self.corridor.lines.append(line)
	   	self.UpdateUI()
