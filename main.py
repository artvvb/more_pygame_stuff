from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
from PIL import Image

import font
import color
import tile
import unit

from ogl_2d import *

window = 0		# glut window number


TILE_TYPE = tile.RECT
MAP_SIZE_W, MAP_SIZE_H = 10, 10
WINDOW_SIZE_W, WINDOW_SIZE_H = 640, 480
FULLSCREEN = False
USEFONT = False
USETEX = True
RANGE = 2

TILE_ADJ = [
	(-1, 0),
	( 0,-1),
	( 1, 0),
	( 0, 1)
]

g_colors = {
"BACK":		color.d_color["BLACK"],
"FOW":		color.d_color["WHITE"] * 0.5,
"IN_LOS":  	color.d_color["WHITE"],
"SELECTED":	color.d_color["RED"],
"FOW_SELECTED": color.d_color["RED"] * 0.5
}

g_texnames = ["unit.png", "bound.png"]

class mygame:
	def __init__(self):
		self.width, self.height = WINDOW_SIZE_W, WINDOW_SIZE_H
		self.map_width, self.map_height = MAP_SIZE_W, MAP_SIZE_H
		self.size = (1.0 / self.map_width, 1.0 / self.map_height)
		self.selected = None
		self.tiles = []
		for y in range(self.map_height):
			for x in range(self.map_width):
				trgb = "FOW"
				ttex = g_texnames.index("bound.png")#(x+y*self.map_width)%2
				tx = x if TILE_TYPE == tile.RECT else (x + (0.5 if y%2 == 0 else 0.0))
				ty = y
				self.tiles.append(tile.tile(tx, ty, trgb, ttex, TILE_TYPE))
		self.init_window()
		self.init_callback()
		if USETEX: self.init_tex()
		self.targets=None#self.get_range_list(0, 0, RANGE)
		self.units = [
			unit.unit((0,0), g_texnames.index("unit.png"), 2),
			unit.unit((9,9), g_texnames.index("unit.png"), 3),
			unit.unit((3,6), g_texnames.index("unit.png"), 1),
			unit.unit((3,5), g_texnames.index("unit.png"), 0)
		]
		self.selected = None
	def coord_in_bounds(self, v2_c):
		return v2_c[0] >= 0 and v2_c[1] >= 0 and v2_c[0] < self.map_width and v2_c[1] < self.map_height
	def get_range_list(self, x, y, r):
		a_targ = [[] for i in range(r+1)]
		a_targ[0].append((int(x), int(y)))
		for i in range(1,r+1):
			for v2_tile in a_targ[i-1]:
				for v2_delta in TILE_ADJ:
					v2_coord = (v2_tile[0]+v2_delta[0], v2_tile[1]+v2_delta[1])
					if self.coord_in_bounds(v2_coord):
						for l in a_targ:
							if v2_coord in l:
								break
						else:
							a_targ[i].append(v2_coord)
		return a_targ
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
		self.genTextures(g_texnames)
	def reshape(self, w, h):
		self.width = w
		self.height = h
	def mouse(self, button, state, x, y):
		if TILE_TYPE == tile.RECT:
			rx = x * self.map_width // self.width
			ry = (self.height - y) * self.map_height // self.height
			ri = ry * self.map_width + rx
			if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
				for u in range(len(self.units)):
					if self.units[u].loc == (rx,ry):
						self.selected = u
						self.targets=self.get_range_list(rx, ry, self.units[u].moverange)
						break
				else:
					self.selected = None
					self.targets = None
			if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
				if self.get_range(self.targets, (rx, ry)) >= 0:
					for u in self.units:
						if u.loc == (rx,ry):
							break
					else:
						self.targets = self.get_range_list(rx, ry, self.units[self.selected].moverange)
						self.units[self.selected].loc = (rx, ry)
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
	def get_range(self, l2_range, v2_coord):
		if l2_range == None:
			return -1
		for i in range(len(l2_range)):
			if v2_coord in l2_range[i]:
				return i
		return -1
	def draw(self):
		refresh2d(1, 1, self.width, self.height)										# set mode to 2d
		
		glClear(GL_COLOR_BUFFER_BIT)
		if USETEX: glEnable(GL_TEXTURE_2D)
		if USEFONT:
			glColor3f(1.0, 1.0, 1.0);
			font.draw("Hello World!", 0.5, 0.5)
		else:
			for t in self.tiles:
				if USETEX:
					for u in self.units:
						if u.loc == t.loc:
							glBindTexture(GL_TEXTURE_2D, self.textures[u.tex])
							break
					else:
						glBindTexture(GL_TEXTURE_2D, self.textures[t.tex])
				
				r = self.get_range(self.targets, t.loc)
				if r != -1:
					for u in self.units:
						if u.loc == t.loc and u.loc != self.targets[0][0]:
							foo = False
							break
					else:
						foo = True
					if foo:
						c = g_colors["SELECTED"]
						c.r = float(self.units[self.selected].moverange+1-r) / (RANGE+1)# 0->1 1->0.5 2->0.33
					else:
						c = g_colors["FOW"]
					c.draw()
				else:
					g_colors["FOW"].draw()
				t.draw(self.size)
		glDisable(GL_TEXTURE_2D)		
		glutSwapBuffers()
		
# initialization

m = mygame()

glutMainLoop() # start everything