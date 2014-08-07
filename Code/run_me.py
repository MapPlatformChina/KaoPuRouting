#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is a lib file for Kao Pu Routing program 
# Created in 2014
# ######################################################################
import sys
from Tkinter import *
import tkFileDialog
from BaseMap import *
from KPRouteMain import *
from RFBaseChart import *
from RFPannel import *
import datetime
from RFUtl import *

# unit test code

def main():
	print 'Initiate TK windows/framework and commponents ...',
	sys.stdout.flush()
	root_widget = Tk()
	inst = RFUtl(root_widget)
	inst.construct_layout()
	inst.draw()
	print 'done!\nStart to take events ...'
	sys.stdout.flush()
	root_widget.mainloop()

			
if __name__=='__main__':
	main()