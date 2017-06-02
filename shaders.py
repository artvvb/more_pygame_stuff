from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.GL.ARB.geometry_shader4 import *
from OpenGL.GL.EXT.geometry_shader4 import *

class shader(node) :
	def __init__(self, filename):
		node.__init__(self)
		self.filename = filename
		self.load()
  
	def load(self, debug=False):
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
			print self.source['vertex']
			print self.source['fragment']
			print self.source['geometry']
 
    

	def init(self):
		##compile and link shader
		self.vs = self.fs = self.gs = 0

		self.vs = glCreateShader(GL_VERTEX_SHADER)
		self.fs = glCreateShader(GL_FRAGMENT_SHADER)
		self.gs = glCreateShader(GL_GEOMETRY_SHADER_EXT)

		glShaderSource(self.vs, self.source['vertex'])
		glShaderSource(self.fs, self.source['fragment'])
		glShaderSource(self.gs, self.source['geometry'])

		glCompileShader(self.vs)
		log = glGetShaderInfoLog(self.vs)
		if log: print 'Vertex Shader: ', log

		glCompileShader(self.gs)
		log = glGetShaderInfoLog(self.gs)
		if log: print 'Geometry Shader: ', log

		glCompileShader(self.fs)
		log = glGetShaderInfoLog(self.fs)
		if log: print 'Fragment Shader: ', log

		self.prog = glCreateProgram()

		glAttachShader(self.prog, self.vs)
		glAttachShader(self.prog, self.fs)
		glAttachShader(self.prog, self.gs)

		glLinkProgram(self.prog)

		glUseProgram(self.prog)

		self.draw = self.use

	def use(self):
		glUseProgram(self.prog)
		uniform_location = glGetUniformLocation(self.prog, "time")
		glUniform1i(uniform_location, pygame.time.get_ticks())

	def end(self):
		glUseProgram(0)
		
