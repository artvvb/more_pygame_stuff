from OpenGL.GL import *

tiledata = [
	[
		( 0.0, 0.0 ),
		( 0.0, 1.0 ),
		( 1.0, 1.0 ),
		( 1.0, 0.0 )
	],
	[
		( 0.43, 0.00 ),
		( 0.86, 0.25 ),
		( 0.86, 0.75 ),
		( 0.43, 1.00 ),
		( 0.00, 0.75 ),
		( 0.00, 0.25 )
	]
]

RECT = 0
HEX = 1

class tile:
	def __init__(self, x, y, rgb, tex, tiletype):
		self.rgb, self.tex, self.tiletype = rgb, tex, tiletype
		self.loc = (x, y)
		self.coords = [(x + cx, y + cy) for cx, cy in tiledata[tiletype]]
		self.texcoords = [(cx, 1.0 - cy) for cx, cy in tiledata[tiletype]]
	def draw(self, size, rotation):
		glBegin(GL_QUADS if self.tiletype == "RECT" else GL_POLYGON)
		for i in range(len(self.coords)):
			ti = (i + rotation) % len(self.texcoords)
			glTexCoord2f(self.texcoords[ti][0], self.texcoords[ti][1])
			glVertex2f(self.coords[i][0] * size[0], self.coords[i][1] * size[1])
		glEnd()
