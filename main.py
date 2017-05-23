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
import coord
import pathfinding

window = 0		# glut window number

TILE_TYPE = tile.RECT
MAP_SIZE = coord.coord(10, 10)
WINDOW_SIZE = coord.coord(640, 480)
FULLSCREEN = False
USEFONT = False
USETEX = TILE_TYPE == tile.RECT
TEXDIR = "textures/"
TEXEXT = ".png"
RANDRANGE=(1,2)


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
	( 1, 0): 3
}

CORNER_ROT = {
	(-1, 0, 0, 1): 1,
	( 0, 1,-1, 0): 3,
	
	(-1, 0, 0,-1): 0,
	( 0,-1,-1, 0): 2,
	
	( 1, 0, 0,-1): 3,
	( 0,-1, 1, 0): 1,
	
	( 1, 0, 0, 1): 2,
	( 0, 1, 1, 0): 0
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
		
		self.window_size = WINDOW_SIZE
		self.map_size = MAP_SIZE
		self.size = (1.0 / self.map_size.x, 1.0 / self.map_size.y)
		self.selected = None
		
		self.tiles = []
		self.m_d_v2_tiles = {}
		for y in range(self.map_size.y):
			for x in range(self.map_size.x):
				ttex = g_texnames.index(g_TILETEX)#(x+y*self.map_size.x)%2
				tx = x if TILE_TYPE == tile.RECT else (x + (0.5 if y%2 == 0 else 0.0))
				ty = y
				tloc = (tx, ty)
				tweight = random.randint(RANDRANGE[0], RANDRANGE[1])
				self.tiles.append(tile.tile(tx, ty, ttex, TILE_TYPE, tweight))
				self.m_d_v2_tiles[tloc] = tile.tile(tx, ty, ttex, TILE_TYPE, tweight)
		self.init_window()
		self.init_callback()
		if USETEX: self.init_tex()
		self.units = [
			unit.unit((0,0), g_texnames.index("unit"), 2),# * sum(RANDRANGE)/2),
			unit.unit((4,6), g_texnames.index("unit"), 4),# * sum(RANDRANGE)/2),
			unit.unit((3,6), g_texnames.index("unit"), 1),# * sum(RANDRANGE)/2),
			unit.unit((3,5), g_texnames.index("unit"), 0),# * sum(RANDRANGE)/2)
		]
		self.selected = None
		self.mouseloc = None
		self.wmouseloc = None
		self.l_v2_movereg = None
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
	
	def deltas_to_tex(self, delta_src, delta_dst):
		if delta_src == delta_dst:
			rot = ARROW_ROT[delta_src]
		else:
			rot = CORNER_ROT[delta_src+delta_dst]
		if delta_dst[0] == delta_src[0] or delta_dst[1] == delta_src[1]:
			texname = "arrow-ud"
		else:
			texname = "arrow-ur"
			
		return (g_texnames.index(texname), rot)
	def get_path_tex(self, v2_s, v2_d, r):
		#def get_path(d_graph, src, max_weight, deltas):
		if v2_d == v2_s:
			return {}
		tiles = {}
		for t in self.tiles:
			if not self.loc_has_unit(t.loc):
				tiles[t.loc] = t.weight
		path = pathfinding.get_path(tiles, v2_s, r, TILE_ADJ)
		# path dict [coordinate tuple] : .src(delta), .weight
		if not v2_d in path or not v2_s in path:
			return {}
			
		v2_t = v2_d
		rdict = {v2_t:(g_texnames.index("arrow-u"), ARROW_ROT[path[v2_t].delta])}
		next_v2 = lambda loc, delta: (loc[0]-delta[0], loc[1]-delta[1])
		while next_v2(v2_t, path[v2_t].delta) != v2_s:
			nextdelta = path[next_v2(v2_t, path[v2_t].delta)].delta
			delta = path[v2_t].delta
			
			rdict[next_v2(v2_t, delta)] = self.deltas_to_tex(nextdelta, delta)
			v2_t = next_v2(v2_t, delta)
		return rdict
		
	def coord_in_bounds(self, v2_c):
		return v2_c[0] >= 0 and v2_c[1] >= 0 and v2_c[0] < self.map_size.x and v2_c[1] < self.map_size.y
	def get_range_list(self, v2_s, r):
		tiles = {}
		for t in self.tiles:
			if not self.loc_has_unit(t.loc):
				tiles[t.loc] = t.weight
		return [loc for loc in pathfinding.get_path(tiles, v2_s, r, TILE_ADJ)]
		"""
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
		"""
	def get_range_list_weighted(self, x, y, r):
		a_targ = []
		return a_targ
	def init_window(self):
		glutInit()											   # initialize glut
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(self.window_size.x, self.window_size.y)					   # set window size
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
		self.window_size.x = w
		self.window_size.y = h
	def mouse_passive(self, x, y):
		self.wmouseloc = (
			x / self.window_size.x,
			(self.window_size.y - y - 1) / self.window_size.y
		)
		self.mouseloc = (
			x * self.map_size.x // self.window_size.x,
			(self.window_size.y - y) * self.map_size.y // self.window_size.y
		)
		for loc in self.m_d_v2_tiles:
			if self.mouseloc == loc:
				self.tooltip.data = self.m_d_v2_tiles[loc].weight
		self.tooltip.start()
	def mouse(self, button, state, x, y):
		# TODO: ADD HEX CLICK LOGIC.
		if TILE_TYPE == tile.RECT:
			rx = x * self.map_size.x // self.window_size.x
			ry = (self.window_size.y - y) * self.map_size.y // self.window_size.y
			ri = ry * self.map_size.x + rx
			if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
				for u in range(len(self.units)):
					if self.units[u].loc == (rx,ry):
						self.selected = u
						self.l_v2_movereg=self.get_range_list(self.units[u].loc, self.units[u].moverange)
						break
				else:
					self.selected = None
					self.l_v2_movereg = None
			if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
				if self.l_v2_movereg != None and (rx, ry) in self.l_v2_movereg:
					for u in self.units:
						if u.loc == (rx,ry):
							break
					else:
						self.units[self.selected].loc = (rx, ry)
						self.l_v2_movereg = self.get_range_list((rx,ry), self.units[self.selected].moverange)
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
	def draw(self):
		refresh2d(1, 1, self.window_size.x, self.window_size.y)										# set mode to 2d
		
		glClear(GL_COLOR_BUFFER_BIT)
		if USETEX: glEnable(GL_TEXTURE_2D)
		if USEFONT:
			glColor3f(1.0, 1.0, 1.0);
			font.draw("Hello World!", 0.5, 0.5)
		else:
			usepath=self.selected != None and self.mouseloc != None
			if usepath and USETEX:
				path = self.get_path_tex(self.units[self.selected].loc, self.mouseloc, self.units[self.selected].moverange)
			
			for loc in self.m_d_v2_tiles:
				if USETEX:
					if usepath:
						try:
							tex = path[loc][0]
							glBindTexture(GL_TEXTURE_2D, self.textures[tex])
							rot = path[loc][1]
						except KeyError:
							tex = self.get_tile_tex(self.m_d_v2_tiles[loc])
							glBindTexture(GL_TEXTURE_2D, self.textures[tex])
							rot = 0
					else:
						tex = self.get_tile_tex(self.m_d_v2_tiles[loc])
						glBindTexture(GL_TEXTURE_2D, self.textures[tex])
						rot = 0
				else:
					rot = 0
				#r = self.get_range(self.l_v2_movereg, loc)
				
				if self.l_v2_movereg == None or not loc in self.l_v2_movereg: # tile is not in range of selected unit
					# color the tile being hovered over blue
					if self.mouseloc != None and loc == self.mouseloc:
						c = color.d_color["BLUE"] * 0.5
					# color others grey
					else:
						c = color.d_color["WHITE"] * ((self.m_d_v2_tiles[loc].weight + 1.0) / (RANDRANGE[1] + 2.0))
				else:
					if self.mouseloc != None and loc == self.mouseloc:
						c = color.d_color["GREEN"] * 0.5
					elif self.loc_has_unit(loc) and (self.selected == None or loc != self.units[self.selected].loc):
						c = color.d_color["WHITE"] * ((self.m_d_v2_tiles[loc].weight + 1.0) / (RANDRANGE[1] + 2.0))
					elif self.selected != None and loc == self.units[self.selected].loc:
						c = color.d_color["RED"]
					else:
						 # :[0:2]
						c = color.d_color["RED"] * ((self.m_d_v2_tiles[loc].weight + 1.0) / (RANDRANGE[1] + 2.0))
				c.draw()
				self.m_d_v2_tiles[loc].draw(self.size, rot)
		if self.tooltip.do_render and self.wmouseloc != None:
			glDisable(GL_TEXTURE_2D)
			glColor3f(1.0, 1.0, 1.0)
			s = "data: " + repr(self.tooltip.data)
			tile.draw_rect(
				self.wmouseloc[0],
				self.wmouseloc[1] + 15.0 / self.window_size.y,
				8.0 * len(s) / self.window_size.x,
				-1.0 * 15 / self.window_size.y,
				self.size,
				True
			)
			glColor3f(0.0, 0.0, 0.0)
			font.draw(s, self.wmouseloc[0], self.wmouseloc[1] + 3.0 / self.window_size.y)
		glDisable(GL_TEXTURE_2D)
		glutSwapBuffers()
		
# initialization

m = mygame()

glutMainLoop() # start everything