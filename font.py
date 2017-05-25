from OpenGL.GL import *
from OpenGL.GLUT import *
import tile

def draw( str, x, y, with_rect=False, window_size=(0,0), size=(0,0) ):
	if with_rect:
		tex2d_enabled = glIsEnabled(GL_TEXTURE_2D)
		if tex2d_enabled:
			glDisable(GL_TEXTURE_2D)
		glColor3f(1.0, 1.0, 1.0)
		tile.draw_rect(
			x,
			y + 15.0 / window_size.y,
			8.0 * len(str) / window_size.x,
			-1.0 * 15 / window_size.y,
			size,
			True
		)
		if tex2d_enabled:
			glEnable(GL_TEXTURE_2D)
	glColor3f(0.0, 0.0, 0.0)
	glRasterPos2f( x, y )
	for i in range(len(str)):
		glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(str[i]))
		