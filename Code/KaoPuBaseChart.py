#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is a lib file for Kao Pu Routing program 
# Created in 2014
# ######################################################################
import math
from Tkinter import *

class KaoPuBaseChart:
	def __init__(self, canvas, width, height):
		self.canvas = canvas
		self.width = width
		self.height = height
		self.pad = 4
		self.axis_value_pad = 20
		self.zero_pos = (0 + self.pad + self.axis_value_pad, height - self.pad - self.axis_value_pad)
		self.selected_slot = 50
		self.value_array = []
		self.benchmark_value = None

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
	
	def set_benchmark_value(self,value):
		self.benchmark_value = value
	
	def draw(self):
		self.canvas.delete(ALL)
		self.draw_slot_bar()
		self.draw_axis()
		self.draw_bar_chart()
	
	def draw_bar_chart(self):
		pos = [self.zero_pos[0],self.zero_pos[1]]
		pos[0] += 1
		pos[1] -= 1
		index = 0
		last_pos = None
		
		if self.benchmark_value != None:
			y = self.zero_pos[1] - self.slot_height * (self.benchmark_value/self.max_value * 100)
			from_pos = [self.zero_pos[0], y]
			to_pos = [self.zero_pos[0] + self.slot_width * self.num_of_slot_x, y]
			self.canvas.create_line(from_pos[0], from_pos[1], to_pos[0], to_pos[1], 
										fill = 'Dark Slate Blue')

		for value in self.value_array:
			current_pos = [pos[0]+ self.slot_width*index, pos[1] - self.slot_height * (value/self.max_value * 100)]
			self.canvas.create_text(current_pos[0], current_pos[1], 
										text ='*', fill = 'blue')
			if last_pos != None:
				self.canvas.create_line(last_pos[0], last_pos[1], current_pos[0], current_pos[1], 
										fill = 'blue')
			last_pos = current_pos
			index += 1
	
	def draw_slot_bar(self):
		if self.selected_slot == None:
			return
		height_of_bar = self.slot_height * self.num_of_slot_y
		pos = [self.zero_pos[0] + self.selected_slot * self.slot_width,self.zero_pos[1]]
		box = [pos[0] - 5, pos[1], pos[0] + 5, pos[1] - height_of_bar]
		self.canvas.create_rectangle(box, fill = 'green', outline = 'green')
		line_pos = [pos[0], pos[1], pos[0], pos[1] - height_of_bar]
		self.canvas.create_line(line_pos, fill = 'red');
		if len(self.value_array) >= self.selected_slot:
			txt = str(int(self.value_array[self.selected_slot]))
			txt = ('结果: %s' % txt)
			self.canvas.create_text(self.width / 2 , self.height / 2, text = txt, font = ('Purisa',32), fill = 'red')
			if self.benchmark_value != None:
				txt = str(int(self.benchmark_value))
				txt = ('参考: %s' % txt)
				self.canvas.create_text(self.width / 2 , self.height / 4 * 3, text = txt, font = ('Purisa',32), fill = 'red')
	
	def draw_axis(self):
		# AXIS X
		length = self.slot_width * self.num_of_slot_x + 10
		
		line_pos = (self.zero_pos[0], self.zero_pos[1], 
						self.zero_pos[0] + length, self.zero_pos[1])
		self.canvas.create_line(line_pos);
		line_pos = (self.zero_pos[0] + length, self.zero_pos[1],
						self.zero_pos[0] + length - 5, self.zero_pos[1] - 5)
		self.canvas.create_line(line_pos);
		line_pos = (self.zero_pos[0] + length, self.zero_pos[1],
						self.zero_pos[0] + length - 5, self.zero_pos[1] + 5)
		self.canvas.create_line(line_pos);
		
		for i in range(0,self.num_of_slot_x / 12+1):
			index = i * 12
			line_pos = (self.zero_pos[0] + index * self.slot_width, self.zero_pos[1],
						self.zero_pos[0] + index * self.slot_width, self.zero_pos[1] + 5)
			self.canvas.create_line(line_pos);
		for i in range(0,self.num_of_slot_x / 24+1):
			index = i * 24
			word = ('%d' % round(index*5/60) )
			self.canvas.create_text(self.zero_pos[0] + index * self.slot_width, self.zero_pos[1] + 15, text = word)
		
		# AXIS Y
		length = self.slot_height * self.num_of_slot_y + 10
		line_pos = (self.zero_pos[0], self.zero_pos[1], 
						self.zero_pos[0], self.zero_pos[1] - length)
		self.canvas.create_line(line_pos);
		line_pos = (self.zero_pos[0], self.zero_pos[1] - length,
						self.zero_pos[0] - 5, self.zero_pos[1] - length + 5)
		self.canvas.create_line(line_pos);
		line_pos = (self.zero_pos[0], self.zero_pos[1] - length,
						self.zero_pos[0] + 5, self.zero_pos[1] - length + 5)
		self.canvas.create_line(line_pos);		
		for i in range(0,self.num_of_slot_y / 10+1):
			index = i * 10
			word = ('%d' % round(index * self.value_step) )
			line_pos = (self.zero_pos[0] , self.zero_pos[1]- index * self.slot_height,
						self.zero_pos[0] - 5, self.zero_pos[1] - index * self.slot_height)
			self.canvas.create_line(line_pos);
			self.canvas.create_text(self.zero_pos[0] - 15, self.zero_pos[1]  - index * self.slot_height, text = word)

	def convert_pos_to_slot(self,pos):
		diff = pos[0] - self.zero_pos[0]
		if diff < 0:
			return None
		index = diff / self.slot_width
		return index
	
	def handler_slot_change(self,event):
		# check if it is on hot spot, for loop should be full loop in order to make sure select the one on top
		if event.x >= self.zero_pos[0] and event.x <= self.zero_pos[0] + self.num_of_slot_x * self.slot_width:
			self.selected_slot = self.convert_pos_to_slot([event.x,event.y])
		elif event.x < self.zero_pos[0]:
			self.selected_slot = 0
		else:
			self.selected_slot = self.num_of_slot_x - 1


# unit test code

def main():
	pass

			
if __name__=='__main__':
	main()