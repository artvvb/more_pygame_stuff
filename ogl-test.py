from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window = 0											   # glut window number
							   # window size
def refresh2d(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()
"""
def draw_rect(x, y, width, height):
	glBegin(GL_QUADS)								   # start drawing a rectangle
	glVertex2f(x, y)								   # bottom left point
	glVertex2f(x + width, y)						   # bottom right point
	glVertex2f(x + width, y + height)				   # top right point
	glVertex2f(x, y + height)						   # top left point
	glEnd()											   # done drawing a rectangle	
	
def draw():											   # ondraw is called all the time
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
	glLoadIdentity()								   # reset position
	refresh2d(width, height)						   # set mode to 2d
	 
	glColor3f (0.0,0.0,1.0)
	draw_rect(10,10,200,100)
	# ToDo draw rectangle
	
	glutSwapBuffers()								   # important for double buffering
"""
	
class color:
	def __init__(self, r, g, b):
		self.r, self.g, self.b = r, g, b
	def draw(self):
		glColor3f(self.r, self.g, self.b)
class rect:
	def __init__(self, x, y, dx, dy, color):
		self.x, self.y, self.dx, self.dy, self.color = x, y, dx, dy, color
	def draw(self):
		self.color.draw()
		glBegin(GL_QUADS)
		glVertex2f(self.x, self.y)
		glVertex2f(self.x + self.dx, self.y)
		glVertex2f(self.x + self.dx, self.y + self.dy)
		glVertex2f(self.x, self.y + self.dy)
		glEnd()
class mygame:
	def __init__(self):
		self.width, self.height = 500, 400
		
		self.rects = []
		for x in range(5):
			for y in range(5):
				if x%2 == 0 and y%2 == 0:
					c = color(1.0, 0.0, 0.0)
				elif x%2 == 0:
					c = color(0.0, 1.0, 0.0)
				elif y%2 == 0:
					c = color(0.0, 0.0, 1.0)
				else:
					c = color(1.0, 0.0, 1.0)
				self.rects.append(rect(20*x, 20*y, 20, 20, c))
		
		glutInit()											   # initialize glut
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(self.width, self.height)					   # set window size
		glutInitWindowPosition(0, 0)						   # set window position
		window = glutCreateWindow(b'Hello World!')			   # create window with title
		glutDisplayFunc(lambda: m.draw())					   # set draw function callback
		glutIdleFunc(lambda: m.draw())						   # draw all the time
		glutMouseFunc(lambda button, state, x, y: m.mouse(button, state, x, y))
	def mouse(self, button, state, x, y):
		if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
			print("check")
	def draw(self):											   # ondraw is called all the time
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
		glLoadIdentity()								   # reset position
		refresh2d(self.width, self.height)						   # set mode to 2d
		
		for r in self.rects:
			r.draw()
		
		glutSwapBuffers()								   # important for double buffering

# initialization

m = mygame()

glutMainLoop()										   # start everything