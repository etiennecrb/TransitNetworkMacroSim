#!/usr/bin/python
# -*- coding: utf-8 -*-

# LogitDialog.py

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin

class AutoWidthSortListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
		ListCtrlAutoWidthMixin.__init__(self)
		ColumnSorterMixin.__init__(self, 3)
		
	def GetListCtrl(self):
		return self

class LogitDialog(wx.Dialog):
	"""
	Create a new dialog that enables user to modify the parameters of the logit model.
	"""
	
	def __init__(self, parent, param, corridor):
		super(LogitDialog, self).__init__(parent)
		self.param = param
		self.corridor = corridor
		self.SetSize((480,480))
		self.InitUI()
		self.SetTitle("Paramètres du modèle de choix modal")
			
	def InitUI(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		fgs = wx.FlexGridSizer(self.param.nb_modes, 2)
		
		labels = []
		self.alpha = []
		for i in range(self.param.nb_modes):
			labels.append(wx.StaticText(self, label="Constante spécifique au mode "+self.param.mode_name[i]+" (€) :"))
			self.alpha.append(wx.TextCtrl(self, value=str(self.param.alpha[i])))
			self.alpha[-1].Bind(wx.EVT_TEXT, self.OnChange)
			fgs.AddMany([(labels[-1], 0, wx.ALIGN_CENTER_VERTICAL), (self.alpha[-1], 1, wx.EXPAND)])
		
		sizer.Add(fgs, 0, wx.ALL|wx.EXPAND, 20)
		
		
		# Buttons
		buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
		ok_button = wx.Button(self, label='OK')
		close_button = wx.Button(self, label='Annuler')
		ok_button.Bind(wx.EVT_BUTTON, self.OnOK)
		close_button.Bind(wx.EVT_BUTTON, self.OnClose)
		buttons_sizer.Add(ok_button, wx.ALIGN_RIGHT)
		buttons_sizer.Add(close_button, wx.ALIGN_RIGHT)
		
		sizer.Add(buttons_sizer, 0, wx.ALL|wx.EXPAND, 10)
		
		self.test = AutoWidthSortListCtrl(self)
		self.test.InsertColumn(0, "Ligne", width=60)
		self.test.InsertColumn(1, "Demande", width=wx.LIST_AUTOSIZE_USEHEADER)
		self.test.InsertColumn(2, "Part modale", width=wx.LIST_AUTOSIZE_USEHEADER)
		self.test.InsertColumn(3, "Charge max.", width=wx.LIST_AUTOSIZE_USEHEADER)
		
		sizer.Add(self.test, 1, wx.EXPAND)
		
		self.OnChange(None)
		
		self.SetSizer(sizer)
		self.Layout()
		
	def OnChange(self, e):
		p = self.param.Duplicate()
		
		for i in range(p.nb_modes):
			p.alpha[i] = float(self.alpha[i].GetValue())
		
		self.test.DeleteAllItems()
		for line in self.corridor.lines:
			index = self.test.InsertStringItem(1000, line.name)
			self.test.SetStringItem(index, 1, str(int(round(self.corridor.Demand(p, line)))))
			self.test.SetStringItem(index, 2, str(int(round(100.0*self.corridor.Demand(p, line)/self.corridor.TotalDemand())))+" %")
			self.test.SetStringItem(index, 3, str(int(round(self.corridor.Demand(p, line)/self.corridor.TotalDemand()*100.0*max(self.corridor.MaxLoadA(), self.corridor.MaxLoadB())/(line.f*line.k))))+" %")
			
	   		
	def OnOK(self, event):
		for i in range(self.param.nb_modes):
			self.param.alpha[i] = float(self.alpha[i].GetValue())
		
		self.Destroy()
	
	def OnClose(self, event):
		self.Destroy()
