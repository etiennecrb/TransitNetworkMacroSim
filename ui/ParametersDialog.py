#!/usr/bin/python
# -*- coding: utf-8 -*-

# ParametersPanel.py

import wx

class ParametersDialog(wx.Dialog):
	"""
	Create a new dialog that enables user to modify the parameters of the model.
	"""
	
	def __init__(self, parent, param):
		super(ParametersDialog, self).__init__(parent)
		self.param = param
		self.SetSize((1050,580))
		self.InitUI()
		self.SetTitle("Paramètres du modèle")
			
	def InitUI(self):
		sizerV = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		# Travelers parameters
		travelers_fgs = wx.FlexGridSizer(13, 2)
		
		ctime_label = wx.StaticText(self, label="Valeur du temps (€/h) :")
		wa_label = wx.StaticText(self, label="Pondération temps d'accès :")
		ww_label = wx.StaticText(self, label="Pondération temps d'attente :")
		wt_label = wx.StaticText(self, label="Pondération temps de trajet :")
		we_label = wx.StaticText(self, label="Pondération temps de sortie :")
		gamma_label = wx.StaticText(self, label="Élasticité de la demande :")
		captive_label = wx.StaticText(self, label="Taux de captifs (%) :")
		
		self.ctime = wx.TextCtrl(self, value=str(self.param.ctime))
		self.wa = wx.TextCtrl(self, value=str(self.param.wa))
		self.ww = wx.TextCtrl(self, value=str(self.param.ww))
		self.wt = wx.TextCtrl(self, value=str(self.param.wt))
		self.we = wx.TextCtrl(self, value=str(self.param.we))
		self.gamma = wx.TextCtrl(self, value=str(self.param.gamma))
		self.captive = wx.TextCtrl(self, value=str(self.param.captive))
		
		travelers_fgs.AddMany([(ctime_label), 
			(self.ctime, 1, wx.EXPAND), 
			(wa_label), 
			(self.wa, 1, wx.EXPAND), 
			(ww_label), 
			(self.ww, 1, wx.EXPAND),
			(wt_label),
			(self.wt, 1, wx.EXPAND), 
			(we_label),
			(self.we, 1, wx.EXPAND),
			(gamma_label),
			(self.gamma, 1, wx.EXPAND),
			(captive_label),
			(self.captive, 1, wx.EXPAND)])
			
		dt_labels = []
		self.dt = []
		
		for i in range(self.param.nb_modes):
			dt_labels.append(wx.StaticText(self, label="Temps perdu à chaque station du mode "+self.param.mode_name[i]+" (s) :"))
			self.dt.append(wx.TextCtrl(self, value=str(self.param.dt[i]*3600)))
			travelers_fgs.AddMany([(dt_labels[-1]), (self.dt[-1], 1, wx.EXPAND)])
		
		sizer.Add(travelers_fgs, 0, wx.ALL|wx.EXPAND, 20)
		
		# Operators parameters
		operators_fgs = wx.FlexGridSizer(3*self.param.nb_modes, 2)
		
		cexp_labels = []
		self.cexp = []
		cinf_labels = []
		self.cinf = []
		csta_labels = []
		self.csta = []
		
		for i in range(self.param.nb_modes):
			cexp_labels.append(wx.StaticText(self, label="Coût d'exploitation horaire par véhicule du mode "+self.param.mode_name[i]+" (€/h/véh.) :"))
			self.cexp.append(wx.TextCtrl(self, value=str(self.param.cexp[i])))
			cinf_labels.append(wx.StaticText(self, label="Coût d'infrastructure horaire du mode "+self.param.mode_name[i]+" (€/h) :"))
			self.cinf.append(wx.TextCtrl(self, value=str(self.param.cinf[i])))
			csta_labels.append(wx.StaticText(self, label="Coût d'une station du mode "+self.param.mode_name[i]+" (€/h) :"))
			self.csta.append(wx.TextCtrl(self, value=str(self.param.csta[i])))
		
		
		for j in range(len(self.cexp)):
			operators_fgs.AddMany([(cexp_labels[j]), (self.cexp[j], 1, wx.EXPAND)])
		for j in range(len(self.cexp)):
			operators_fgs.AddMany([(cinf_labels[j]), (self.cinf[j], 1, wx.EXPAND)])
		for j in range(len(self.cexp)):
			operators_fgs.AddMany([(csta_labels[j]), (self.csta[j], 1, wx.EXPAND)])
		

		sizer.Add(operators_fgs, 1, wx.ALL|wx.EXPAND, 20)
		
		# Buttons
		buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
		ok_button = wx.Button(self, label='OK')
		close_button = wx.Button(self, label='Annuler')
		ok_button.Bind(wx.EVT_BUTTON, self.OnOK)
		close_button.Bind(wx.EVT_BUTTON, self.OnClose)
		buttons_sizer.Add(ok_button, wx.ALIGN_RIGHT)
		buttons_sizer.Add(close_button, wx.ALIGN_RIGHT)
		
		sizerV.Add(sizer, 0, wx.EXPAND)
		sizerV.Add(buttons_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		self.SetSizer(sizerV)
	   		
	def OnOK(self, event):
 		self.param.ctime = float(self.ctime.GetValue())
		self.param.wa = float(self.wa.GetValue())
		self.param.ww = float(self.ww.GetValue())
		self.param.wt = float(self.wt.GetValue())
		self.param.we = float(self.we.GetValue())
		self.param.gamma = float(self.gamma.GetValue())
		self.param.captive = float(self.captive.GetValue())
		
		for i in range(self.param.nb_modes):
			self.param.dt[i] = float(self.dt[i].GetValue())/3600
			self.param.csta[i] = float(self.csta[i].GetValue())
			self.param.cexp[i] = float(self.cexp[i].GetValue())
			self.param.cinf[i] = float(self.cinf[i].GetValue())
		
		self.Destroy()
	
	def OnClose(self, event):
		self.Destroy()
