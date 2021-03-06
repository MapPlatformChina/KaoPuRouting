#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is one of traffic map utility component files
# Created in 2013
# ######################################################################
import math

# Below is the area for class definition

# Below is for helper functions

# function to calculate distance between to coords
# distance returned is in KM
def coords_to_distance(coords_a, coords_b):
	lat_a = coords_a[1]
	lon_a = coords_a[0]
	lat_b = coords_b[1]
	lon_b = coords_b[0]
	
	c = math.sin(lat_a) * math.sin(lat_b) * math.cos(lon_a - lon_b) + math.cos(lat_a) * math.cos(lat_b)
	distance = 6371.004 * math.acos(c)*math.pi/180
	
	return distance

# function convert coords into pos (in pixel)
def geocoordinates_to_pixels(coords, zoom_level, image_size = 256):
	pic_size = 2 ** zoom_level * image_size
	x = coords[0] / 360.0 + 0.5						# convert longitude into pos x
	y = (coords[1] / 90.0 + 1) * math.pi / 4.0;		
	y = 1 - (math.log(math.tan(y)) / math.pi + 1) / 2.0		# convert Latitude into pos y
	return [round(x * pic_size), round(y * pic_size)]

# function convert pos (in pixel) into coords
def pixels_to_geocoordinates(pos, zoom_level, image_size=256):
	pic_size = 2 ** zoom_level * image_size
	longitude = (pos[0] / pic_size - 0.5) * 360.0
	latitude = math.pi * (1 - 2 * pos[1] / pic_size)
	latitude = math.atan(math.exp(latitude)) * 360 / math.pi - 90
	return [longitude,latitude]

# function that find out grid that the pixel locate
def pixels_to_grid(pos, zoom_level, image_size = 256):
	pic_size = 2 ** zoom_level * image_size
	col = int(math.floor(pos[0] / image_size))
	row = int(math.floor(pos[1] / image_size))
	return [col,row]

# function that find out grid that the coords locate
def geocoordinates_to_grid(coords, zoom_level, image_size = 256):
	pos = geocoordinates_to_pixels(coords, zoom_level, image_size)
	return pixels_to_grid(pos, zoom_level, image_size)

#def get_right_center_pixels(grid, image_size = 256):
#	right_x = (grid[0] + 1) * image_size
#	center_y = grid[1] * image_size + image_size / 2
#	return [right_x, center_y]

class PosCoordsUtl:
	def __init__(self, zoom_level, canvas_size, image_size = 256):
		self.canvas_size = canvas_size
		self.image_size = image_size
#		self.row = self.canvas_size[1]/ self.image_size
#		self.row = self.canvas_size[0] / self.image_size
		self.set_zoom_level(zoom_level)

	def set_zoom_level(self, zoom_level):
		self.zoom_level = zoom_level
		# compute the picture size
		self.pic_size = 2 ** self.zoom_level * self.image_size
		
#		self.row = self.canvas_size[1]/ self.image_size
#		self.row = self.canvas_size[0] / self.image_size
		
	
	def get_conner_grid(self, center_coords):
		center_pos = geocoordinates_to_pixels(center_coords, self.zoom_level, self.image_size)
		
		left_top_pos = [center_pos[0] - self.canvas_size[0]/2 , center_pos[1] - self.canvas_size[1]/2]
		left_top_grid = pixels_to_grid(left_top_pos, self.zoom_level, self.image_size)
		
		right_bottom_pos = [center_pos[0] + self.canvas_size[0]/2 , center_pos[1] + self.canvas_size[1]/2]
		right_bottom_grid = pixels_to_grid(right_bottom_pos, self.zoom_level, self.image_size)
		
		return (left_top_grid, right_bottom_grid)

	def coords_to_pos(self, coords):
		x = coords[0] / 360.0 + 0.5						# convert longitude into pos x
		y = (coords[1] / 90.0 + 1) * math.pi / 4.0;		
		y = 1 - (math.log(math.tan(y)) / math.pi + 1) / 2.0		# convert Latitude into pos y
		return [round(x * self.pic_size),round(y * self.pic_size)]


	# function convert pos (in pixel) into coords
	def pos_to_coords(self, pos):
		longitude = (pos[0] / self.pic_size - 0.5) * 360.0
		latitude = math.pi * (1 - 2 * pos[1] / self.pic_size)
		latitude = math.atan(math.exp(latitude)) * 360 / math.pi - 90
		return [longitude,latitude]

	# function that find out grid that the pixel locate
	def pos_to_grid(self, pos):
		col = int(math.floor(pos[0] / self.image_size))
		row = int(math.floor(pos[1] / self.image_size))
		return [col,row]

	# function that find out grid that the coords locate
	def coords_to_grid(self, coords):
		pos = self.coords_to_pos(coords)
		return self.pos_to_grid(pos)

	def get_shift(self, center_coords):
		pos = self.coords_to_pos(center_coords)
		left_top_pos = [ int(pos[0] - self.canvas_size[0]/2), int(pos[1] - self.canvas_size[1]/2)]
		return [left_top_pos[0] % self.image_size, left_top_pos[1] % self.image_size]

		
		
def get_conner_grid( center_coords, zoom_level, image_size = 256 ):
	pic_size = [2 ** zoom_level * image_size, 2 ** zoom_level * image_size]
	center_pos = geocoordinates_to_pixels(center_coords, zoom_level, image_size)
	left_top_pos = [center_pos[0] - 1024/2 , center_pos[1] - 768/2]
	right_bottom_pos = [center_pos[0] + 1024/2 , center_pos[1] + 768/2]
	left_top_grid = pixels_to_grid(left_top_pos, zoom_level, image_size)
	right_bottom_grid = pixels_to_grid(right_bottom_pos, zoom_level, image_size)
	return (left_top_grid, right_bottom_grid)
	
# unit test code

def main():

	# Here, your unit test code or main program

	# Check parameters
	# argc = len(sys.argv)
	# if argc <= 2:
	#	print_help()
	#	exit()

	coords = [ 116.54774, 39.76751 ]
	
	print coords
	
	pos = geocoordinates_to_pixels(coords,13)
	print pos
	
	print pixels_to_grid(pos, 13)
	
	coords = pixels_to_geocoordinates(pos,13)
	print coords
	
	coords_a = [ 116.3580358, 39.9867797 ]
	coords_b = [ 116.3586259, 39.9869299 ]
	dis = coords_to_distance(coords_a,coords_b)
	print 'Below result should be about: 0.052 KM'
	print 'Disance:',coords_a, '-', coords_b, ':', dis , 'KM'
			
if __name__=='__main__':
	main()