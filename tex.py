from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
from PIL import Image

import font
import color

from ogl_2d import *

window = 0		# glut window number

HEX, RECT = 0, 1
TILE_TYPE = RECT
MAP_SIZE_W, MAP_SIZE_H = 10, 10
WINDOW_SIZE_W, WINDOW_SIZE_H = 640, 480
FULLSCREEN = False
USEFONT = False


g_colors = {
"BACK":		color.d_color["BLACK"],
"FOW":		color.d_color["WHITE"] * 0.5,
"IN_LOS":  	color.d_color["WHITE"],
"SELECTED":	color.d_color["RED"],
"FOW_SELECTED": color.d_color["RED"] * 0.5
}
class mygame:
	def __init__(self):
		self.width, self.height = WINDOW_SIZE_W, WINDOW_SIZE_H
		self.map_width, self.map_height = MAP_SIZE_W, MAP_SIZE_H
		self.size = (1.0 / self.map_width, 1.0 / self.map_height)
		self.selected = None
		
		if TILE_TYPE == RECT:
			self.rects = []
		elif TILE_TYPE == HEX:
			self.hexes = []
			
		for y in range(self.map_height):
			for x in range(self.map_width):
				ci = "FOW"
				ti = (x+y*self.map_width)%2
				if TILE_TYPE == RECT:
					self.rects.append(rect(x, y, ci, ti))
				elif TILE_TYPE == HEX:
					self.hexes.append(hex(x + (0.5 if y%2==0 else 0.0), y, ci, ti))
		
		self.init_window()
		self.init_callback()
		self.init_tex()
		
	def init_window(self):
		glutInit()											   # initialize glut
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(self.width, self.height)					   # set window size
		glutInitWindowPosition(0, 0)						   # set window position
		self.window = glutCreateWindow(b'Hello World!')			   # create window with title
		if FULLSCREEN: glutFullScreen()
	def init_callback(self):
		glutDisplayFunc(lambda: m.draw())					   # set draw function callback
		glutIdleFunc(lambda: m.draw())						   # draw all the time
		glutMouseFunc(lambda button, state, x, y: m.mouse(button, state, x, y))
		glutKeyboardFunc(lambda key, x, y: m.keyboard(key, x, y))
		glutReshapeFunc(lambda w, h: self.reshape(w, h))
	def init_tex(self):
		self.genTextures(["sample.png", "sample2.png"])
	def reshape(self, w, h):
		self.width = w
		self.height = h
	def mouse(self, button, state, x, y):
		if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
			if TILE_TYPE == RECT:
				#assumes that rects list has not changed order
				rx = x * self.map_width // self.width
				ry = (self.height - y) * self.map_height // self.height
				ri = ry * self.map_width + rx
				if self.rects[ri].rgb == "FOW":
					self.rects[ri].rgb = "FOW_SELECTED"
				elif self.rects[ri].rgb == "FOW_SELECTED":
					self.rects[ri].rgb = "FOW"
			else:
				print("check")
				
				
			
	def keyboard(self, key, x, y):
		if key == b'\x1b':
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
		
		glClear(GL_COLOR_BUFFER_BIT)
		glEnable(GL_TEXTURE_2D)
		
		if USEFONT:
			glColor3f(1.0, 1.0, 1.0);
			font.draw("Hello World!", 0.5, 0.5)
		else:
			if TILE_TYPE == RECT:
				for r in range(len(self.rects)):
					glBindTexture(GL_TEXTURE_2D, self.textures[self.rects[r].tex])
					g_colors[self.rects[r].rgb].draw()
					self.rects[r].draw(self.size)
			elif TILE_TYPE == HEX:
				for h in range(len(self.hexes)):
					glBindTexture(GL_TEXTURE_2D, self.textures[self.hexes[h].tex])
					g_colors[self.hexes[h].rgb].draw()
					self.hexes[h].draw(self.size)
		glDisable(GL_TEXTURE_2D)
		
		glutSwapBuffers()
		
		
		
# initialization

m = mygame()

glutMainLoop()										   # start everything