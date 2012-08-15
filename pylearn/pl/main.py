#!/usr/bin/python -OO

import gtk
import gettext

#t = gettext.translation('pylearn', '../langs')
#_ = t.ugettext
def _(text):
	return text
 
class main:
	def __init__(self):
		self._create_window()
		self._create_menu()
		self._create_dashboard()

	def _create_window(self):
		self.window = gtk.Window()
		self.window.set_title(_("PyLearn"))
		self.window.resize(500,500)
		self.window.show()

	def _create_menu(self):
		return None
		
	def _create_dashboard(self):
		return None
