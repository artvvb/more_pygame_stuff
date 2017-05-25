import datetime
import font
import tile
from OpenGL.GL import *
class fps:
	def __init__(self):
		self.mytime = (datetime.datetime.now(),None)
	def update(self):
		self.mytime = (datetime.datetime.now(),self.mytime[0])
	def draw(self, position, window_size, size):
		delta = self.mytime[0]-self.mytime[1]
		rate = 1000000.0/delta.microseconds
		s = "freq: " + repr(rate)
		font.draw(s, position[0], position[1], True, window_size, size)