#!/usr/bin/python
# -*- coding: utf-8 -*-

# SuccessDialog.py

import wx

class SuccessDialog(wx.Dialog):
	""" Create a dialog that displays the results of optimizations.
	
	Parameter :
		- results_success -- A list [[corridor.name, r.success, r.message]...]
	"""
	def __init__(self, results_success):
		super(SuccessDialog, self).__init__(None) 
			
		self.SetSize((800,300))
		
		sizer = wx.BoxSizer(wx.VERTICAL)

		sizer.Add(wx.StaticText(self, label="Résultats des scénarios d'optimisation"), 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
		
		fgs = wx.FlexGridSizer(len(results_success), 3)
		
		for r in results_success:
			name = wx.StaticText(self, label=r[0]+" :")
			if r[1]:
				success = wx.StaticText(self, label="Succès")
				message = wx.StaticText(self, label="")
			else:
				success = wx.StaticText(self, label="Échec")
				message = wx.StaticText(self, label="Message : "+r[2])
			fgs.AddMany([	(name, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10),
							(success, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10),
							(message, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)])
		
		sizer.Add(fgs, 0, wx.ALL|wx.EXPAND, 20)
		ok_button = wx.Button(self, label='OK')
		ok_button.Bind(wx.EVT_BUTTON, self.OnOK)
		sizer.Add(ok_button, 0, wx.ALL|wx.EXPAND, 10)
		self.SetSizer(sizer)
		self.Layout()
	
	def OnOK(self, e):
		self.Destroy()	
	
