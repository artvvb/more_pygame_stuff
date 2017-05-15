from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
from PIL import Image

def refresh2d(vw, vh, width, height):
	glViewport(0, 0, width, height)
	glClearColor(0,0,0,0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 	# clear the screen
	glLoadIdentity()								   	# reset position
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, vw, 0.0, vh, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()
	

class color:
	def __init__(self, r, g, b):
		self.r, self.g, self.b = r, g, b
	def draw(self):
		glColor3f(self.r, self.g, self.b)
		
		
COLOR_TABLE = {
	"red":		color(1.0, 0.0, 0.0),
	"green":	color(0.0, 1.0, 0.0),
	"blue":		color(0.0, 0.0, 1.0),
	"magenta":	color(1.0, 0.0, 1.0)
}

class rect:
	def __init__(self, x, y, rgb, tex):
		self.rgb, self.tex = rgb, tex
		basecoords = [
			(0,0),
			(0,1),
			(1,1),
			(1,0)
		]
		self.coords = [(x + cx, y + cy) for cx, cy in basecoords]
		self.texcoords = [(cx, 1.0 - cy) for cx, cy in basecoords]
	def draw(self, size):
		glBegin(GL_QUADS)
		for i in range(4):
			glTexCoord2f(self.texcoords[i][0], self.texcoords[i][1])
			glVertex2f(self.coords[i][0] * size[0], self.coords[i][1] * size[1])
		glEnd()
HEX_BASECOORDS = [
	(0.43,0),
	(0.86,0.25),
	(0.86,0.75),
	(0.43,1.0),
	(0,0.75),
	(0,0.25)
]
class hex:
	def __init__(self, x, y, rgb, tex):
		self.rgb, self.tex = rgb, tex
		self.coords = [(x + cx, y + cy) for cx, cy in HEX_BASECOORDS]
		self.texcoords = [(cx / 0.86, 1.0 - cy) for cx, cy in HEX_BASECOORDS]
	def draw(self, size):
		glBegin(GL_POLYGON)
		for i in range(6):
			glTexCoord2f(self.texcoords[i][0], self.texcoords[i][1])
			glVertex2f(self.coords[i][0] * size[0], self.coords[i][1] * size[1])
		glEnd()
	
	
	