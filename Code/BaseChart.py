#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is a lib file for Kao Pu Routing program 
# Created in 2014
# ######################################################################
import math
from Tkinter import *
from PIL import Image, ImageFont, ImageTk, ImageDraw

BASECHART_LINE_COLOR = '#000000'
BASECHART_TEXT_COLOR = '#000000'
BASECHART_SPOT_COLOR = '#FF0000'
BASECHART_FIGURE_COLOR = '#0000FF'

BASECHART_LINE_WIDTH = 1
BASECHART_FIGURE_WIDTH = 1

class BaseChart:
	def __init__(self, width, height, reverse_y_direction = False):
		# basic attributes
		self.width = width
		self.height = height
		if reverse_y_direction:
			self.y_factor = -1
		else:
			self.y_factor = 1
		
		# prepare object of image
		self.dynamic_image_obj = Image.new('RGBA', (self.width, self.height))
		
		self.font_size = 14
		self.text_font = ImageFont.truetype('simfang.ttf',self.font_size)
		
		# data of value
		self.value_array = []
		self.max_value = 120
		self.value_step = 1
		
		# data of control
		self.select_slot = 50

		# draw values
		self.pad = 4	# pad as margin
		self.axis_value_pad = 30	# pad to display axis value
		zero_pos_x = 0 + self.pad + self.axis_value_pad
		if reverse_y_direction:
			zero_pos_y = 0 + self.pad + self.axis_value_pad
		else:
			zero_pos_y = height - self.pad - self.axis_value_pad
		self.zero_pos = (zero_pos_x,zero_pos_y)
		self.slot_width = 1
		self.slot_height = 2
		self.num_of_slot_x = 24 * 12	# 5 mins a slot
		self.num_of_slot_y = 100	# max speed is set to 120		
		self.value_step = 1
		
	
	def set_value_array(self, value_array):
		self.value_array = value_array
		if len(self.value_array) > 0:
			max_value = max(self.value_array)
			self.value_step = (math.ceil(max_value / 10) * 10) / 100
			self.max_value = self.value_step * 100
		else:
			self.value_step = 1
			self.max_value = 100
		self.static_image_obj = Image.new('RGBA', (self.width, self.height))
		draw_obj = ImageDraw.Draw(self.static_image_obj)
		self.draw_axis(draw_obj)
		self.draw_value(draw_obj)
		self.static_photo = ImageTk.PhotoImage(self.static_image_obj)
	
	def get_static_photo(self):
		return self.static_photo
	
	def draw_value(self,draw_obj):
		index = 0
		last_pos = None
		for value in self.value_array:
			pos_x = self.zero_pos[0] + index * self.slot_width
			pos_y = self.zero_pos[1] - value / self.max_value * 100 * self.slot_height * self.y_factor
			current_pos = [pos_x,pos_y]
			if last_pos != None:
				draw_obj.line((last_pos[0], last_pos[1], current_pos[0], current_pos[1]), 
										fill = BASECHART_FIGURE_COLOR, width = BASECHART_FIGURE_WIDTH)
			last_pos = current_pos
			index += 1

				
	def draw_axis(self, draw_obj):
		# AXIS X
		length = self.slot_width * self.num_of_slot_x + 10
		
		line_pos = (self.zero_pos[0], self.zero_pos[1], 
						self.zero_pos[0] + length, self.zero_pos[1])
		draw_obj.line(line_pos, fill = BASECHART_LINE_COLOR, width = BASECHART_LINE_WIDTH);
		line_pos = (self.zero_pos[0] + length, self.zero_pos[1],
						self.zero_pos[0] + length - 5, self.zero_pos[1] - 5)
		draw_obj.line(line_pos, fill = BASECHART_LINE_COLOR, width = BASECHART_LINE_WIDTH);
		line_pos = (self.zero_pos[0] + length, self.zero_pos[1],
						self.zero_pos[0] + length - 5, self.zero_pos[1] + 5)
		draw_obj.line(line_pos, fill = BASECHART_LINE_COLOR, width = BASECHART_LINE_WIDTH);
		
		x_value_mark_shift = self.y_factor * 5
		if self.y_factor > 0:
			x_text_shift = x_value_mark_shift + 3
		else:
			x_text_shift = x_value_mark_shift - self.font_size - 3
		for i in range(0,self.num_of_slot_x / 12+1):
			index = i * 12
			line_pos = (self.zero_pos[0] + index * self.slot_width, self.zero_pos[1],
						self.zero_pos[0] + index * self.slot_width, self.zero_pos[1] + x_value_mark_shift)
			draw_obj.line(line_pos,fill = BASECHART_LINE_COLOR, width = BASECHART_LINE_WIDTH);
		for i in range(0,self.num_of_slot_x / 24+1):
			index = i * 24
			word = ('%d' % round(index*5/60) )
			draw_obj.text((self.zero_pos[0] + index * self.slot_width - self.font_size/2, self.zero_pos[1] + x_text_shift), 
							word, fill = BASECHART_TEXT_COLOR, font = self.text_font)
		
		# AXIS Y
		length = self.slot_height * self.num_of_slot_y + 10
		end_pos = (self.zero_pos[0], self.zero_pos[1] - length * self.y_factor)
		line_pos = (self.zero_pos[0], self.zero_pos[1], 
						self.zero_pos[0], self.zero_pos[1] - length * self.y_factor)
		draw_obj.line(line_pos,fill = BASECHART_LINE_COLOR, width = BASECHART_LINE_WIDTH)
		
		line_pos = (end_pos[0], end_pos[1],end_pos[0] - self.y_factor * 5, end_pos[1] + self.y_factor * 5 )
		draw_obj.line(line_pos,fill = BASECHART_LINE_COLOR, width = BASECHART_LINE_WIDTH)
		line_pos = (end_pos[0], end_pos[1],end_pos[0] + self.y_factor * 5, end_pos[1] + self.y_factor * 5 )
		draw_obj.line(line_pos,fill = BASECHART_LINE_COLOR, width = BASECHART_LINE_WIDTH)
		for i in range(0,self.num_of_slot_y / 10+1):
			index = i * 10
			word = ('%d' % round(index * self.value_step) )
			line_pos = (self.zero_pos[0] , self.zero_pos[1]- index * self.slot_height * self.y_factor,
						self.zero_pos[0] - 5, self.zero_pos[1] - index * self.slot_height * self.y_factor)
			draw_obj.line(line_pos,fill = BASECHART_LINE_COLOR, width = BASECHART_LINE_WIDTH)
			draw_obj.text((self.zero_pos[0] - self.font_size*2, 
						self.zero_pos[1]  - index * self.slot_height*self.y_factor - self.font_size/2),  
						word, fill = BASECHART_TEXT_COLOR, font = self.text_font)


# unit test code

def main():
	root_widget = Tk()
	
	map_area = LabelFrame(root_widget, text = "Traffic Map", padx=5,pady=5)
	map_area.pack(side = LEFT)

	map_canvas = Canvas(map_area, width = 1600, height = 800 + 50)
	map_canvas.pack()
	
	basechart_obj = BaseChart(350,250,False)
	value_array = []
	for i in range(0,100):
		value_array.append(i)
	basechart_obj.set_value_array(value_array)
	photo_1 = basechart_obj.get_static_photo()
	map_canvas.create_image(1400,150, image= photo_1)

	basechart_obj_x = BaseChart(350,250,True)
	basechart_obj_x.set_value_array(value_array)
	photo_2 = basechart_obj_x.get_static_photo()
	map_canvas.create_image(1400,400, image= photo_2)
	
	root_widget.mainloop()

			
if __name__=='__main__':
	main()