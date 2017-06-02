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
import tex
import fps
import geometry
import map


# TODO: next step, implement turn structure.

window = 0		# glut window number

TILE_TYPE = tile.RECT
MAP_SIZE = coord.Coord(x=10, y=10)
WINDOW_SIZE = coord.Coord(x=640, y=480)
FULLSCREEN = False
USEFONT = False
TEXDIR = "textures/"
TEXEXT = ".png"
RANDRANGE=(1,3)
SHOWFPS=True


TILE_ADJ = [
	coord.Coord(x=-1,y= 0),
	coord.Coord(x= 0,y=-1),
	coord.Coord(x= 1,y= 0),
	coord.Coord(x= 0,y= 1)
]

ARROW_ROT = {
	TILE_ADJ[3]: 0,
	TILE_ADJ[0]: 1,
	TILE_ADJ[1]: 2,
	TILE_ADJ[2]: 3
}

CORNER_ROT = {
	(TILE_ADJ[0],TILE_ADJ[3]): 1,
	(TILE_ADJ[3],TILE_ADJ[0]): 3,
	(TILE_ADJ[0],TILE_ADJ[1]): 0,
	(TILE_ADJ[1],TILE_ADJ[0]): 2,
	(TILE_ADJ[2],TILE_ADJ[1]): 3,
	(TILE_ADJ[1],TILE_ADJ[2]): 1,
	(TILE_ADJ[2],TILE_ADJ[3]): 2,
	(TILE_ADJ[3],TILE_ADJ[2]): 0
}

