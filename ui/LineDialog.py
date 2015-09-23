#!/usr/bin/python
# -*- coding: utf-8 -*-

# LineDialog.py

import wx
import model

class CreateLineDialog(wx.Dialog):
	""" Create a dialog that enables user to add a new line 
	to the corridor given in argument.
	
	Parameters :
		- param : instance of model.Parameters
		- corridor : the corridor of the line
		- modify : 0 if it is a new line or the object line if it is a modification
	"""
	def __init__(self, param, corridor, modify):
		super(CreateLineDialog, self).__init__(None) 
		
		self.param = param
		self.modify = modify
		self.corridor = corridor
		if self.modify == 0:
			self.SetTitle("Créer une ligne de transport collectif")
			self.default_line = self.param.DefaultLine(self.corridor, 1)
		else:
			self.SetTitle("Modifier une ligne de transport collectif")
			self.default_line = self.modify
		
		self.SetSize((640,640))
		self.InitUI()
		 
	def InitUI(self):
		"""
		The dialog is composed by a global vertical sizer which contains :
			- the mode static box (bus, bhns, tram...) : radio buttons
			- the vehicle static box : max speed (spinctrl) and capacity (spinctrl)
			- the LOS static box : frequency (spinctrl) and interstation (textctrl)
		"""
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Name
		name_sizer = wx.BoxSizer(wx.HORIZONTAL)
		name_sizer.Add(wx.StaticText(self, label="Nom de la ligne :"), 0, wx.ALIGN_CENTER_VERTICAL)
		self.name = wx.TextCtrl(self, value=self.default_line.name, size=(300,-1))
		name_sizer.Add(self.name, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer.Add(name_sizer, 0, wx.ALL|wx.EXPAND, 20)
		
		# Mode
		mode_box = wx.StaticBox(self, label='Mode')
		mode_sizer = wx.StaticBoxSizer(mode_box, orient=wx.VERTICAL)
		self.mode = []
		self.mode.append(wx.RadioButton(self, label='Routier', style=wx.RB_GROUP))
		self.mode[-1].Bind(wx.EVT_RADIOBUTTON, self.OnModeChange)
		mode_sizer.Add(self.mode[-1])
		for m in range(self.param.nb_modes-1):
			self.mode.append(wx.RadioButton(self, label=self.param.mode_name[m+1]))
			self.mode[-1].Bind(wx.EVT_RADIOBUTTON, self.OnModeChange)
			if self.default_line.m == m+1:
				self.mode[-1].SetValue(1)
			mode_sizer.Add(self.mode[-1])
		
		self.price = wx.TextCtrl(self, value=str(self.default_line.price), size=(50,-1))
		price_sizer = wx.BoxSizer(wx.HORIZONTAL)
		price_sizer.AddMany([(wx.StaticText(self, label="Prix du ticket (€) :"), 0, wx.ALIGN_CENTER_VERTICAL), (self.price, 0, wx.ALIGN_CENTER_VERTICAL)])
		mode_sizer.Add(price_sizer, 0)
		
		sizer.Add(mode_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		# Vehicles
		vehicle_box = wx.StaticBox(self, label='Véhicules')
		vehicle_sizer = wx.StaticBoxSizer(vehicle_box, orient=wx.VERTICAL)
		
		# Vehicle speed
		self.max_speed = []
		abc = ["A", "B", "C", "D", "E", "F", "G"]
		for i in range(self.corridor.n):
			max_speed_sizer = wx.BoxSizer(wx.HORIZONTAL)
			max_speed_label = wx.StaticText(self, label="Vitesse inter-station (km/h) zone "+abc[i]+" :")
			self.max_speed.append(wx.SpinCtrl(self, value=str(self.default_line.v[i]), size=(60,-1), max=220))
			max_speed_sizer.Add(max_speed_label, 1, wx.ALIGN_CENTER_VERTICAL)
			max_speed_sizer.Add(self.max_speed[-1], 1, wx.ALIGN_CENTER_VERTICAL)
			vehicle_sizer.Add(max_speed_sizer)
			
		# Vehicle capacity
		capacity_sizer = wx.BoxSizer(wx.HORIZONTAL)
		capacity_label = wx.StaticText(self, label="Capacité (personnes) :")
		self.capacity = wx.TextCtrl(self, value=str(self.default_line.k), size=(60,-1))
		capacity_sizer.Add(capacity_label, 1, wx.ALIGN_CENTER_VERTICAL)
		capacity_sizer.Add(self.capacity, 1, wx.ALIGN_CENTER_VERTICAL)
			
		
		vehicle_sizer.Add(capacity_sizer)
			
		sizer.Add(vehicle_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		# LOS
		los_box = wx.StaticBox(self, label='Niveau de service')
		los_sizer = wx.StaticBoxSizer(los_box, orient=wx.VERTICAL)
		
		# LOS interstation
		self.interstation = []
		for i in range(self.corridor.n):
			interstation_sizer = wx.BoxSizer(wx.HORIZONTAL)
			interstation_label = wx.StaticText(self, label="Distance inter-station (km) zone "+abc[i]+" :")
			self.interstation.append(wx.TextCtrl(self, value=str(self.default_line.s[i]), size=(60,-1)))
	   		interstation_sizer.Add(interstation_label, 1, wx.ALIGN_CENTER_VERTICAL)
			interstation_sizer.Add(self.interstation[-1], 1, wx.ALIGN_CENTER_VERTICAL)
			los_sizer.Add(interstation_sizer)
			
		# LOS frequency
		frequency_sizer = wx.BoxSizer(wx.HORIZONTAL)
		frequency_label = wx.StaticText(self, label="Fréquence (véh./h) :")
		self.frequency = wx.TextCtrl(self, value=str(self.default_line.f), size=(60,-1))
		frequency_sizer.Add(frequency_label, 1, wx.ALIGN_CENTER_VERTICAL)
		frequency_sizer.Add(self.frequency, 1, wx.ALIGN_CENTER_VERTICAL)
			
		
		los_sizer.Add(frequency_sizer)
		
		sizer.Add(los_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
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
		self.Layout()
	
	def OnOK(self, e):
		"""
		Add a new line into the corridor and destroy the CreateLineDialog.
		"""
		# Convert the radio buttons of the mode into an integer used by the Line class
		for i in range(self.param.nb_modes):
			if self.mode[i].GetValue():
				m = i
		
		# Modification of the corridor given in argument of CreateLineDialog
		s = []
		v = []
		for i in range(self.corridor.n):
			s.append(float(self.interstation[i].GetValue()))
			v.append(float(self.max_speed[i].GetValue()))
			
		line = model.Line(	self.corridor,
							m,
							float(self.frequency.GetValue()),
							s,
							v,
							float(self.capacity.GetValue()),
							self.param.dt[m],
							float(self.price.GetValue()),
							self.name.GetValue().encode("utf-8"))
		if self.modify != 0:
			self.corridor.lines.remove(self.modify)
		self.corridor.lines.append(line)
		
		self.Destroy()	
	
	def OnModeChange(self, e):
		""" Auto-fill parameters with default values.
		"""
		for i in range(self.param.nb_modes):
			if self.mode[i].GetValue():
				self.default_line = self.param.DefaultLine(self.corridor, i)
		self.DestroyChildren()
		self.InitUI()
	
	def OnClose(self, e):
		""" Destroy the CreateLineDialog."""
		self.Destroy()


class OptOptionsDialog(wx.Dialog):
	""" Create a new dialog that enables user to choose optimization options for a line. """
	def __init__(self, param, corridor, modify, lines):
		super(OptOptionsDialog, self).__init__(None) 
		
		self.param = param
		self.lines = lines
		self.modify = modify
		self.corridor = corridor
		if self.modify == 0:
			self.default_line = self.param.DefaultLine(self.corridor, 1)
		else:

			self.default_line = self.modify
		
		self.SetTitle("Options d'optimisation")
		
		self.SetSize((640,680))
		self.InitUI()
		 
	def InitUI(self):
		"""
		The dialog is composed by a global vertical sizer which contains :
			- the mode static box (bus, bhns, tram...) : radio buttons
			- the vehicle static box : max speed (spinctrl) and capacity (spinctrl)
			- the LOS static box : frequency (spinctrl) and interstation (textctrl)
		"""
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Name
		name_sizer = wx.BoxSizer(wx.HORIZONTAL)
		name_sizer.Add(wx.StaticText(self, label="Nom de la ligne :"), 0, wx.ALIGN_CENTER_VERTICAL)
		self.name = wx.TextCtrl(self, value=self.default_line.name, size=(300,-1))
		name_sizer.Add(self.name, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer.Add(name_sizer, 0, wx.ALL|wx.EXPAND, 20)
		
		# Mode
		mode_box = wx.StaticBox(self, label='Mode')
		mode_sizer = wx.StaticBoxSizer(mode_box, orient=wx.VERTICAL)
		self.mode = []
		self.mode.append(wx.RadioButton(self, label='Routier', style=wx.RB_GROUP))
		self.mode[-1].Bind(wx.EVT_RADIOBUTTON, self.OnModeChange)
		mode_sizer.Add(self.mode[-1])
		for m in range(self.param.nb_modes-1):
			self.mode.append(wx.RadioButton(self, label=self.param.mode_name[m+1]))
			self.mode[-1].Bind(wx.EVT_RADIOBUTTON, self.OnModeChange)
			if self.default_line.m == m+1:
				self.mode[-1].SetValue(1)
			mode_sizer.Add(self.mode[-1])
			
		self.price = wx.TextCtrl(self, value=str(self.default_line.price), size=(50,-1))
		price_sizer = wx.BoxSizer(wx.HORIZONTAL)
		price_sizer.AddMany([(wx.StaticText(self, label="Prix du ticket (€) :"), 0, wx.ALIGN_CENTER_VERTICAL), (self.price, 0, wx.ALIGN_CENTER_VERTICAL)])
		mode_sizer.Add(price_sizer, 0)
		
		sizer.Add(mode_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		# Vehicles
		vehicle_box = wx.StaticBox(self, label='Véhicules')
		vehicle_sizer = wx.StaticBoxSizer(vehicle_box, orient=wx.VERTICAL)
		
		# Vehicle speed
		self.max_speed = []
		abc = ["A", "B", "C", "D", "E", "F", "G"]
		for i in range(self.corridor.n):
			max_speed_sizer = wx.BoxSizer(wx.HORIZONTAL)
			self.max_speed.append(wx.SpinCtrl(self, value=str(self.default_line.v[i]), size=(60,-1), max=220, min=10))
			max_speed_sizer.Add(wx.StaticText(self, label="Vitesse inter-station (km/h) en zone "+abc[i]+" :"), 1, wx.ALIGN_CENTER_VERTICAL)
			max_speed_sizer.Add(self.max_speed[-1], 0, wx.ALIGN_CENTER_VERTICAL)
			vehicle_sizer.Add(max_speed_sizer)
			
		# Vehicle capacity
		capacity_sizer = wx.BoxSizer(wx.HORIZONTAL)
		capacity_label = wx.StaticText(self, label="Capacité (personnes) :")
		self.capacity = wx.TextCtrl(self, value=str(self.default_line.k), size=(60,-1))
		capacity_sizer.Add(capacity_label, 1, wx.ALIGN_CENTER_VERTICAL)
		capacity_sizer.Add(self.capacity, 1, wx.ALIGN_CENTER_VERTICAL)
			
		
		vehicle_sizer.Add(capacity_sizer)
			
		sizer.Add(vehicle_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		# LOS
		los_box = wx.StaticBox(self, label='Niveau de service')
		los_sizer = wx.StaticBoxSizer(los_box, orient=wx.VERTICAL)
		los_fgs = wx.FlexGridSizer(5, 4, 10, 10)
		
		los_fgs.AddMany([(wx.StaticText(self, label=" ")), (wx.StaticText(self, label="Valeur"), 1, wx.ALIGN_CENTER_HORIZONTAL), (wx.StaticText(self, label="Min."), 1, wx.ALIGN_CENTER_HORIZONTAL), (wx.StaticText(self, label="Max."), 1, wx.ALIGN_CENTER_HORIZONTAL)])
		
		# LOS interstation
		self.interstation = []
		self.interstation_min = []
		self.interstation_max = []
		self.interstation_opt = []
		for i in range(self.corridor.n):
			self.interstation_opt.append(wx.CheckBox(self, label="Distance inter-station (km) zone "+abc[i]+" :"))
			self.interstation_opt[-1].SetValue(self.default_line.opt[1][i])
			self.interstation.append(wx.TextCtrl(self, value=str(self.default_line.s[i]), size=(60,-1)))
			self.interstation_min.append(wx.TextCtrl(self, value=str(self.default_line.cons[1][i][0]), size=(60,-1)))
			self.interstation_max.append(wx.TextCtrl(self, value=str(self.default_line.cons[1][i][1]), size=(60,-1)))
			los_fgs.Add(self.interstation_opt[-1], 0, wx.ALIGN_CENTER_VERTICAL)
			los_fgs.Add(self.interstation[-1], 1, wx.ALIGN_CENTER_VERTICAL)
			los_fgs.Add(self.interstation_min[-1], 1, wx.ALIGN_CENTER_VERTICAL)
			los_fgs.Add(self.interstation_max[-1], 1, wx.ALIGN_CENTER_VERTICAL)
			
		# LOS frequency
		frequency_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.frequency_opt = wx.CheckBox(self, label="Fréquence (véh./h) :")
		self.frequency_opt.SetValue(self.default_line.opt[0])
		self.frequency = wx.TextCtrl(self, value=str(self.default_line.f), size=(60,-1))
		self.frequency_min = wx.TextCtrl(self, value=str(self.default_line.cons[0][0]), size=(60,-1))
		self.frequency_max = wx.TextCtrl(self, value=str(self.default_line.cons[0][1]), size=(60,-1))
		
		los_fgs.AddMany([(self.frequency_opt), (self.frequency), (self.frequency_min), (self.frequency_max)])
			
		
		los_sizer.Add(los_fgs)
		
		sizer.Add(los_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		# Buttons
		buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
		ok_button = wx.Button(self, label="Ok")
		close_button = wx.Button(self, label='Annuler')
		ok_button.Bind(wx.EVT_BUTTON, self.OnOK)
		close_button.Bind(wx.EVT_BUTTON, self.OnClose)
		buttons_sizer.Add(ok_button, wx.ALIGN_RIGHT)
		buttons_sizer.Add(close_button, wx.ALIGN_RIGHT)
		
		sizer.Add(buttons_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		self.SetSizer(sizer)
		self.Layout()
	
	def OnOK(self, e):
		"""
		Add a new line into the corridor and destroy the CreateLineDialog.
		"""
		
		# Convert the radio buttons of the mode into an integer used by the Line class
		for i in range(self.param.nb_modes):
			if self.mode[i].GetValue():
				m = i
		
		
		# Modification of the corridor given in argument of CreateLineDialog
		s = []
		v = []
		s_opt = []
		s_cons = []
		for i in range(self.corridor.n):
			s.append(float(self.interstation[i].GetValue()))
			v.append(float(self.max_speed[i].GetValue()))
			
			if self.interstation_opt[i].GetValue():
				s_opt.append(1)
			else:
				s_opt.append(0)
			s_cons.append((float(self.interstation_min[i].GetValue()), float(self.interstation_max[i].GetValue())))
		
		
		opt = []
		cons = []
		if self.frequency_opt.GetValue():
			opt.append(1)
		else:
			opt.append(0)
		cons.append((float(self.frequency_min.GetValue()), float(self.frequency_max.GetValue())))
		opt.append(s_opt)
		cons.append(s_cons)
		
		line = model.Line(self.corridor, m, float(self.frequency.GetValue()), s, v, float(self.capacity.GetValue()), self.param.dt[m], float(self.price.GetValue()), self.name.GetValue().encode("utf-8"), opt, cons)
		
		if self.modify != 0:
			self.lines.remove(self.modify)
			
		self.lines.append(line)
		
		self.Destroy()	
	
	
	def OnModeChange(self, e):
		"""
		If in creation mode (not modification), auto-fill parameters with default values.
		"""
		if self.modify == 0:
			for i in range(self.param.nb_modes):
				if self.mode[i].GetValue():
					self.default_line = self.param.DefaultLine(self.corridor, i)
			self.DestroyChildren()
			self.InitUI()
	
	
	def OnClose(self, e):
		"""
		Destroy the CreateLineDialog.
		"""
		self.Destroy()
