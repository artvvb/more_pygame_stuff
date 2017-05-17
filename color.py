from OpenGL.GL import glColor3f

class color:
	def __init__(self, r, g, b):
		self.r, self.g, self.b = r, g, b
	def draw(self):
		glColor3f(self.r, self.g, self.b)
	def __mul__(self, intensity):
		r = self.r * intensity if self.r * intensity <= 1.0 else 1.0
		g = self.g * intensity if self.g * intensity <= 1.0 else 1.0
		b = self.b * intensity if self.b * intensity <= 1.0 else 1.0
		return color(r, g, b)
		
d_color = {
	"RED":		color(1.0, 0.0, 0.0),
	"GREEN":	color(0.0, 1.0, 0.0),
	"BLUE":		color(0.0, 0.0, 1.0),
	"YELLOW":	color(1.0, 1.0, 0.0),
	"MAGENTA":	color(1.0, 0.0, 1.0),
	"TEAL":		color(0.0, 1.0, 1.0),
	"BLACK":	color(0.0, 0.0, 0.0),
	"WHITE":	color(1.0, 1.0, 1.0)
}
