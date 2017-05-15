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
	