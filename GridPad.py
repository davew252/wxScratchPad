#!/usr/bin/env python

import wx
import  wx.grid as gridlib
import wx.lib.colourdb as colordb

class GridPad(wx.Frame):

	def __init__(self, parent, id, owner=None, topLevel = None, **kwargs):
		wx.Frame.__init__(self, parent, id, (owner or 'wxGridPad'),
				size=(1200, 800))
		colordb.updateColourDB()
		self.SetThemeEnabled(True)
		self.owner = owner
		self.topLevel = topLevel
		self.toolIDbase = wx.ID_HIGHEST + 1000
		self.curToolID = 0
		self.toolIDs = []
		self.panel = wx.Panel(self, -1)
		self.panel.SetBackgroundColour("SNOW")
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.initStatusBar()
		self.createMenuBar()
		self.createToolBar()
		self.createMainGrid(self.panel)
		self.setupToolFunctions()
	
	def setTable(self, table):
		self.mainGrid.SetTable(table, True)	# The second parameter means that the grid is to take ownership of the
		# table and will destroy it when done.  Otherwise you would need to keep
		# a reference to it and call it's Destroy method later.
	
	
	
	def prnt(self, text):
		#self.mainText.AppendText("\n" + text)
		wx.MessageBox(text)
		
	def initStatusBar(self):
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetFieldsCount(3)
		self.statusbar.SetStatusWidths([-1, -2, -3])
		
	def createToolBar(self):
		toolbar = self.CreateToolBar()
		for each in self.toolbarData():
			self.createSimpleTool(toolbar, *each)
		toolbar.AddSeparator()
		toolbar.Realize()

	def setupToolFunctions(self, funclist=None):
		if funclist:
			self.toolFuncs = funclist	#passed in from secondary client code creating this form
		else:
			self.toolFuncs = [self.tool1_click,  self.tool2_click,  self.tool3_click,  self.tool4_click,  self.tool5_click,
								self.tool6_click,  self.tool7_click,  self.tool8_click,  self.tool9_click,  self.tool10_click]
		self.toolFunc = dict(zip([id for tool, id in self.toolIDs], self.toolFuncs))
		#self.prnt(str(self.toolFunc))
		
	def disableTool(self, toolNumber):
		if toolNumber < 1 or toolNumber > len(self.toolFuncs):
			wx.MessageBox("Invalid tool number.")
		else:
			toolId = self.toolIDs[toolNumber - 1][1]
			self.toolFunc[toolId] = self.toolDisabled
			wx.MessageBox("Tool number " + str(toolNumber) + " has been disabled.")
	
	def toolDisabled(self):
		wx.MessageBox("Tool disabled.")

	def createSimpleTool(self, toolbar, label, filename, help, handler):
		if not label:
			toolbar.AddSeparator()
			return
		bmp = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		if self.curToolID == 0:
			self.curToolID = self.toolIDbase
		else:
			self.curToolID += 1
		tool = toolbar.AddSimpleTool(self.curToolID, bmp, label, help)
		self.toolIDs.append((tool, self.curToolID))
		#self.Bind(wx.EVT_MENU, handler, tool)
		self.Bind(wx.EVT_TOOL, handler, tool)
		#tool.Bind(wx.EVT_TOOL, handler, tool)	AttributeError: 'ToolBarToolBase' object has no attribute 'Bind'
	
	def toolbarData(self):		#f:/PythonWork/wxScratchPad/
		return (("1", "bookmark-new.png", "Do function 1", self.OnToolClick),				#("", "", "", ""),
				("2", "bookmark-new.png", "Do function 2", self.OnToolClick),
				("3", "bookmark-new.png", "Do function 3", self.OnToolClick),
				("4", "bookmark-new.png", "Do function 4", self.OnToolClick),
				("5", "bookmark-new.png", "Do function 5", self.OnToolClick),
				("6", "bookmark-new.png", "Do function 6", self.OnToolClick),
				("7", "bookmark-new.png", "Do function 7", self.OnToolClick),
				("8", "bookmark-new.png", "Do function 8", self.OnToolClick),
				("9", "bookmark-new.png", "Do function 9", self.OnToolClick),
				("10", "bookmark-new.png", "Do function 10", self.OnToolClick))

	def menuData(self):
		return [("&File", (
					("&New", "New Sketch file", self.OnNew),
					("&Open", "Open sketch file", self.OnOpen),
					("&Save", "Save sketch file", self.OnSave),
					("", "", ""),
					("About...", "Show about window", self.OnAbout),
					("&Quit", "Quit", self.OnCloseWindow)))]

	def createMenuBar(self):
		menuBar = wx.MenuBar()
		for eachMenuData in self.menuData():
			menuLabel = eachMenuData[0]
			menuItems = eachMenuData[1]
			menuBar.Append(self.createMenu(menuItems), menuLabel)
		self.SetMenuBar(menuBar)

	def createMenuItem(self, menu, label, status, handler, kind=wx.ITEM_NORMAL):
		if not label:
			menu.AppendSeparator()
			return
		menuItem = menu.Append(-1, label, status, kind)
		self.Bind(wx.EVT_MENU, handler, menuItem)

	def createMenu(self, menuData):
		menu = wx.Menu()
		for eachItem in menuData:
			if len(eachItem) == 2:
				label = eachItem[0]
				subMenu = self.createMenu(eachItem[1])
				menu.AppendMenu(wx.NewId(), label, subMenu)
			else:
				self.createMenuItem(menu, *eachItem)
		return menu


	def createMainGrid(self, panel):
		font = wx.Font(pointSize=10, family=wx.FONTFAMILY_DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, faceName="Verdana", encoding=wx.FONTENCODING_DEFAULT)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.mainGrid = gridlib.Grid(panel, -1)	#, style=wx.BORDER_THEME)
		#self.mainGrid.Font = font
		sizer.Add(self.mainGrid, proportion=1,  flag=wx.EXPAND)
		#box = wx.StaticBox(panel, -1, '', style=wx.BORDER_THEME)
		self.btnsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.btnpanel = wx.Panel(panel, -1, size = (100,50), style=wx.BORDER_THEME)
		self.btnpanel.SetBackgroundColour("snow")
		sizer.Add(self.btnpanel, proportion=0,  flag=wx.EXPAND)

		self.button1 = wx.Button(self.btnpanel, -1, "Test1")
		self.button2 = wx.Button(self.btnpanel, -1, "Test2")
		self.btnspacer = (20,20)
		self.btnsizer.Add(self.btnspacer, proportion=1)
		self.btnsizer.Add(self.button1, proportion=0,  flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)
		self.btnsizer.Add(self.button2, proportion=0,  flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)
		self.btnpanel.SetSizer(self.btnsizer)
		self.btnpanel.Fit()
		self.Bind(wx.EVT_BUTTON, self.button1_click, self.button1)
		self.Bind(wx.EVT_BUTTON, self.button2_click, self.button2)
		#sizer.Add(self.btnsizer, proportion=0, flag=wx.EXPAND|wx.ALL, border=3)

		panel.SetSizer(sizer)
		panel.Fit()
	
	#self.toolfuncs = []
