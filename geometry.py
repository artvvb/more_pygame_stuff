RECT = 4
HEX  = 6
TILETYPE = RECT
from coord import Coord
class GeometryComponent:
	def CoordinateToVertices(self, coord):
		return [coord+delta for delta in self.vertex_deltas]
	def CoordinateGetNeighbors(self, coord):
		return [coord+delta for delta in self.neighbor_deltas]
	# CoordinateList methods intended to implement batch processing and help reduce tearing from inexact floating point arithmetic
	def CoordinateListToVertices(self, L_coord):
		return [self.CoordinateToVertices(x) for x in L_coord] # TODO: minimize do-over processing
	def CoordinateListGetNeighbors(self, L_coord):
		return [self.CoordinateGetNeighbors(x) for x in L_coord]
		
class RectGeometryComponent(GeometryComponent):
	def __init__(self):
		self.neighbor_deltas = [(0,1),(1,0),(0,-1),(-1,0)]
		self.vertex_deltas = [(-0.5,-0.5),(-0.5,0.5),(0.5,0.5),(0.5,-0.5)]
	def PixelToCoordinate(self, pix, screen_size, screen_offset):
		return ( x / screen_size[0] - screen_offset[0] , y / screen_size[1] - screen_offset[1] )
	def NearestCoordinate(self, coord):
		return (round(coord[0]), round(coord[1]))
	def CoordinateToPixel(self, coord, screen_size, screen_offset):
		t = self.NearestCoordinate(coord)
		return (t[0] * screen_size[0] + screen_offset[0], t[1] * screen_size[1] + screen_offset[1])
		
class HexGeometryComponent(GeometryComponent):
	def __init__(self):
		# uses coord3's in cubic form
		self.neighbor_deltas = [(0,1,-1),(0,-1,1),(1,0,-1),(1,-1,0),(-1,0,1),(-1,1,0)]
		self.vertex_deltas = []
	def PixelToCoordinate(self, pix, screen_size, screen_offset):
		
		
		raise NotImplementedError()
	def CoordinateToPixel(self, coord, screen_size, screen_offset):
		x = 0.5 * sqrt(3) * (coord[0] + coord[1]/2)
		y = 0.75 * coord[1]
		return ( x / screen_size[0] - screen_offset[0] , y / screen_size[1] - screen_offset[1] )
	def NearestCoordinate(self, coord):
		
		raise NotImplementedError()

GEOMETRY_COMPONENTS = {
	RECT: RectGeometryComponent(),
	HEX:  HexGeometryComponent()
}


# TYPES OF COORD:
#  pixel: x,y = [0,screen_size.x),[0,screen_size.y) (int)
#  game:  x,y = [0,map_size.x),[0,map_size.y) (int)
#  gl:    x,y = [0.0,1.0],[0.0,1.0]