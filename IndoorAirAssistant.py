#-*-coding:utf-8-*-

import numpy 
import math 
import wx  
from collections import OrderedDict
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from getoutdoorozone import IPToLocation
from getoutdoorozone import GetAQI

class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, 'Indoor Air Assistant', size = (800,600))
		panel = wx.Panel(self)
		self.backgroundcolour = '#F5F5F5' #whitesmoke
		panel.SetBackgroundColour(self.backgroundcolour)
		self.paneldraw = wx.Panel(panel, wx.ID_ANY, style=wx.NO_BORDER, pos = (200,340), size = wx.Size(560,190))
		self.paneldraw.SetBackgroundColour(self.backgroundcolour)
		self.paneldraw.Show(False)
		self.panellogo = wx.Panel(panel, wx.ID_ANY, style=wx.NO_BORDER, pos = (500,8), size = wx.Size(283,54))

		self.SetMaxSize((800,600)) #fix the frame size
		self.SetMinSize((800,600)) #fix the frame size

		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText('Welcome to Indoor Air Assistant...')
		
		#information
		self.info = wx.StaticText(panel, -1, 'Version: 1.1.0.20170310_release\nReleased by Air Lab in NJU\nAll rights reserved by author', (10,490))
		self.info.SetForegroundColour('grey')
		ifont = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.info.SetFont(ifont)

		#show logo image
		image = wx.Image("newlogo.jpg",wx.BITMAP_TYPE_JPEG)
		logo = wx.StaticBitmap(self.panellogo, -1, wx.BitmapFromImage(image))
		
		#your city
		citylabel1 = wx.StaticText(panel, -1, 'Your City:', (20,15))
		try:
			ip = IPToLocation()
			cityname = ip.city().decode('utf-8')
			self.city = wx.StaticText(panel, -1, cityname, (50,40), (80,-1))
			self.statusbar.SetStatusText('Welcome to Indoor Air Assistant...')
		except:
			self.city = wx.StaticText(panel, -1, 'Offline', (50,40), (80,-1))
			self.statusbar.SetStatusText('You are offline! Please check your internet connection...')

		#outdoor ozone
		self.outppb = wx.SpinCtrl(panel, -1, 'Outdoor Ozone', (30,100), (80,-1))
		self.outppb.SetRange(0,10000)
		outppblabel1 = wx.StaticText(panel, -1, 'Outdoor Ozone:', (20,75))
		outppblabel2 = wx.StaticText(panel, -1, 'ppb', (115,100))
		self.outppb.Bind(wx.EVT_TEXT, self.OutPpb)
		try:
			webozone = GetAQI(cityname)
			webozone = int(webozone.ozone())
			self.outppb.SetValue(webozone)
			self.statusbar.SetStatusText('Welcome to Indoor Air Assistant...')
		except:
			self.outppb.SetValue(100)
			self.statusbar.SetStatusText('You are offline! Please check your internet connection...')

		#air change rate
		self.ach = wx.Slider(panel, -1, 5, 0, 50, (20,160), (90,-1), 
			style = wx.SL_HORIZONTAL|wx.SL_TOP)
		self.ach.Bind(wx.EVT_SCROLL, self.ACHScroll)
		self.achvalue = wx.TextCtrl(panel, -1, str(self.ach.GetValue()/10.0), (110,160), (35,-1))
		self.achvalue.Bind(wx.EVT_TEXT, self.ACHText)
		self.achlabel1 = wx.StaticText(panel, -1, 'Air Change Per Hour:', (20,135))
		self.achlabel2 = wx.StaticText(panel, -1, '/h', (150,160))

		#indoor source
		self.indoorsource = wx.TextCtrl(panel, -1, '0', (30,220), (80,-1))
		self.indoorsource.Bind(wx.EVT_TEXT, self.IndoorSourceText)
		indoorsourcelabel1 = wx.StaticText(panel, -1, 'Indoor Source:', (20,195))
		indoorsourcelabel2 = wx.StaticText(panel, -1, 'mg/h', (115,220))

		#disinfection
		self.disinfection = wx.CheckBox(panel,-1,'Disinfection',pos = (20,255),size=(100,-1))
		self.disinfection.Bind(wx.EVT_CHECKBOX, self.Disinfection)
		self.disinfectionlabel = wx.StaticText(panel, -1, 'Disinfection Settings', (20,290))
		self.disinfectionlabel.SetForegroundColour('red')
		dfont = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.BOLD)
		self.disinfectionlabel.SetFont(dfont)
		self.disinfectionlabel.Enable(False)

		#disinfection time
		self.dtime = wx.SpinCtrl(panel, -1, 'Disinfection Time', (30,340), (80,-1))
		self.dtime.SetRange(0,300)
		self.dtime.SetValue(30)
		self.dtimelabel1 = wx.StaticText(panel, -1, 'Disinfection Time:', (20,315))
		self.dtimelabel2 = wx.StaticText(panel, -1, 'min', (115,340))
		self.dtime.Bind(wx.EVT_TEXT, self.DTime)
		self.dtime.Enable(False)
		self.dtimelabel1.Enable(False)
		self.dtimelabel2.Enable(False)

		#ach during disinfection 
		self.achd1 = wx.Slider(panel, -1, 5, 0, 50, (20,400), (90,-1), 
			style = wx.SL_HORIZONTAL|wx.SL_TOP)
		self.achd1.Bind(wx.EVT_SCROLL, self.ACHD1Scroll)
		self.achvalued1 = wx.TextCtrl(panel, -1, str(self.ach.GetValue()/10.0), (110,400), (35,-1))
		self.achvalued1.Bind(wx.EVT_TEXT, self.ACHD1Text)
		self.achd1label1 = wx.StaticText(panel, -1, 'ACH During Disinfection:', (20,375))
		self.achd1label2 = wx.StaticText(panel, -1, '/h', (150,400))
		self.achd1.Enable(False)
		self.achvalued1.Enable(False)
		self.achd1label1.Enable(False)
		self.achd1label2.Enable(False)

		#ach after disinfection 
		self.achd2 = wx.Slider(panel, -1, 5, 0, 50, (20,460), (90,-1), 
			style = wx.SL_HORIZONTAL|wx.SL_TOP)
		self.achd2.Bind(wx.EVT_SCROLL, self.ACHD2Scroll)
		self.achvalued2 = wx.TextCtrl(panel, -1, str(self.ach.GetValue()/10.0), (110,460), (35,-1))
		self.achvalued2.Bind(wx.EVT_TEXT, self.ACHD2Text)
		self.achd2label1 = wx.StaticText(panel, -1, 'ACH After Disinfection:', (20,435))
		self.achd2label2 = wx.StaticText(panel, -1, '/h', (150,460))
		self.achd2.Enable(False)
		self.achvalued2.Enable(False)
		self.achd2label1.Enable(False)
		self.achd2label2.Enable(False)

		#room volume
		self.volume = wx.TextCtrl(panel, -1, '45', (200,40), (80,-1))
		self.volume.Bind(wx.EVT_TEXT, self.VolumeText)
		volumelabel1 = wx.StaticText(panel, -1, 'Room Volume:', (190,15))
		volumelabel2 = wx.StaticText(panel, -1, 'm3', (285,40))

		#material 1
		materiallist = list(material.keys())

		self.material1 = wx.Choice(panel, -1, pos = (200,100), size = (180,-1), choices = materiallist)
		self.material1.SetSelection(13)
		self.area1 = wx.TextCtrl(panel, -1, '15', (390,100), (40,-1))
		materiallabel1 = wx.StaticText(panel, -1, 'Floor:', (190,75))
		arealabel1 = wx.StaticText(panel, -1, 'm2', (435,100))
		self.material1.Bind(wx.EVT_CHOICE, self.ChooseMaterial1)
		self.area1.Bind(wx.EVT_TEXT, self.AreaText1)

		#material 2
		self.material2 = wx.Choice(panel, -1, pos = (200,160), size = (180,-1), choices = materiallist)
		self.material2.SetSelection(21)
		self.area2 = wx.TextCtrl(panel, -1, '15', (390,160), (40,-1))
		materiallabel2 = wx.StaticText(panel, -1, 'Ceiling:', (190,135))
		arealabel2 = wx.StaticText(panel, -1, 'm2', (435,160))
		self.material2.Bind(wx.EVT_CHOICE, self.ChooseMaterial2)
		self.area2.Bind(wx.EVT_TEXT, self.AreaText2)

		#material 3
		self.material3 = wx.Choice(panel, -1, pos = (200,220), size = (180,-1), choices = materiallist)
		self.material3.SetSelection(19)
		self.area3 = wx.TextCtrl(panel, -1, '30', (390,220), (40,-1))
		materiallabel3 = wx.StaticText(panel, -1, 'Wall1:', (190,195))
		arealabel3 = wx.StaticText(panel, -1, 'm2', (435,220))
		self.material3.Bind(wx.EVT_CHOICE, self.ChooseMaterial3)
		self.area3.Bind(wx.EVT_TEXT, self.AreaText3)

		#material 4
		self.material4 = wx.Choice(panel, -1, pos = (200,280), size = (180,-1), choices = materiallist)
		self.material4.SetSelection(21)
		self.area4 = wx.TextCtrl(panel, -1, '18', (390,280), (40,-1))
		materiallabel4 = wx.StaticText(panel, -1, 'Wall2:', (190,255))
		arealabel4 = wx.StaticText(panel, -1, 'm2', (435,280))
		self.material4.Bind(wx.EVT_CHOICE, self.ChooseMaterial4)
		self.area4.Bind(wx.EVT_TEXT, self.AreaText4)

		#material 5
		self.material5 = wx.Choice(panel, -1, pos = (500,100), size = (180,-1), choices = materiallist)
		self.material5.SetSelection(39)
		self.area5 = wx.TextCtrl(panel, -1, '15', (690,100), (40,-1))
		materiallabel5 = wx.StaticText(panel, -1, 'Surface:', (490,75))
		arealabel5 = wx.StaticText(panel, -1, 'm2', (735,100))
		self.material5.Bind(wx.EVT_CHOICE, self.ChooseMaterial5)
		self.area5.Bind(wx.EVT_TEXT, self.AreaText5)

		#material 6
		self.material6 = wx.Choice(panel, -1, pos = (500,160), size = (180,-1), choices = materiallist)
		self.material6.SetSelection(45)
		self.area6 = wx.TextCtrl(panel, -1, '10', (690,160), (40,-1))
		materiallabel6 = wx.StaticText(panel, -1, 'Surface:', (490,135))
		arealabel6 = wx.StaticText(panel, -1, 'm2', (735,160))
		self.material6.Bind(wx.EVT_CHOICE, self.ChooseMaterial6)
		self.area6.Bind(wx.EVT_TEXT, self.AreaText6)

		#material 7
		self.material7 = wx.Choice(panel, -1, pos = (500,220), size = (180,-1), choices = materiallist)
		self.material7.SetSelection(0)
		self.area7 = wx.TextCtrl(panel, -1, '0', (690,220), (40,-1))
		materiallabel7 = wx.StaticText(panel, -1, 'Surface:', (490,195))
		arealabel7 = wx.StaticText(panel, -1, 'm2', (735,220))
		self.material7.Bind(wx.EVT_CHOICE, self.ChooseMaterial7)
		self.area7.Bind(wx.EVT_TEXT, self.AreaText7)

		#material 8
		self.material8 = wx.Choice(panel, -1, pos = (500,280), size = (180,-1), choices = materiallist)
		self.material8.SetSelection(0)
		self.area8 = wx.TextCtrl(panel, -1, '0', (690,280), (40,-1))
		materiallabel8 = wx.StaticText(panel, -1, 'Surface:', (490,255))
		arealabel8 = wx.StaticText(panel, -1, 'm2', (735,280))
		self.material8.Bind(wx.EVT_CHOICE, self.ChooseMaterial8)
		self.area8.Bind(wx.EVT_TEXT, self.AreaText8)

		#show inppb result
		self.inppb = wx.StaticText(panel, -1, 'Ozone', pos = (350,410), size = (200,-1), style = wx.ALIGN_RIGHT)
		self.inppb.SetForegroundColour('blue')
		font = wx.Font(30, wx.ROMAN, wx.NORMAL, wx.BOLD)
		self.inppb.SetFont(font)
		inppblabel = wx.StaticText(panel, -1, 'Indoor Ozone: ', (190,315))

	#draw disinfection ppb curve
	def DrawPpb(self):
		inppbresults = []
		ta = 5*self.dtime.GetValue()
		for t in xrange(ta+1):
			inppbresults.append(eqdynamic(float(self.outppb.GetValue()), 
				self.achd1.GetValue()/10.0, self.achd2.GetValue()/10.0, 
				float(self.volume.GetValue()), 
				float(self.indoorsource.GetValue()), 
				getsumvda(material.get(self.material1.GetStringSelection()), 
					float(self.area1.GetValue()), 
					material.get(self.material2.GetStringSelection()), 
					float(self.area2.GetValue()), 
					material.get(self.material3.GetStringSelection()), 
					float(self.area3.GetValue()), 
					material.get(self.material4.GetStringSelection()), 
					float(self.area4.GetValue()), 
					material.get(self.material5.GetStringSelection()), 
					float(self.area5.GetValue()), 
					material.get(self.material6.GetStringSelection()), 
					float(self.area6.GetValue()), 
					material.get(self.material7.GetStringSelection()), 
					float(self.area7.GetValue()), 
					material.get(self.material8.GetStringSelection()), 
					float(self.area8.GetValue()), 
					getvt(self.ach.GetValue()/10.0) ), t/60., 
				self.dtime.GetValue()/60.))
		
		t_score = numpy.arange(0, ta+1, 1)
		s_score = numpy.array(inppbresults)

		self.figure_score = Figure()
		self.figure_score.set_facecolor(self.backgroundcolour)
		self.figure_score.set_figheight(2.4)
		self.figure_score.set_figwidth(7.2)
		self.axes_score = self.figure_score.add_subplot(111) #seperate the window into 1*1 matrix (subwindows), occupied the 1st subwindow

		self.axes_score.plot(t_score, s_score, 'b')
		self.axes_score.axhline(y = 140, color='r')
		#self.axes_score.set_title('Indoor Ozone')
		self.axes_score.grid(True)
		self.axes_score.set_xlabel('Time (min)')
		self.axes_score.set_ylabel('Indoor Ozone (ppb)')

		FigureCanvas(self.paneldraw, -1, self.figure_score)

	#show indoor ppb result
	def ShowPpb(self):
		return self.inppb.SetLabel(str(eqsteady(float(self.outppb.GetValue()), 
			self.ach.GetValue()/10.0, float(self.volume.GetValue()), 
			float(self.indoorsource.GetValue()), 
			getsumvda(material.get(self.material1.GetStringSelection()), 
				float(self.area1.GetValue()), 
				material.get(self.material2.GetStringSelection()), 
				float(self.area2.GetValue()), 
				material.get(self.material3.GetStringSelection()), 
				float(self.area3.GetValue()), 
				material.get(self.material4.GetStringSelection()), 
				float(self.area4.GetValue()), 
				material.get(self.material5.GetStringSelection()), 
				float(self.area5.GetValue()), 
				material.get(self.material6.GetStringSelection()), 
				float(self.area6.GetValue()), 
				material.get(self.material7.GetStringSelection()), 
				float(self.area7.GetValue()), 
				material.get(self.material8.GetStringSelection()), 
				float(self.area8.GetValue()), 
				getvt(self.ach.GetValue()/10.0) )))+' ppb')
	
	def OutPpb(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def ACHScroll(self, event):
		self.achvalue.SetValue(str(self.ach.GetValue()/10.0))
		self.ShowPpb()
		self.statusbar.SetStatusText('')
	
	def ACHText(self, event):
		try:
			if float(self.achvalue.GetValue()) >20.0:
				self.ach.SetValue(200)
				self.statusbar.SetStatusText('RangeError! Air change rate ranges from 0 to 5...')
			elif float(self.achvalue.GetValue()) <0.0:
				self.ach.SetValue(0)
				self.statusbar.SetStatusText('RangeError! Air change rate ranges from 0 to 5...')
			else:
				self.ach.SetValue(int(float(self.achvalue.GetValue())*10))
				self.statusbar.SetStatusText('')
			self.ShowPpb()
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number from 0 to 5...')

	def ACHD1Scroll(self, event):
		self.achvalued1.SetValue(str(self.achd1.GetValue()/10.0))
		self.DrawPpb()
		self.statusbar.SetStatusText('')
	
	def ACHD1Text(self, event):
		try:
			if float(self.achvalued1.GetValue()) >20.0:
				self.achd1.SetValue(200)
				self.statusbar.SetStatusText('RangeError! Air change rate ranges from 0 to 5...')
			elif float(self.achvalued1.GetValue()) <0.0:
				self.achd1.SetValue(0)
				self.statusbar.SetStatusText('RangeError! Air change rate ranges from 0 to 5...')
			else:
				self.achd1.SetValue(int(float(self.achvalued1.GetValue())*10))
				self.statusbar.SetStatusText('')
			self.DrawPpb()
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number from 0 to 5...')

	def ACHD2Scroll(self, event):
		self.achvalued2.SetValue(str(self.achd2.GetValue()/10.0))
		self.DrawPpb()
		self.statusbar.SetStatusText('')
	
	def ACHD2Text(self, event):
		try:
			if float(self.achvalued2.GetValue()) >20.0:
				self.achd2.SetValue(200)
				self.statusbar.SetStatusText('RangeError! Air change rate ranges from 0 to 5...')
			elif float(self.achvalued2.GetValue()) <0.0:
				self.achd2.SetValue(0)
				self.statusbar.SetStatusText('RangeError! Air change rate ranges from 0 to 5...')
			else:
				self.achd2.SetValue(int(float(self.achvalued2.GetValue())*10))
				self.statusbar.SetStatusText('')
			self.DrawPpb()
		except ValueError:
			self.statusbar.SetStatusText('ValueError! Please input a number from 0 to 20...')

	def IndoorSourceText(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def DTime(self, event):
		self.DrawPpb()
		self.statusbar.SetStatusText('')

	def VolumeText(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial1(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def AreaText1(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial2(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def AreaText2(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial3(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def AreaText3(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial4(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def AreaText4(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial5(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def AreaText5(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial6(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def AreaText6(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial7(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def AreaText7(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def ChooseMaterial8(self, event):
		if self.disinfection.IsChecked():
			self.DrawPpb()
		else:
			self.ShowPpb()
		self.statusbar.SetStatusText('')

	def AreaText8(self, event):
		if self.disinfection.IsChecked():
			try:
				self.DrawPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')
		else:
			try:
				self.ShowPpb()
				self.statusbar.SetStatusText('')
			except ValueError:
				self.statusbar.SetStatusText('ValueError! Please input a number...')

	def Disinfection(self, event):
		if self.disinfection.IsChecked():
			self.dtime.Enable(True)
			self.achd1.Enable(True)
			self.achvalued1.Enable(True)
			self.achd2.Enable(True)
			self.achvalued2.Enable(True)
			self.achd1label1.Enable(True)
			self.achd1label2.Enable(True)
			self.achd2label1.Enable(True)
			self.achd2label2.Enable(True)
			self.dtimelabel1.Enable(True)
			self.dtimelabel2.Enable(True)
			self.disinfectionlabel.Enable(True)
			self.paneldraw.Show(True)
			self.ach.Enable(False)
			self.achvalue.Enable(False)
			self.achlabel1.Enable(False)
			self.achlabel2.Enable(False)
			self.inppb.Show(False)
		else:
			self.dtime.Enable(False)
			self.achd1.Enable(False)
			self.achvalued1.Enable(False)
			self.achd2.Enable(False)
			self.achvalued2.Enable(False)
			self.achd1label1.Enable(False)
			self.achd1label2.Enable(False)
			self.achd2label1.Enable(False)
			self.achd2label2.Enable(False)
			self.dtimelabel1.Enable(False)
			self.dtimelabel2.Enable(False)
			self.disinfectionlabel.Enable(False)
			self.paneldraw.Show(False)
			self.ach.Enable(True)
			self.achvalue.Enable(True)
			self.achlabel1.Enable(True)
			self.achlabel2.Enable(True)
			self.inppb.Show(True)

def eqsteady(outppb, ach, v, source, sumvda):
	ppbsteady = float(float(ach)*(float(outppb)/500.)+float(source)/float(v))/(float(ach)+float(sumvda)/float(v))
	ppbsteady = ppbsteady*500.
	return round(ppbsteady, 1) #the unit of output ppbt is ppb, the convertion coefficient is 500; the input unit should also be ppb

def eqdynamic(outppb, achdis, achvent, v, source, sumvda, t, tdis):
	initppb = float(float(achdis)*(float(outppb)/500.))/(float(achdis)+float(sumvda)/float(v))
	ppbtdis = (initppb-float(float(achdis)*(float(outppb)/500.)+float(source)/float(v))/(float(achdis)+float(sumvda)/float(v)))*math.exp(-(float(achdis)+float(float(sumvda)/float(v)))*tdis)+float(float(achdis)*(float(outppb)/500.)+float(source)/float(v))/(float(achdis)+float(sumvda)/float(v))
	if t <= tdis:
		ppbt = (initppb-float(float(achdis)*(float(outppb)/500.)+float(source)/float(v))/(float(achdis)+float(sumvda)/float(v)))*math.exp(-(float(achdis)+float(float(sumvda)/float(v)))*t)+float(float(achdis)*(float(outppb)/500.)+float(source)/float(v))/(float(achdis)+float(sumvda)/float(v))
	else:
		ppbt = (ppbtdis-float(float(achvent)*(float(outppb)/500.))/(float(achvent)+float(sumvda)/float(v)))*math.exp(-(float(achvent)+float(float(sumvda)/float(v)))*(t-tdis))+float(float(achvent)*(float(outppb)/500.))/(float(achvent)+float(sumvda)/float(v))	
	ppbt = ppbt*500.
	return round(ppbt, 1) #the unit of output ppbt is ppb, the convertion coefficient is 500; the input unit should also be ppb

def getsumvda(r1, a1, r2, a2, r3, a3, r4, a4, r5, a5, r6, a6, r7, a7, r8, a8, vt):
	vd1 = 36.*(float(vt)*float(r1)*36000./(4.*float(vt)+float(r1)*36000.)) #convert cm/s to m/h (multiple conversion coefficient, 36)
	vd2 = 36.*(float(vt)*float(r2)*36000./(4.*float(vt)+float(r2)*36000.))
	vd3 = 36.*(float(vt)*float(r3)*36000./(4.*float(vt)+float(r3)*36000.))
	vd4 = 36.*(float(vt)*float(r4)*36000./(4.*float(vt)+float(r4)*36000.))
	vd5 = 36.*(float(vt)*float(r5)*36000./(4.*float(vt)+float(r5)*36000.))
	vd6 = 36.*(float(vt)*float(r6)*36000./(4.*float(vt)+float(r6)*36000.))
	vd7 = 36.*(float(vt)*float(r7)*36000./(4.*float(vt)+float(r7)*36000.))
	vd8 = 36.*(float(vt)*float(r8)*36000./(4.*float(vt)+float(r8)*36000.))
	sumvda = vd1*float(a1)+vd2*float(a2)+vd3*float(a3)+vd4*float(a4)+vd5*float(a5)+vd6*float(a6)+vd7*float(a7)+vd8*float(a8)
	return sumvda

def getvt(ach):
	vt = (float(ach)/5.)*0.6+0.1 #cm/s
	return vt
	
if __name__ == '__main__':
	#reaction probability of materials
	material = OrderedDict([
		('No material',0.0), ('Glass',6.06e-06), 
		('Lucite',5.50e-08), ('Metal, Aluminium',1.08e-07), 
		('Metal, Stainless steel',1.30e-06), ('Metal, Galvanized steel',1.10e-06), 
		('Ceramic',4.44e-07), ('Porcelain clay tile',1.02e-06), 
		('Resilient tile',1.11e-06), ('Concrete, Course',9.65e-06),
		('Concrete, Fine',4.20e-06), ('Stone material, Soft dense',7.82e-06), 
		('Stone material, Hard dense',1.67e-08), ('Floor, Wooden',1.20e-06), 
		('Floor, Finished hardwood',2.45e-06), ('Floor, Finished bamboo',1.95e-06), 
		('Ceiling tile, Perlite',1.02e-05), ('Ceiling tile, Mineral fiber',4.65e-05), 
		('Ceiling tile, Fiberglass',3.74e-05), ('Wallpaper',4.28e-06),
		('Fabric wall covering',5.30e-06), ('Paint, Latex',1.47e-06), 
		('Paint, Clay',5.65e-05), ('Paint, Water-based',4.90e-06), 
		('Paint, Oil-based',6.10e-06), ('Paint, Collagen',3.15e-06), 
		('Gypsum board, Painted',4.72e-06), ('Gypsum board, Untreated',1.73e-05), 
		('Wall plaster, Clay',2.20e-05), ('Green material, Sunflower',3.78e-06),
		('Green material, Cork',5.67e-06), ('Green material, Wheat',5.22e-06), 
		('Nylon',5.50e-08), ('FEP Teflon',5.50e-07), 
		('Rubber',6.86e-06), ('Neoprene',1.90e-06), 
		('Polyethylene sheet',1.51e-06),('PVC',1.68e-06),
		('Medium density fibreboard',4.50e-06), 
		('Particle board',5.00e-07), ('Plywood',5.80e-07),
		('Bamboo',4.44e-07), ('Cedar',5.20e-06), 
		('Woodwork, Fine, hard',5.59e-07), ('Woodwork, Course, soft',4.16e-06), 
		('Cloth, <1 year old',8.99e-06), ('Cloth, >1 year old',7.06e-07), 
		('Linoleum',7.89e-07), ('Linen',6.30e-07), 
		('Carpet, Recycled',3.20e-05), ('Carpet, Fabric-backed',2.30e-05),
		('Carpet, Nylon',1.38e-05), ('Carpet, Olefin',1.01e-05), 
		('Carpet, Wool',1.06e-05), ('Brick',1.59e-05), 
		('Activated carbon cloth',2.24e-05)
		]) 
	app = wx.App()
	MyFrame().Show()
	
	app.MainLoop()
