from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
from PIL import Image

import font

from ogl_2d import *

window = 0		# glut window number


class mygame:
	def __init__(self):
		self.width, self.height = 640, 480
		self.map_width, self.map_height = 100,100
		self.size = (1.0 / self.map_width, 1.0 / self.map_height)
		self.rects = []
		self.hexes = []
		self.color_names = ["red", "green", "blue", "magenta"]
		for x in range(self.map_width):
			for y in range(self.map_height):
				ci = 2*(y%2)+(x%2)
				ti = (x+y*self.map_width)%2
				self.rects.append(rect(x, y, ci, ti))
				self.hexes.append(hex(x + (0.5 if y%2==0 else 0.0), y, ci, ti))
				
		#self.rects.sort(key=lambda foo: foo.rgb)#order of rects list does not affect draw()
		glutInit()											   # initialize glut
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(self.width, self.height)					   # set window size
		glutInitWindowPosition(0, 0)						   # set window position
		self.window = glutCreateWindow(b'Hello World!')			   # create window with title
		#glutFullScreen()
		glutDisplayFunc(lambda: m.draw())					   # set draw function callback
		glutIdleFunc(lambda: m.draw())						   # draw all the time
		glutMouseFunc(lambda button, state, x, y: m.mouse(button, state, x, y))
		glutKeyboardFunc(lambda key, x, y: m.keyboard(key, x, y))
		glutReshapeFunc(lambda w, h: self.reshape(w, h))
		#font.initialize()
		self.genTextures(["sample.png", "sample2.png"])
	def reshape(self, w, h):
		self.width = w
		self.height = h
	def mouse(self, button, state, x, y):
		if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
			print("check")
	def keyboard(self, key, x, y):
		if key == b'\x1b':
			#font.cleanup()
			exit()
	def genTextures(self, filenames):
		self.textures = glGenTextures(len(filenames))
		for i in range(len(filenames)):
			img = Image.open(filenames[i])
			img_data = numpy.array(list(img.getdata()), numpy.uint8)

			#texture = glGenTextures(1)
			glPixelStorei(GL_UNPACK_ALIGNMENT,1)
			glBindTexture(GL_TEXTURE_2D, self.textures[i])

			# Texture parameters are part of the texture object, so you need to 
			# specify them only once for a given texture object.
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
			glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

	def draw(self):
		refresh2d(1, 1, self.width, self.height)										# set mode to 2d
		
		"""
		w, h = self.width, self.height
		glViewport(0, 0, w, h)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, 1, 0, 1, 0, 1)

#		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		"""
		glClear(GL_COLOR_BUFFER_BIT)

		#glColor3f(1.0, 1.0, 1.0);
		#font.draw("Hello World!", 0.5, 0.5)
		
		glEnable(GL_TEXTURE_2D)
		"""
		for r in range(len(self.rects)):
			glBindTexture(GL_TEXTURE_2D, self.textures[self.rects[r].tex])
			COLOR_TABLE[self.color_names[self.rects[r].rgb]].draw()
			self.rects[r].draw(self.size)
		"""
		for h in range(len(self.hexes)):
			glBindTexture(GL_TEXTURE_2D, self.textures[self.hexes[h].tex])
			COLOR_TABLE[self.color_names[self.hexes[h].rgb]].draw()
			self.hexes[h].draw(self.size)
		glDisable(GL_TEXTURE_2D)
		#"""
		# swap the front and back buffers so that the texture is visible
		glutSwapBuffers()
		
		
		
# initialization

m = mygame()

glutMainLoop()										   # start everything