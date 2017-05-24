from OpenGL.GLUT import *
from OpenGL.GL import *
import numpy

def init_window():
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	glutInitWindowSize(640, 480)
	glutInitWindowPosition(0, 0)
	return glutCreateWindow(b'Hello World!')
	
window = init_window()
glViewport			(0, 0, 800, 600)
glClearColor 		(0.0, 0.0, 0.0, 0.0)
glEnableClientState	(GL_VERTEX_ARRAY)

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
	
	
g_texnames = ["bound"]
	
class grid:
	def __init__(self, size, tiledata, dimensions):
		self.v_per_t = len(tiledata)
		self.dimensions = dimensions
		self.size = size
		
		f_ind = lambda sel, a, b: (a%b if sel==0 else a//b)
		
		self.vertices = numpy.array(
			[
				( tiledata[ (i//dimensions)%self.v_per_t ][ i%dimensions ] *
					f_ind(i%self.dimensions, i, self.v_per_t * self.dimensions)
				) / ( size[i%2] )
				for i in range(size[1] * size[0] * self.v_per_t * self.dimensions)
			], dtype='float32'
		)
		self.vbo = glGenBuffers (1)
		glBindBuffer (GL_ARRAY_BUFFER, self.vbo)
		glBufferData (GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)
	def draw(self):
		refresh2d(1,1,640,480)
		glBindBuffer	(GL_ARRAY_BUFFER, self.vbo)
		glVertexPointer (self.dimensions, GL_FLOAT, 0, None)
		glColor3f		(1.0, 1.0, 1.0)
		glDrawArrays	(GL_QUADS, 0, self.size[1]*self.size[0]*self.dimensions*self.v_per_t)
		glutSwapBuffers ()

DIMENSIONS=2
TILEDATA=[
	(0.0,0.0),
	(0.0,1.0),
	(1.0,1.0),
	(1.0,0.0)
]
SIZE=(100,100)
mygrid = grid(SIZE, TILEDATA, DIMENSIONS)

glutDisplayFunc(lambda: mygrid.draw())
glutIdleFunc(lambda: mygrid.draw())
glutMainLoop()