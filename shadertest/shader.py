from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
DEBUG_SHADER = False
class Shader:
	def __init__(self, filename):
		self.filename = filename
		self.load()
	def load(self, debug=DEBUG_SHADER):
		fh = open(self.filename)  
		self.source = {'vertex': '', 'fragment':'', 'geometry':''}
		write = None
		for line in fh :
			if line == '[[vertex-program]]\n' : 
				write = 'vertex'
			elif line == '[[fragment-program]]\n' : 
				write = 'fragment'
			elif line == '[[geometry-program]]\n' : 
				write = 'geometry'
			else :
				self.source[write] += line
    
		self.draw = self.init
		if debug :
			print(self.source['vertex'])
			print(self.source['fragment'])
			print(self.source['geometry'])

	def init(self):
		##compile and link shader
		self.vs = self.fs = self.gs = 0

		self.vs = glCreateShader(GL_VERTEX_SHADER)
		self.fs = glCreateShader(GL_FRAGMENT_SHADER)
		#self.gs = glCreateShader(GL_GEOMETRY_SHADER_EXT)

		glShaderSource(self.vs, self.source['vertex'])
		glShaderSource(self.fs, self.source['fragment'])
		#glShaderSource(self.gs, self.source['geometry'])

		glCompileShader(self.vs)
		log = glGetShaderInfoLog(self.vs)
		if log: print('Vertex Shader: ', log)

		#glCompileShader(self.gs)
		#log = glGetShaderInfoLog(self.gs)
		#if log: print('Geometry Shader: ', log)

		glCompileShader(self.fs)
		log = glGetShaderInfoLog(self.fs)
		if log: print('Fragment Shader: ', log)

		self.prog = glCreateProgram()

		glAttachShader(self.prog, self.vs)
		glAttachShader(self.prog, self.fs)
		#glAttachShader(self.prog, self.gs)

		glLinkProgram(self.prog)

		glUseProgram(self.prog)

		self.draw = self.use

	def use(self):
		glUseProgram(self.prog)
	def end(self):
		glUseProgram(0)

class App:
	def __init__(self, filename):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(640, 480)
		glutInitWindowPosition(0, 0)
		self.window = glutCreateWindow(b'Hello World!')
		glutDisplayFunc(lambda: self.draw())
		glutIdleFunc(lambda: self.draw())
		glutKeyboardFunc(lambda key, x, y: self.keyboard(key, x, y))
		self.shader = Shader(filename)
		self.shader.init()
		
		self.triangles = [ [0.0,0.0],[0.25,0.5],[0.5,0.0] , [0.25,0.5],[0.75,0.5],[0.5,1.0] , [0.5,0.0],[1.0,0.0],[0.75,0.5] ]
		self.vbo = arrays.vbo.VBO(numpy.array(self.triangles, dtype=numpy.float32))#[0.0,0.0,0.5,0.0,0.25,0.5,0.25,0.5,0.75,0.5,0.5,1.0,0.5,0.0,1.0,0.0,0.75,0.5]))
	def draw(self):
		glViewport(0, 0, 640, 480)
		glClearColor(0, 0, 0, 0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
		glMatrixMode (GL_MODELVIEW)
		glLoadIdentity()
		
		glBegin(GL_QUADS)
		glVertex2f(0.25, 0.25)
		glVertex2f(0.25, 0.75)
		glVertex2f(0.75, 0.75)
		glVertex2f(0.75, 0.25)
		glEnd()
		
		self.shader.use()
		
		glEnableClientState(GL_VERTEX_ARRAY)
		self.vbo.bind()
		glVertexPointer(2, GL_FLOAT, 0, None)
		glDrawArrays(GL_TRIANGLES, 0, 9)
		self.vbo.unbind()
		glDisableClientState(GL_VERTEX_ARRAY)
		
		self.shader.end()
		
		glutSwapBuffers()
	def keyboard(self, key, x, y):
		if key == b'\x1b':
			exit()
		
if __name__ == "__main__":
	myapp = App("shader.glsl")
	glutMainLoop()