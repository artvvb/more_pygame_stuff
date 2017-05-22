from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
from PIL import Image

import font
import color
import tile
import unit
import tooltips
import random

window = 0		# glut window number

TILE_TYPE = tile.RECT
MAP_SIZE_W, MAP_SIZE_H = 10, 10
WINDOW_SIZE_W, WINDOW_SIZE_H = 640, 480
FULLSCREEN = False
USEFONT = False
USETEX = TILE_TYPE == tile.RECT
TEXDIR = "textures/"
TEXEXT = ".png"
RANDRANGE=(0,99)

TILE_ADJ = [
	(-1, 0),
	( 0,-1),
	( 1, 0),
	( 0, 1)
]
ARROW_ROT = {
	( 0, 1): 0,
	(-1, 0): 1,
	( 0,-1): 2,
	( 1, 0): 3,
	
	(-1,-1): 0,#
	( 1,-1): 3,
	(-1, 1): 1,#
	( 1, 1): 2
}


g_TILETEX = "bound" if TILE_TYPE == tile.RECT else "hex-bound"
g_texnames = ["unit", g_TILETEX, "arrow-u", "arrow-ud", "arrow-ur"]

def refresh2d(vw, vh, width, height):
	glViewport(0, 0, width, height)
	glClearColor(0, 0, 0, 0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, vw, 0.0, vh, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()

class mygame:
	def __init__(self):
		random.seed(None)
		
		self.width, self.height = WINDOW_SIZE_W, WINDOW_SIZE_H
		self.map_width, self.map_height = MAP_SIZE_W, MAP_SIZE_H
		self.size = (1.0 / self.map_width, 1.0 / self.map_height)
		self.selected = None
		
		self.tiles = []
		for y in range(self.map_height):
			for x in range(self.map_width):
				ttex = g_texnames.index(g_TILETEX)#(x+y*self.map_width)%2
				tx = x if TILE_TYPE == tile.RECT else (x + (0.5 if y%2 == 0 else 0.0))
				ty = y
				self.tiles.append(tile.tile(tx, ty, ttex, TILE_TYPE, random.randint(RANDRANGE[0], RANDRANGE[1])))
		
		self.init_window()
		self.init_callback()
		if USETEX: self.init_tex()
		self.l2v_movereg = None
		self.units = [
			unit.unit((0,0), g_texnames.index("unit"), 2),# * sum(RANDRANGE)/2),
			unit.unit((9,9), g_texnames.index("unit"), 3),# * sum(RANDRANGE)/2),
			unit.unit((3,6), g_texnames.index("unit"), 1),# * sum(RANDRANGE)/2),
			unit.unit((3,5), g_texnames.index("unit"), 0),# * sum(RANDRANGE)/2)
		]
		self.selected = None
		self.mouseloc = None
		self.wmouseloc = None
		self.tooltip = tooltips.tooltip(1.0)
		self.tooltip.start()
	def get_delta(self, v2_s, v2_d):
		if v2_s[0] > v2_d[0]:
			return (-1, 0)
		elif v2_s[0] < v2_d[0]:
			return ( 1, 0)
		elif v2_s[1] > v2_d[1]:
			return ( 0,-1)
		else:# v2_s[0] < v2_d[0]:
			return ( 0, 1)
	def get_path_tex(self, v2_s, v2_d):
		
		a_v2_path = {v2_s: (g_texnames.index("unit"), 0)}
		if v2_s == v2_d:
			return a_v2_path
		
		v2_t = v2_s
		v2_delta = self.get_delta(v2_t, v2_d)
		
		while v2_t != v2_d:
			v2_ldelta = v2_delta
			v2_delta = self.get_delta(v2_t, v2_d)
			
			if v2_delta != v2_ldelta:
				v2_rdelta = (v2_delta[0]+v2_ldelta[0], v2_delta[1]+v2_ldelta[1])
			else:
				v2_rdelta = v2_ldelta
			rot = ARROW_ROT[v2_rdelta]
			
			if v2_delta[0] == v2_ldelta[0] or v2_delta[1] == v2_ldelta[1]:
				texname = "arrow-ud"
			else:
				texname = "arrow-ur"
				
			if v2_t != v2_s:
				a_v2_path[v2_t] = (g_texnames.index(texname), rot)
			v2_t = (v2_t[0]+v2_delta[0], v2_t[1]+v2_delta[1])
		
		a_v2_path[v2_t] = (g_texnames.index("arrow-u"), ARROW_ROT[v2_delta])
		
		return a_v2_path
	def coord_in_bounds(self, v2_c):
		return v2_c[0] >= 0 and v2_c[1] >= 0 and v2_c[0] < self.map_width and v2_c[1] < self.map_height
	def get_range_list(self, v2_s, r):
		# TODO: include path to each cell.
		# (combine with get_path_tex)
		a_targ = [[] for i in range(r+1)]
		a_targ[0].append(v2_s)
		for i in range(1,r+1):
			for v2_tile in a_targ[i-1]:
				for v2_delta in TILE_ADJ:
					v2_coord = (v2_tile[0]+v2_delta[0], v2_tile[1]+v2_delta[1])
					if self.coord_in_bounds(v2_coord) and not self.loc_has_unit(v2_coord):
						for l in a_targ:
							if v2_coord in l:
								break
						else:
							a_targ[i].append(v2_coord)
		return a_targ
	def get_range_list_weighted(self, x, y, r):
		a_targ = []
		return a_targ
	def init_window(self):
		glutInit()											   # initialize glut
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(self.width, self.height)					   # set window size
		glutInitWindowPosition(0, 0)						   # set window position
		self.window = glutCreateWindow(b'Hello World!')			   # create window with title
		if FULLSCREEN: glutFullScreen()
	def init_callback(self):
		glutDisplayFunc(lambda: self.draw())					   # set draw function callback
		glutIdleFunc(lambda: self.draw())						   # draw all the time
		glutMouseFunc(lambda button, state, x, y: self.mouse(button, state, x, y))
		glutPassiveMotionFunc(lambda x, y: self.mouse_passive(x, y))
		glutKeyboardFunc(lambda key, x, y: self.keyboard(key, x, y))
		glutReshapeFunc(lambda w, h: self.reshape(w, h))
	def init_tex(self):
		texnames = [TEXDIR+s+TEXEXT for s in g_texnames]
		self.genTextures(texnames)
	def reshape(self, w, h):
		self.width = w
		self.height = h
	def mouse_passive(self, x, y):
		self.wmouseloc = (
			x / self.width,
			(self.height - y - 1) / self.height
		)
		self.mouseloc = (
			x * self.map_width // self.width,
			(self.height - y) * self.map_height // self.height
		)
		for t in self.tiles:
			if self.mouseloc == t.loc:
				self.tooltip.data = t.data
		self.tooltip.start()
	def mouse(self, button, state, x, y):
		# TODO: ADD HEX CLICK LOGIC.
		if TILE_TYPE == tile.RECT:
			rx = x * self.map_width // self.width
			ry = (self.height - y) * self.map_height // self.height
			ri = ry * self.map_width + rx
			if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
				for u in range(len(self.units)):
					if self.units[u].loc == (rx,ry):
						self.selected = u
						self.l2v_movereg=self.get_range_list(self.units[u].loc, self.units[u].moverange)
						break
				else:
					self.selected = None
					self.l2v_movereg = None
			if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
				if self.get_range(self.l2v_movereg, (rx, ry)) >= 0:
					for u in self.units:
						if u.loc == (rx,ry):
							break
					else:
						self.l2v_movereg = self.get_range_list((rx,ry), self.units[self.selected].moverange)
						self.units[self.selected].loc = (rx, ry)
	def keyboard(self, key, x, y):
		if key == b'\x1b':
			self.tooltip.stop()
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
	def get_tile_tex(self, t):
		for u in self.units:
			if u.loc == t.loc:
				return u.tex
		else:
			return t.tex
	def loc_has_unit(self, loc):
		for u in self.units:
			if loc == u.loc:
				return True
		return False
	def tile_has_unit(self, t):
		for u in self.units:
			if u.loc == t.loc:
				return True
		return False
	def draw(self):
		refresh2d(1, 1, self.width, self.height)										# set mode to 2d
		
		glClear(GL_COLOR_BUFFER_BIT)
		if USETEX: glEnable(GL_TEXTURE_2D)
		if USEFONT:
			glColor3f(1.0, 1.0, 1.0);
			font.draw("Hello World!", 0.5, 0.5)
		else:
			usepath=self.selected != None and self.mouseloc != None
			if usepath and USETEX:
				path = self.get_path_tex(self.units[self.selected].loc, self.mouseloc)
			
			for t in self.tiles:
				if USETEX:
					if usepath:
						try:
							tex = path[t.loc][0]
							glBindTexture(GL_TEXTURE_2D, self.textures[tex])
							rot = path[t.loc][1]
						except KeyError:
							tex = self.get_tile_tex(t)
							glBindTexture(GL_TEXTURE_2D, self.textures[tex])
							rot = 0
					else:
						tex = self.get_tile_tex(t)
						glBindTexture(GL_TEXTURE_2D, self.textures[tex])
						rot = 0
				else:
					rot = 0
				r = self.get_range(self.l2v_movereg[0], t.loc)
				
				if r == -1: # tile is not in range of selected unit
					# color the tile being hovered over blue
					if self.mouseloc != None and t.loc == self.mouseloc:
						c = color.d_color["BLUE"] * 0.5
					# color others grey
					else:
						c = color.d_color["WHITE"] * 0.5
				else:
					if self.mouseloc != None and t.loc == self.mouseloc:
						c = color.d_color["GREEN"] * 0.5
					elif self.tile_has_unit(t) and t.loc != self.targets[0][0]:
						c = color.d_color["WHITE"] * 0.5
					else:
						c = color.d_color["RED"]
						c.r = float(self.units[self.selected].moverange+1-r) / (self.units[self.selected].moverange+1)# 0->1 1->0.5 2->0.33
				c.draw()
				t.draw(self.size, rot)
		if self.tooltip.do_render and self.wmouseloc != None:
			# TODO: draw a textured rectangle behind the text
			#glBindTexture(GL_TEXTURE_2D, self.textures[g_texnames.index("bound")])
			glDisable(GL_TEXTURE_2D)
			glColor3f(1.0, 1.0, 1.0)
			s = "data: " + repr(self.tooltip.data)
			print(
				self.wmouseloc[0],
				self.wmouseloc[1] + 13.0 / self.height,
				8.0 * len(s) / self.width,
				-1.0 * 13 / self.height,
				self.size
			)
			tile.draw_rect(
				self.wmouseloc[0],
				self.wmouseloc[1] + 13.0 / self.height,
				8.0 * len(s) / self.width,
				-1.0 * 13 / self.height,
				self.size,
				True
			)
			glColor3f(0.0, 0.0, 0.0)
			font.draw(s, self.wmouseloc[0], self.wmouseloc[1])
		glDisable(GL_TEXTURE_2D)
		glutSwapBuffers()
		
# initialization

m = mygame()

glutMainLoop() # start everything