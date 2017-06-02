import random
import coord

class Map:
	def __init__(self, coordFactory, dataFactory):
		self.data = {}
		for coord in coordFactory.coords:
			self.data[coord] = dataFactory.value
	def __iter__(self):
		return iter(self.data)
	def next(self):
		return self.data.next()
	def __getitem__(self, i):
		return self.data[i]
	def __setitem__(self, i, v):
		self.data[i] = v
		return v
		
class CoordFactory:
	def __init__(self):
		pass
	@property
	def coords(self):
		pass

#class AxialCoordFactory:
		
class RectCoordFactory(CoordFactory):
	def __init__(self, map_size):
		self.map_size = map_size
	@property
	def coords(self):
		return ( coord.Coord(x=x,y=y) for x in range(self.map_size.x) for y in range(self.map_size.y) )
	
class DataFactory:
	def __init__(self):
		pass
	@property
	def data(self):
		pass
		
class RandDataFactory(DataFactory):
	def __init__(self, rand_range):
		self.rand_range=rand_range
	@property
	def value(self):
		return MapData(random.randint(self.rand_range[0], self.rand_range[1]))
	
class MapData:
	def __init__(self, weight):
		self.weight = weight