from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
from ctypes import pointer

DEBUG_SHADER = False
USE_GEOMETRY = False

g_shader_params = {
	"vert": GL_VERTEX_SHADER,
	"frag": GL_FRAGMENT_SHADER,
	"geom": GL_GEOMETRY_SHADER
}
g_shader_filenames = {
	"vert": "shader.vert",
	"frag": "shader.frag"
}

class Shader:
	def __init__(self, filenames):
		self.source = {}
		self.prog = glCreateProgram()
		for key in filenames:
			if key in g_shader_params:
				fh = open(filenames[key])
				self.source[key] = glCreateShader(g_shader_params[key])
				string = fh.read()
				glShaderSource(self.source[key], string)
				fh.close()
				glCompileShader(self.source[key])
				glAttachShader(self.prog, self.source[key])
		glLinkProgram(self.prog)
		self.inuse = False
	def use(self):
		self.inuse = True
		glUseProgram(self.prog)
	def end(self):
		self.inuse = False
		glUseProgram(0)
	def setScale(self, scale):
		loc = glGetUniformLocation(self.prog, "scale")
		if (loc != -1):
		   glUniform2f(loc, scale[0], scale[1])
	def setOffset(self, offset):
		loc = glGetUniformLocation(self.prog, "offset")
		if (loc != -1):
		   glUniform2f(loc, offset[0], offset[1])
	
class Coord:
	def __init__(self, x, y):
		self.x, self.y = x, y
	def __add__(self, other):
		return Coord(self.x+other.x, self.y+other.y)

class Map:
	def __init__(self, nX, nY):
		self.nX, self.nY = nX, nY
		self.data = {}
		for y in range(nY):
			for x in range(nX):
				self.data[(x,y)] = Coord(x,y)
	def make_vbos(self):
		L = [[],[]]
		D = [
			[ Coord(0,0), Coord(1,0), Coord(0,1) ],
			[ Coord(1,0), Coord(0,1), Coord(1,1) ]
		]
		for c in self.data:
			for x in range(2):
				for d in D[x]:
					e = self.data[c] + d
					print(e.x,e.y)
					L[x].append(e.x)
					L[x].append(e.y)
				print()
		return [arrays.vbo.VBO(numpy.array(l, dtype=numpy.float32)) for l in L]
class App:
	def __init__(self, filenames):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(640, 480)
		glutInitWindowPosition(0, 0)
		self.window = glutCreateWindow(b'Hello World!')
		glutDisplayFunc(lambda: self.draw())
		glutIdleFunc(lambda: self.draw())
		glutKeyboardFunc(lambda key, x, y: self.keyboard(key, x, y))
		self.shader = Shader(filenames)
		nX , nY = 2 , 2
		fX , fY = nX / 2.0 , nY / 2.0
		self.scale = (1.0/fX,1.0/fY)
		self.offset = (-1.0*fX,-1.0*fY)
		
		self.triangles = [
			
		]
		
		#self.triangles = [
		#[	[0,0],[0,1],[1,0],
		#	[0,1],[0,2],[1,1],
		#	[1,0],[1,1],[2,0]
		#],[	[0,1],[1,0],[1,1],
		#	[0,2],[1,1],[1,2],
		#	[1,1],[2,0],[2,1]
		#]]
		self.colors = ((1,0,0),(0,1,0))
		self.vbos = Map(nX,nY).make_vbos()#[arrays.vbo.VBO(numpy.array(x, dtype=numpy.float32)) for x in self.triangles]
		
	def draw(self):
		glClearColor(0,0,0,0)
		glClear(GL_COLOR_BUFFER_BIT)
		glLoadIdentity()
		
		self.shader.use()
		self.shader.setScale(self.scale)
		self.shader.setOffset(self.offset)
		glEnableClientState(GL_VERTEX_ARRAY)
		
		#self.vbo.bind()
		#glVertexPointer(2, GL_FLOAT, 0, None)
		#glDrawArrays(GL_TRIANGLES, 0, 9)
		#self.vbo.unbind()
		for x in range(len(self.vbos)):
			glColor3f(self.colors[x][0],self.colors[x][1],self.colors[x][2])
			self.vbos[x].bind()
			glVertexPointer(2, GL_FLOAT, 0, None)
			glDrawArrays(GL_TRIANGLES, 0, 12)
			self.vbos[x].unbind()
		glDisableClientState(GL_VERTEX_ARRAY)
		self.shader.end()
		
		glutSwapBuffers()
		
	def keyboard(self, key, x, y):
		if key == b'\x1b':
			#self.vbo.delete()
			for x in self.vbos: x.delete()
			exit()
		
if __name__ == "__main__":
	myapp = App(g_shader_filenames)
	glutMainLoop()