g_texnames = [key for key in tex.ATLAS_POSITIONS]

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
		self.size = coord.Coord(x = 1.0 / self.map_size.x, y = 1.0 / self.map_size.y)
		
		#self.tiles = {}
		#for y in range(self.map_size.y):
		#	for x in range(self.map_size.x):
		#		ttex = 0
		#		tx = x if TILE_TYPE == tile.RECT else (x + (0.5 if y%2 == 0 else 0.0))
		#		ty = y
		#		tloc = coord.Coord(x=tx, y=ty)
		#		tweight = random.randint(RANDRANGE[0], RANDRANGE[1])
		#		#self.tiles.append(tile.tile(tx, ty, ttex, TILE_TYPE, tweight))
		#		self.tiles[tloc] = tile.tile(tx, ty, ttex, TILE_TYPE, tweight)
				
		coordFactory = map.RectCoordFactory(MAP_SIZE)
		dataFactory = map.RandDataFactory(RANDRANGE)
		self.map = map.Map(coordFactory, dataFactory)
		
		self.init_window()
		self.init_callback()
		tex.init()
		self.units = {
			coord.Coord(x=0,y=0): unit.unit(coord.Coord(x=0,y=0), g_texnames.index("unit"), 2),# * sum(RANDRANGE)/2),
			coord.Coord(x=4,y=6): unit.unit(coord.Coord(x=4,y=6), g_texnames.index("unit"), 4),# * sum(RANDRANGE)/2),
			coord.Coord(x=3,y=6): unit.unit(coord.Coord(x=3,y=6), g_texnames.index("unit"), 1),# * sum(RANDRANGE)/2),
			coord.Coord(x=3,y=5): unit.unit(coord.Coord(x=3,y=5), g_texnames.index("unit"), 0),# * sum(RANDRANGE)/2)
		}
		self.selected = None
		self.mouseloc = None
		self.wmouseloc = None
		self.tooltip = tooltips.tooltip(1.0)
		self.tooltip.start()
		self.path = None
		self.pathtex = None
		self.myfps = fps.fps()
	def init_window(self):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(self.window_size.x, self.window_size.y)
		glutInitWindowPosition(0, 0)
		self.window = glutCreateWindow(b'Hello World!')
		if FULLSCREEN: glutFullScreen()
	def init_callback(self):
		glutDisplayFunc(lambda: self.draw())
		glutIdleFunc(lambda: self.draw())
		glutMouseFunc(lambda button, state, x, y: self.mouse(button, state, x, y))
		glutPassiveMotionFunc(lambda x, y: self.mouse_passive(x, y))
		glutKeyboardFunc(lambda key, x, y: self.keyboard(key, x, y))
		glutReshapeFunc(lambda w, h: self.reshape(w, h))
	
	def deltas_to_tex(self, delta_src, delta_dst):
		if delta_src == delta_dst:
			rot = ARROW_ROT[delta_src]
		else:
			rot = CORNER_ROT[(delta_src,delta_dst)]
		if delta_dst.x == delta_src.x or delta_dst.y == delta_src.y:
			texname = "arrow-ud"
		else:
			texname = "arrow-ur"
			
		return (g_texnames.index(texname), rot)
	def get_path_tex(self, v2_s, v2_d):
		if v2_d == v2_s or not v2_d in self.path or not v2_s in self.path:
			return {}
			
		v2_t = v2_d
		rdict = {v2_t:(g_texnames.index("arrow-u"), ARROW_ROT[self.path[v2_t].delta])}
		
		while v2_t - self.path[v2_t].delta != v2_s:
			nextdelta = self.path[v2_t - self.path[v2_t].delta].delta
			delta = self.path[v2_t].delta
			
			rdict[v2_t - delta] = self.deltas_to_tex(nextdelta, delta)
			v2_t = v2_t - delta
		return rdict
		
	def coord_in_bounds(self, v2_c):
		return v2_c[0] >= 0 and v2_c[1] >= 0 and v2_c[0] < self.map_size.x and v2_c[1] < self.map_size.y
		
	def reshape(self, w, h):
		self.window_size.x = w
		self.window_size.y = h
		
	def mouse_passive(self, x, y):
		self.wmouseloc = coord.Coord(x=x,y=y)
		self.wmouseloc *= coord.Coord(x=1.0,y=-1.0)
		self.wmouseloc += coord.Coord(x=0,y=self.window_size.y-1)
		self.wmouseloc /= self.window_size
		
		nx = x * self.map_size.x // self.window_size.x
		ny = (self.window_size.y - y) * self.map_size.y // self.window_size.y
		
		self.mouseloc = coord.Coord(x=nx,y=ny)
		
		self.update_path()
		
		#if self.mouseloc in self.tiles:
			#self.tooltip.data = self.tiles[self.mouseloc].weight
			#self.tooltip.start()
		if self.mouseloc in self.map:
			self.tooltip.data = self.map[self.mouseloc].weight
			self.tooltip.start()
	def mouse(self, button, state, x, y):
		# TODO: ADD HEX CLICK LOGIC.
		if TILE_TYPE != tile.RECT: return
		rx = x * self.map_size.x // self.window_size.x
		ry = (self.window_size.y - y) * self.map_size.y // self.window_size.y
		ri = ry * self.map_size.x + rx
		if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
			if coord.Coord(x=rx,y=ry) in self.units:
				self.selected = coord.Coord(x=rx,y=ry)
			else:
				self.selected = None
		elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
			c = coord.Coord(x=rx,y=ry)
			if self.path != None and c in self.path and not c in self.units:
				self.units[c] = self.units[self.selected]
				self.units.pop(self.selected, None)
				self.selected = c
				self.units[self.selected].loc = self.selected
		self.update_path()
	def update_path(self):
		tiles = {}
		for loc in self.map:
			if not loc in self.units:
				#tiles[loc] = self.tiles[loc]
				tiles[loc] = self.map[loc]
		self.path = None if self.selected == None else pathfinding.get_path(tiles, self.selected, self.units[self.selected].moverange, TILE_ADJ)
		self.pathtex = None if self.selected == None or self.mouseloc == None else self.get_path_tex(self.selected, self.mouseloc)
	def keyboard(self, key, x, y):
		if key == b'\x1b':
			self.tooltip.stop()
			exit()
	
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
		return loc in self.units
	def draw(self):
		refresh2d(1, 1, self.window_size.x, self.window_size.y)										# set mode to 2d
		
		#glClear(GL_COLOR_BUFFER_BIT)
		glEnable(GL_TEXTURE_2D)
	
		glBindTexture(GL_TEXTURE_2D, tex.g_texture)
		for loc in self.map:
			stex = "unit" if loc in self.units else "bound"
			rot = 0
			
			if self.path == None or not loc in self.path: # tile is not in range of selected unit
				if self.mouseloc != None and loc == self.mouseloc:
					c = color.d_color["BLUE"]
				else:
					c = color.d_color["WHITE"]
			elif self.loc_has_unit(loc) and (self.selected == None or loc != self.selected):
				c = color.d_color["WHITE"]
			else:
				c = color.d_color["RED"]
			weightmult = ((self.map[loc].weight - RANDRANGE[0] + 1.0) / (RANDRANGE[1] - RANDRANGE[0] + 1.0))
			#weightmult for an appropriate RANDRANGE should be [W+1/dR+1 for W] -> [1/2,2/2] for dR=1
			c = c * weightmult
			c.draw()
			tile.draw_tile(loc, self.size, tex.get_texcoords(stex, rot), rot)
			if self.pathtex and loc in self.pathtex:
				itex, rot = self.pathtex[loc]
				(color.d_color["WHITE"]*0.5).draw()
				tile.draw_tile(loc, self.size, tex.get_texcoords(g_texnames[itex], rot), rot)
		glDisable(GL_TEXTURE_2D)
		if self.tooltip.do_render and self.wmouseloc != None:
			s = "data: " + repr(self.tooltip.data)
			font.draw(s, self.wmouseloc[0], self.wmouseloc[1] + 3.0 / self.window_size.y, True, self.window_size, self.size)
		if SHOWFPS:
			self.myfps.update()
			self.myfps.draw((0.0,0.0), self.window_size, self.size)
		glutSwapBuffers()
		
# initialization
geometry.TILETYPE = geometry.RECT
m = mygame()

glutMainLoop() # start everything