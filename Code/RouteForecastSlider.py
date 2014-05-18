#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is one of traffic map utility component files
# Created in 2013
# ######################################################################
from PIL import Image, ImageTk, ImageDraw
from Tkinter import *
from BaseMap import *

# Below is the area for class definition
# Route Forecast Slider
class RouteForecastSlider:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.radius = self.height / 2
		self.image_obj = Image.new('RGBA', (self.width, self.height), (0,125,200,75))
		self.draw_obj = ImageDraw.Draw(self.image_obj)
		self.border_color_1 = '#4EA6CE'
		self.border_color_2 = '#70D7FF'
		self.line_width = 5
		self.slider_length = 288
		self.slider_line_color = '#ffffff'
		self.draw_all_slider([10,30])
	
	def get_photo(self):
		self.photo_obj = ImageTk.PhotoImage(self.image_obj)
		return self.photo_obj
	
	def draw_all_slider(self, pos):
		# Slider for Date
		self.draw_slider([pos[0],pos[1]])
		# Slider for Time
		self.draw_slider([pos[0],pos[1] + 300])
		# Slider for Map Zoom Level
		self.draw_slider([pos[0],pos[1] + 300 * 2])
		
	def draw_slider(self, pos):
		# slider
		
		line_points = [pos[0], pos[1], pos[0] + self.slider_length, pos[1]]
		self.draw_obj.line(line_points, fill = self.slider_line_color, width = self.line_width)
		
		
		'''
		arc_1_conner_1 = [0,0]
		arc_1_conner_2 = [self.radius * 2 - 1, self.radius * 2 - 1]
		arc_2_conner_1 = [self.width - self.radius * 2 - 1, 0]
		arc_2_conner_2 = [self.width - 1, self.radius * 2 - 1]

		# draw left arc
		bbox = [arc_1_conner_1[0], arc_1_conner_1[1], arc_1_conner_2[0], arc_1_conner_2[1]]
		self.draw_obj.arc(bbox, 90,270, fill = self.border_color_1)
		bbox[0] += self.line_width
		bbox[1] += self.line_width
		bbox[2] -= self.line_width
		bbox[3] -= self.line_width
		self.draw_obj.arc(bbox, 90,270, fill = self.border_color_2)

		# draw right arc
		bbox = [arc_2_conner_1[0], arc_2_conner_1[1], arc_2_conner_2[0], arc_2_conner_2[1]]
		self.draw_obj.arc(bbox, -90,90, fill = self.border_color_1)
		bbox[0] += self.line_width
		bbox[1] += self.line_width
		bbox[2] -= self.line_width
		bbox[3] -= self.line_width
		self.draw_obj.arc(bbox, -90,90, fill = self.border_color_2)

		# draw lines between arcs
		point_1 = [self.radius,0]
		point_2 = [self.width - self.radius, 0]
		point_3 = [self.radius, self.radius * 2 - self.line_width]
		point_4 = [self.width - self.radius, self.radius * 2 - self.line_width]
		
		line_pos_array = [point_1[0],point_1[1], point_2[0],point_2[1]]
		self.draw_obj.line(line_pos_array, fill = self.border_color_1, width = self.line_width)
		line_pos_array[1] += self.line_width
		line_pos_array[3] += self.line_width
		self.draw_obj.line(line_pos_array, fill = self.border_color_2, width = self.line_width)
		line_pos_array = [point_3[0], point_3[1], point_4[0],point_4[1]]
		self.draw_obj.line(line_pos_array, fill = self.border_color_1, width = self.line_width)
		line_pos_array[1] -= self.line_width
		line_pos_array[3] -= self.line_width
		self.draw_obj.line(line_pos_array, fill = self.border_color_2, width = self.line_width)
		'''
		pass
		
# Below is for helper functions

# unit test code

def main():

	# Here, your unit test code or main program

	# init Tkinter
	root_widget = Tk()
	
	map_area = LabelFrame(root_widget, text = "Traffic Map", padx=5,pady=5)
	map_area.pack(side = LEFT)

	map_canvas = Canvas(map_area, width = 1600, height = 900)
	map_canvas.pack()
	
	basemap_instance = BaseMap((1600,900))
	basemap_instance.draw(map_canvas)
	
	slider_obj = RouteForecastSlider(350,800)
	
	photo = slider_obj.get_photo()
	map_canvas.create_image(1400,450, image= photo)
	
	root_widget.mainloop()

			
if __name__=='__main__':
	main()