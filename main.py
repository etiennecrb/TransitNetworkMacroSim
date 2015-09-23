#!/usr/bin/python
# -*- coding: utf-8 -*-

# main.py

import wx
import ui
import model as m

class Software():
	""" This class launch the software. """
	
	def __init__(self):
		model = m.Model()
		
		app = wx.App()
		window = ui.MainWindow(model)
		app.MainLoop()


if __name__ == '__main__':
	Software()
