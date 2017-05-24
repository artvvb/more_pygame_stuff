from OpenGL.GL import *
from PIL import Image
import numpy
import tile

ATLAS_NAME="textures/atlas.png"
ATLAS_POSITIONS = {
	"bound": 	(0,0),
	"arrow-ud":	(1,0),
	"unit": 	(2,0),
	"arrow-ur":	(0,1),
	"arrow-u":	(1,1)
}
ATLAS_SIZE = (3,2)
BASE_TEXCOORDS = [(cx, 1.0 - cy) for cx, cy in tile.tiledata[tile.RECT]]
g_texture = None
def init():
	global g_texture
	g_texture = glGenTextures(1)
	
	img = Image.open(ATLAS_NAME)
	img_data = numpy.array(list(img.getdata()), numpy.uint8)

	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glBindTexture(GL_TEXTURE_2D, g_texture)

	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
	
def get_texcoords(key, rotation):
	position = ATLAS_POSITIONS[key]
	texcoords = [((position[0]+c[0]) / ATLAS_SIZE[0], (position[1]+c[1]) / ATLAS_SIZE[1]) for c in BASE_TEXCOORDS]
	return [texcoords[(i+rotation) % len(texcoords)] for i in range(len(texcoords))]