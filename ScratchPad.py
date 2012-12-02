#!/usr/bin/env python

import wx

class ScratchPad(wx.Frame):

	def __init__(self, parent, id, owner=None, topLevel = None, **kwargs):
		wx.Frame.__init__(self, parent, id, (owner or 'wxScratchPad'),
				size=(1200, 800))
		self.owner = owner
		self.topLevel = topLevel
		self.toolIDbase = wx.ID_HIGHEST + 1000
		self.curToolID = 0
		self.toolIDs = []
		panel = wx.Panel(self, -1)
		panel.SetBackgroundColour("Snow")
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.initStatusBar()
		self.createMenuBar()
		self.createToolBar()
		self.createMainTextField(panel)
		self.setupToolFunctions()
	
	def prnt(self, text):
		self.mainText.AppendText("\n" + text)
		
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

	# def buttonData(self):
		# return (("1", self.On1),  ("2", self.On2),   ("3", self.On3),  ("4", self.On4),   ("5", self.On5),
				# ("6", self.On6),  ("7", self.On7),   ("8", self.On8),   ("9", self.On9),  ("10", self.On10)
				# )

	# def createButtonBar(self, panel, yPos = 0):
		# xPos = 0
		# for eachLabel, eachHandler in self.buttonData():
			# pos = (xPos, yPos)
			# button = self.buildOneButton(panel, eachLabel, eachHandler, pos)
			# button.Size = (40, 25)
			# xPos += button.GetSize().width +2

	# def buildOneButton(self, parent, label, handler, pos=(0,0)):
		# button = wx.Button(parent, -1, label, pos)
		# self.Bind(wx.EVT_BUTTON, handler, button)
		# return button

	def createMainTextField(self, panel):
		font = wx.Font(pointSize=12, family=wx.FONTFAMILY_DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, faceName="Verdana", encoding=wx.FONTENCODING_DEFAULT)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.mainText = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE, name = "MainText")
		self.mainText.Font = font
		sizer.Add(self.mainText, proportion=1,  flag=wx.EXPAND)
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
		
	def tool1_click(self): 
		self.prnt( "You clicked button 1.")
	def tool2_click(self): 
		self.mainText.Clear()
	def tool3_click(self): 
		self.prnt( "You clicked button 3.")
	def tool4_click(self): 
		self.prnt( "You clicked button 4.")
	def tool5_click(self): 
		self.prnt( "You clicked button 5.")
	def tool6_click(self): 
		self.prnt( "You clicked button 6.")
	def tool7_click(self): 
		self.prnt( "You clicked button 7.")
	def tool8_click(self): 
		self.prnt( "You clicked button 8.")
	def tool9_click(self): 
		self.prnt( "You clicked button 9.")
	def tool10_click(self): 
		self.prnt( "You clicked button 10.")
		
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

if __name__ == '__main__':
	app = wx.PySimpleApp(redirect=True)
	frame = ScratchPad(parent=None,  id=-1, style=wx.BORDER_THEME)
	frame.Show()
	app.MainLoop()