# Just grouping the empty event handlers together
	def OnToolClick(self, event): 
		#prnt = self.prnt
		# print self.toolIDs
		# print "EventId: " + str(event.Id)	#Yes. This is the same as the tool id
		# tool = event.GetEventObject()		#this returns the TOOLBAR, not the tool
		# print "ToolId: " + str(tool.Id), "ToolLabel: " + tool.Label		#, tool.ShortHelp
		tool_id = [(tool, id) for tool, id  in self.toolIDs if id == event.Id]
		toolId = tool_id[0][1]
		# if tool:
			# tool = tool[0]
			# #prnt("Tool clicked is " + tool.ShortHelp)
			# if tool.ShortHelp == "1":
				# self.tool1_click()
		# else: prnt( "Tool not identified. Id = " + event.Id)
		self.toolFunc[toolId]()
		
	def OnButtonClick(self, event): 
		#prnt = self.prnt
		# print self.toolIDs
		# print "EventId: " + str(event.Id)	#Yes. This is the same as the tool id
		# tool = event.GetEventObject()		#this returns the TOOLBAR, not the tool
		# print "ToolId: " + str(tool.Id), "ToolLabel: " + tool.Label		#, tool.ShortHelp
		tool_id = [(tool, id) for tool, id  in self.toolIDs if id == event.Id]
		toolId = tool_id[0][1]
		# if tool:
			# tool = tool[0]
			# #prnt("Tool clicked is " + tool.ShortHelp)
			# if tool.ShortHelp == "1":
				# self.tool1_click()
		# else: prnt( "Tool not identified. Id = " + event.Id)
		self.toolFunc[toolId]()
		
	def tool1_click(self): 
		self.prnt( "You clicked tool button 1.")
	def tool2_click(self): 
		self.prnt( "You clicked tool button 2.")
	def tool3_click(self): 
		self.prnt( "You clicked tool button 3.")
	def tool4_click(self): 
		self.prnt( "You clicked tool button 4.")
	def tool5_click(self): 
		self.prnt( "You clicked tool button 5.")
	def tool6_click(self): 
		self.prnt( "You clicked tool button 6.")
	def tool7_click(self): 
		self.prnt( "You clicked tool button 7.")
	def tool8_click(self): 
		self.prnt( "You clicked tool button 8.")
	def tool9_click(self): 
		self.prnt( "You clicked tool button 9.")
	def tool10_click(self): 
		self.prnt( "You clicked tool button 10.")
	def button1_click(self): 
		self.prnt( "You clicked button 1.")
	def button2_click(self): 
		self.prnt( "You clicked button 2.")
		
	def OnNew(self, event): pass
	def OnSave(self, event): pass
	def OnOpen(self, event): pass
	def OnAbout(self, event): pass
	def OnCopy(self, event): pass
	def OnCut(self, event): pass
	def OnPaste(self, event): pass
	def OnOptions(self, event): pass
	def OnCloseWindow(self, event):
		if self.topLevel != None:
			try:
				self.topLevel.Restore()
			except:
				pass
		self.Destroy()

# if __name__ == '__main__':
	# app = wx.PySimpleApp(redirect=True)
	# frame = ScratchPad(parent=None,  id=-1)
	# frame.Show()
	# app.MainLoop()

	
	