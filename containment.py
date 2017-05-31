def difference(a,b):
	return (a[0]-b[0],a[1]-b[1])
def dot_product(a,b):
	return a[0]*b[0]+a[1]*b[1]

class TriangleContainment:
	def __init__(self):
		return
	def triangle_contains(self, a, b, c, p):
		raise NotImplementedError()
	def triangle_contains_any(self, a, b, c, L_p):
		raise NotImplementedError()
	def triangle_contains_all(self, a, b, c, L_p):
		raise NotImplementedError()
	def any_triangles_contain(self, L_a, L_b, L_c, p):
		raise NotImplementedError()
	def all_triangles_contain(self, L_a, L_b, L_c, p):
		raise NotImplementedError()
	
class BarycenterMethod(TriangleContainment):
	def __init__(self):
		return
	def _set_triangle(self, a, b, c):
		self.a,self.b,self.c = a,b,c
		self.v0 = difference( self.c , self.a)
		self.v1 = difference( self.b , self.a)
		self.dot00 = dot_product( self.v0, self.v0 )
		self.dot01 = dot_product( self.v0, self.v1 )
		self.dot11 = dot_product( self.v1, self.v1 )
		self.invDenom = 1.0 / (self.dot00 * self.dot11 - self.dot01 * self.dot01)
	def _triangle_containment(self):
		self.v2 = difference( self.p, self.a )
		self.dot02 = dot_product( self.v0, self.v2 )
		self.dot12 = dot_product( self.v1, self.v2 )
		self.u = (self.dot11 * self.dot02 - self.dot01 * self.dot12) * self.invDenom
		self.v = (self.dot00 * self.dot12 - self.dot01 * self.dot02) * self.invDenom
		return (self.u >= 0) and (self.v >= 0) and (self.u + self.v < 1)
	def _set_point(self, p):
		self.p = p
	def triangle_contains(self, a, b, c, p):
		self._set_point( p )
		self._set_triangle( a, b, c )
		return self._triangle_containment()
	def triangle_contains_any(self, a, b, c, L_p):
		self._set_triangle( a, b, c )
		for p in L_p:
			self._set_point(p)
			if self._triangle_containment():
				return True
		return False
	def triangle_contains_all(self, a, b, c, L_p):
		self._set_triangle( a, b, c )
		for p in L_p:
			self._set_point(p)
			if not self._triangle_containment():
				return False
		return True
	def any_triangles_contain(self, L_a, L_b, L_c, p):
		self._set_point( p )
		for i in range(len(L_a)):
			self._set_triangle(L_a[i], L_b[i], L_c[i])
			if self._triangle_containment():
				return True
		return False
	def all_triangles_contain(self, L_a, L_b, L_c, p):
		self._set_point( p )
		for i in range(len(L_a)):
			self._set_triangle(L_a[i], L_b[i], L_c[i])
			if not self._triangle_containment():
				return False
		return True

class AreaMethod(TriangleContainment):
	def __init__(self):
		return
	def _compute_area(self, a, b, c):
		temp = (a[0]-c[0])*(b[1]-a[1])-(a[0]-b[0])*(c[1]-a[1])
		if temp < 0: temp *= -1
		return temp/2
	def triangle_contains(self, a, b, c, p):
		a0 = self._compute_area(a, b, c)
		a1 = self._compute_area(a, b, p)
		a2 = self._compute_area(a, p, c)
		a3 = self._compute_area(p, b, c)
		return a0 == a1+a2+a3


if __name__ == "__main__":
	print("Benchmarking Available TriangleContainment Components:")
	import datetime
	L_t = []
	L_r = []
	a,b,c = (-340,495),(-153,-910),(835,-947)
	x,y,z = (-175, 41),(-421,-714),(574,-645)
	p = (0,0)
	bary_comp = BarycenterMethod()
	area_comp = AreaMethod()
	L_t.append( datetime.datetime.now() )
	L_r.append( bary_comp.triangle_contains( a , b , c , p ) )
	L_r.append( bary_comp.triangle_contains( x , y , z , p ) )
	L_t.append( datetime.datetime.now() )
	L_r.append( area_comp.triangle_contains( a , b , c , p ) )
	L_r.append( area_comp.triangle_contains( x , y , z , p ) )
	L_t.append( datetime.datetime.now() )
	print((L_t[1]-L_t[0]).microseconds, (L_t[2]-L_t[1]).microseconds)
	print(L_r)
	
	
	#TODO: create a benchmark based on import random or project euler problem #102
		