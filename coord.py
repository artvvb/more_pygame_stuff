class Coord:
	def __init__(self, **kargs):
		self.x = kargs["x"]
		self.y = kargs["y"]
	def __add__(self, other):
		return Coord(x=self.x+other.x,y=self.y+other.y)
	def __iadd__(self, other):
		self.x += other.x
		self.y += other.y
		return self
	def __sub__(self, other):
		return Coord(x=self.x-other.x,y=self.y-other.y)
	def __isub__(self, other):
		self.x -= other.x
		self.y -= other.y
		return self
	def __mul__(self, other):
		if type(other) is Coord:
			return Coord(x=self.x*other.x,y=self.y*other.y)
		else:
			return Coord(x=self.x*other,y=self.y*other)
	def __imul__(self, other):
		if type(other) is Coord:
			self.x *= other.x
			self.y *= other.y
		else:
			self.x *= other
			self.y *= other
		return self
	def __round__(self):
		return Coord(x=round(self.x),y=round(self.y))
	def __repr__(self):
		return "(%s,%s)"%(repr(self.x),repr(self.y))
	def __eq__(self, other):
		if type(other) is type(None):
			return False
		return self.x == other.x and self.y == other.y
	def __ne__(self, other):
		if type(other) is type(None):
			return False
		return self.x != other.x or self.y != other.y
	def __hash__(self):
		return hash((self.x, self.y))
	def __truediv__(self, other):
		if type(other) is Coord:
			return Coord(x=self.x/other.x,y=self.y/other.y)
		else:
			return Coord(x=self.x/other,y=self.y/other)
	def __itruediv__(self, other):
		if type(other) is Coord:
			self.x /= other.x
			self.y /= other.y
		else:
			self.x /= other
			self.y /= other
		return self