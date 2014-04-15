#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is to help structuring a good program
# Created in 2013
# ######################################################################

# Below is the area for class definition
import sys
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
		print 'Start to load matching table...',
		sys.stdout.flush()
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
		print 'Done!'
		sys.stdout.flush()
		
		
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
	
	print 'Load dictionary ...',
	sys.stdout.flush()
	lm = LinkMatch()
	print 'Done!'
	sys.stdout.flush()

	print 'from:',geo_a,'to:', geo_b
	print 'result should be:', expected_result
	result = lm.match(geo_a,geo_b, reverse_flag)
	
	print 'result is:', result
	
	path_a = [39.9515573,116.4195518,39.9510098,116.4195442,39.950881,116.4195549,39.9508703,116.4195764,39.9508917,116.4213252,39.9509132,116.4223123,39.9503446,116.4223123,39.9502909,116.4223123,39.9502051,116.4223123,39.9502265,116.4229453,39.9502587,116.4238572,39.9502695,116.4242542,39.9503446,116.4251876,39.9503446,116.4252841,39.9502695,116.4252949,39.9499583,116.4252949,39.9497652,116.4253056,39.9494112,116.42537,39.9494541,116.4268291,39.9494863,116.4279878,39.9495399,116.4280951,39.9495614,116.4281809,39.9495828,116.4297259,39.9496043,116.4297795,39.949615,116.4299834,39.949615,116.4307451,39.9495828,116.4310563,39.9494863,116.431582,39.9491644,116.4325905,39.9491322,116.4328587,39.9491751,116.433202,39.9493146,116.4336419,39.949379,116.4339209,39.9494541,116.4343822,39.9494648,116.4345431,39.9494541,116.4349401,39.9494648,116.4363992,39.949379,116.4425576,39.9493897,116.4436948,39.9494326,116.4442742,39.9495184,116.4447677,39.9496257,116.445111,39.9498403,116.4456046,39.9499691,116.4458621,39.9502051,116.4461946,39.9505699,116.4466345,39.9516642,116.4477718,39.9523079,116.4485013,39.9540782,116.4504433,39.9547219,116.4511836,39.9555588,116.4520955,39.9572861,116.4540374,39.9578869,116.4546812,39.9581552,116.4549816,39.9581981,116.4550674,39.9582517,116.4552176,39.9582624,116.4553893,39.958241,116.4555287,39.9581444,116.455754,39.958005,116.4558613,39.9579406,116.4558828,39.9577904,116.4558828,39.9576616,116.4558184,39.9575651,116.4557326,39.9575007,116.4556146,39.9574578,116.4554429,39.9574471,116.4551747,39.9574792,116.4550352,39.9579298,116.4543486,39.9579835,116.4542842,39.9580371,116.454252,39.9581659,116.4541769,39.9581981,116.4541662,39.9582732,116.4541769,39.958359,116.4542413,39.9588311,116.4547563,39.9599683,116.4560544,39.9609339,116.4570951,39.9611807,116.4573848,39.9616957,116.4578998,39.9618137,116.4579749,39.9618781,116.4579856,39.9638629,116.460228,39.9668133,116.4634681,39.967972,116.464777,39.9692166,116.4661396,39.9693346,116.4662898,39.9697423,116.4667082,39.9705148,116.4675772,39.9728215,116.4700985,39.9728751,116.4701736,39.9729609,116.4702487,39.9734008,116.4707637,39.9742591,116.4717185,39.9746776,116.4721584,39.9757719,116.473403,39.9762332,116.473875,39.9762654,116.4739287,39.977349,116.4750981,39.9782181,116.4760637,39.9783146,116.4761388,39.9800634,116.4781344,39.9802244,116.4782953,39.9842906,116.48278,39.9862754,116.4849901,39.9866617,116.4853978,39.9881637,116.4870715,39.9887967,116.4878118,39.9889898,116.4880157,39.9890649,116.4880908,39.9905348,116.4857841,39.9912214,116.4847541,39.9919403,116.4836597,39.9925196,116.4827478,39.992584,116.4826727,39.9936354,116.4810526,39.9962962,116.4770508,39.9963713,116.4769542,39.9969292,116.4760423,39.9971867,116.4756668,39.9974549,116.4753127,39.998678,116.4734352,39.9987209,116.4733815,39.9987531,116.4734352,39.9987853,116.4734566,39.999311,116.4740467,39.9992681,116.4741004,39.9991023,116.4743121]
	fake_array = []
	for index in range(0,len(path_a) / 2):
		geo = (float(path_a[index * 2 + 1]),float(path_a[index * 2]))
		fake_array.append(geo)
	
	last_point = None
	print 'computing',
	sys.stdout.flush()
	for data_item in fake_array:
		if last_point == None:
			last_point = data_item
			continue
		current_point = data_item
		result = lm.match(last_point, current_point)
		print last_point, current_point, 'matched to:', result
		sys.stdout.flush()
		last_point = current_point



	
if __name__=='__main__':
	main()