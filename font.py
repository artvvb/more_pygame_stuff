from OpenGL.GL import *
from OpenGL.GLUT import *

def draw( str, x, y ):
	glRasterPos2f( x, y )
	for i in range(len(str)):
		glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(str[i]))
		