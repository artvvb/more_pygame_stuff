from OpenGL.GL import *
from OpenGL.WGL import wglUseFontBitmaps
from OpenGL.WGL import wglGetCurrentDC

from win32ui import CreateFont
from win32ui import CreateDCFromHandle

ESCAPE = '\033'
base = None

def initialize():
	global base
	wgldc = wglGetCurrentDC()
	hDC = CreateDCFromHandle(wgldc)
	base = glGenLists(32+96)
	font_properties = {
		"name" : "Courier New",
		"width" : 0,
		"height" : -24,
		"weight" : 800
	}
	font = CreateFont(font_properties)
	oldfont = hDC.SelectObject(font)
	wglUseFontBitmaps(wgldc, 32, 96, base+32)
	hDC.SelectObject(oldfont)
	
def cleanup():
	global base
	glDeleteLists(base, 32+96)
	
def draw(s, x, y):
	glRasterPos2f(x, y)
	glPrint(s)
	
def glPrint (str):
	""" // Custom GL "Print" Routine
	"""
	global base
	# // If THere's No Text Do Nothing
	if (str == None):
		return
	if (str == ""):
		return
	glPushAttrib(GL_LIST_BIT);							# // Pushes The Display List Bits
	try:
		glListBase(base);								# // Sets The Base Character to 32
		glCallLists(str)									# // Draws The Display List Text
	finally:
		glPopAttrib();										# // Pops The Display List Bits