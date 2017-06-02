from OpenGL.GL import *

import geometry

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

def draw_rect(x, y, dx, dy, size, usetex, rotation=0):
	glBegin(GL_QUADS)
	#coord = geometry.
	#vertices = geometry.GEOMETRY_COMPONENTS[geometry.TILETYPE].
	
	for i in range(4):
		ti = (i + rotation) % 4
		glTexCoord2f(tiledata[0][ti][0], tiledata[0][ti][1])
		glVertex2f(x + tiledata[0][i][0] * dx, y + tiledata[0][i][1] * dy)
	glEnd()

def draw_square(center, map_size, texcoords, rotation=0):
	glBegin(GL_QUADS)
	for i in range(4):
		#ti = (i + rotation) % 4
		glTexCoord2f(
			texcoords[i][0],
			texcoords[i][1]
		)
		glVertex2f(
			(center.x + tiledata[0][i][0]) * map_size.x,
			(center.y + tiledata[0][i][1]) * map_size.y
		)
	glEnd()
	