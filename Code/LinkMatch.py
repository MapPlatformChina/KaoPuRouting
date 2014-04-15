#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

# Below is the area for class definition
import math
from RoadNetworkV2 import *
from PosCoordsUtl import *

MAX_DIS = 100**2 + 100**2

class LinkMatch:

	def __init__(self):
		# { grid: [[direction_sign, (longitude,latitude) , LCD, direction] ...] }
		# grid is in format of GRID_GRID, zoom level 
		self.link_match_table = {}
		self.zoom_level_of_grids = 15

		self.load()
	
	def load(self):
		file_name = '../Res/LinkMatch.dict'
		
		file_stream = open(file_name,'r')
		for line in file_stream:
			direction_sign, longitude_str, latitude_str, link_name = line.split(';')
			longitude = float(longitude_str)
			latitude = float(latitude_str)
			if link_name[-1] == '\n':
				link_name = link_name[0:-1]
			LCD = link_name[0:-2]
			direction = int(link_name[-1:])
			
			# PosCoordsUtl is longitude first
			grid = geocoordinates_to_grid((longitude,latitude), self.zoom_level_of_grids)
			
			key = ('%d_%d' % (grid[0],grid[1]))
			if not self.link_match_table.has_key(key):
				self.link_match_table[key] = [];
			self.link_match_table[key].append([direction_sign, [longitude,latitude], LCD, direction])
			
		file_stream.close()
		
		
		
	# para of geo_a/b should be in the format of longitude/latitude
	# if it is revered, please set reverse_lon_lat flag to True
	def match(self,geo_a, geo_b, reverse_lon_lat = False):
		if reverse_lon_lat:
			geo_from = [geo_a[1],geo_a[0]]
			geo_to = [geo_b[1],geo_b[0]]
		else:
			geo_from = geo_a
			geo_to = geo_b
		
		direction_sign = get_direction_sign_with_geo(geo_from, geo_to)
		
		geo_to_be_matched = [(geo_from[0] + geo_to[0]) / 2, (geo_from[1] + geo_to[1]) / 2]
		#geo = geo_b
		
		grid = geocoordinates_to_grid(geo_to_be_matched, self.zoom_level_of_grids)
		
		grid_start = grid
		grid_end = grid
		min_dis = MAX_DIS
		link_matched = ['?','?']
		MAX_LEVEL_OF_OUT_SEARCH = 5
		level_of_out_search = 0
		
		while True:
			grid_start = [grid_start[0] - 1, grid_start[1] - 1]
			grid_end = [grid_end[0] + 1, grid_end[1] + 1]
			for index_grid_x in range(grid_start[0],grid_end[0] + 1):
				for index_grid_y in range(grid_start[1],grid_end[1] + 1):
					key = ('%d_%d' % (index_grid_x,index_grid_y))
					if not self.link_match_table.has_key(key):
						continue
					for value in self.link_match_table[key]:
						if direction_sign == value[0]:		# direction must match
							geo = value[1]
							# calculate distance with latitude zoomed
							dis = (geo_to_be_matched[0] - geo[0]) **2 + ((geo_to_be_matched[1] - geo[1])*2)**2 
							if dis < min_dis:
								link_matched[0] = value[2]
								link_matched[1] = value[3]
								min_dis = dis
			if min_dis < MAX_DIS:
				return link_matched
			if level_of_out_search > MAX_LEVEL_OF_OUT_SEARCH:
				return link_matched
			level_of_out_search += 1

def main():

	# Here, your unit test code or main program

	# point of HPL
	geo_a = [39.9515592744,116.41934259]
	geo_b = [39.9505592744,116.41934259]
	reverse_flag = True
	expected_result = '155_0'
	
	print 'from:',geo_a,'to:', geo_b
	print 'result should be:', expected_result
	lm = LinkMatch()
	result = lm.match(geo_a,geo_b, reverse_flag)
	
	print 'result is:', result

	
if __name__=='__main__':
	main()