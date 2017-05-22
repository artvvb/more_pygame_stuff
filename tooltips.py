"""
Functionality:
tooltip_reset whenever mouse_passive_callback is called
	if movement:
		set tooltip_message to parameter
		set tooltip_render to false
		delete timer instance
		create new timer instance
when timer exceeds 1.0 sec
	set tooltip_render to true
"""

from threading import Timer
from threading import RLock
import font

class tooltip:
	def __init__(self, time_to_popup, data=None):
		self.time_to_popup = time_to_popup
		self.data = data
		self.lock = RLock()
		self.timer = Timer(self.time_to_popup, lambda: self.callback())
		self.running = False
		self.do_render = False
	def callback(self):
		with self.lock:
			if self.running:
				self.timer.cancel()
				self.running = False
			self.do_render = True
	def start(self):
		with self.lock:
			if self.running:
				self.timer.cancel()
				self.running = False
			del self.timer
			self.timer = Timer(self.time_to_popup, lambda: self.callback())
			self.timer.start()
			self.running = True
			self.do_render = False
				
	def stop(self):
		with self.lock:
			if self.running:
				self.timer.cancel()
				self.running = False