#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is one of traffic map utility component files
# Created in 2013
# ######################################################################
from PIL import Image, ImageTk, ImageFont, ImageDraw
from Tkinter import *
from BaseMap import *

PANEL_WIDTH = 350
PANEL_HEIGHT = 850

TITLE_TEXT = '约会模式'
DATE_TEXT = '2014-06-18'
APPOINTMENT_TIME_TEXT = '约会时间:'
APPOINTMENT_PLACE_TEXT = '约会地点:'
FROM_TEXT = '出发地点:'

SUGGESTED_START_TIME_TEXT = '建议出发时间:'
TTA_CERTAINTY_TEXT = '准时到达概率:'

ZOOM_LEVEL_TEXT = '地图图层:'

BACKGROUND_COLOR = (0,125,200,150)

LEFT_POS_0 = 100
LEFT_POS_1 = 50
LEFT_POS_2 = 30

LINE_INTERVAL = 30

POS_TITLE = [LEFT_POS_0, 20]
POS_DATE = [LEFT_POS_2, 80]

POS_SLIDER = [0,0]
POS_APPOINTMENT_TIME = [LEFT_POS_1, 140]
POS_APPOINTMENT_PLACE = [LEFT_POS_1, 140 + LINE_INTERVAL]
POS_FROM = [LEFT_POS_1, 140 + LINE_INTERVAL * 2]
POS_SUGGESTED_START_TIME = [LEFT_POS_2, 140 + LINE_INTERVAL * 3.5]
POS_TTA_CERTAINTY = [LEFT_POS_2, 140 + LINE_INTERVAL * 4.5]
POS_ZOOM_LEVEL = [LEFT_POS_2, PANEL_HEIGHT - 60]

RIGHT_POS_0 = 100
RIGHT_POS_1 = 170
RIGHT_POS_2 = 100

POS_OUTPUT_APPOINTMENT_TIME = [LEFT_POS_1+RIGHT_POS_0, 140]
POS_OUTPUT_APPOINTMENT_PLACE = [LEFT_POS_1+RIGHT_POS_0, 140 + LINE_INTERVAL]
POS_OUTPUT_FROM = [LEFT_POS_1+RIGHT_POS_0, 140 + LINE_INTERVAL * 2]
POS_OUTPUT_SUGGESTED_START_TIME = [LEFT_POS_2+RIGHT_POS_1, 140 + LINE_INTERVAL * 3.5]
POS_OUTPUT_TTA_CERTAINTY = [LEFT_POS_2+RIGHT_POS_1, 140 + LINE_INTERVAL * 4.5]
POS_OUTPUT_ZOOM_LEVEL = [LEFT_POS_2+RIGHT_POS_2, PANEL_HEIGHT - 60]

POS_SLIDER_DATE = [LEFT_POS_2, 125]
POS_SLIDER_ZOOM_LEVEL = [LEFT_POS_2, PANEL_HEIGHT - 25 ]
POS_SLIDER_TIME = [LEFT_POS_2, 140 + LINE_INTERVAL * 5.5 + 200 + 20 + 20 ]

# Below is the area for class definition
# Route Forecast Slider
class RFPannel:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		
		self.pannel_image_obj = Image.new('RGBA', (self.width, self.height), BACKGROUND_COLOR)
		self.output_image_obj = Image.new('RGBA', (self.width, self.height))
		self.title_text_font = ImageFont.truetype('simhei.ttf',36)
		self.date_text_font = ImageFont.truetype('simhei.ttf',24)
		self.body_text_font = ImageFont.truetype('simhei.ttf',20)
		
		self.title_text_color = '#ffffff'
		self.date_text_color = '#ffff88'
		self.body_text_color = '#ffff88'

		self.line_width = 5
		self.slider_length = 288
		self.slider_line_color = '#ffff88'
		
		self.draw_pannel()
		
	
	#def set_data(self):
		self.date = '2014-06-20'
		self.time = '16:00'
		self.start_geo = '116.21734,46.83424'
		self.end_geo = '115.72374,46.23482'
		self.go_time = '13:00'
		self.certainty = '80%'
		self.zoom_level = '12'
		
	def get_static_photo(self):
		self.static_photo = ImageTk.PhotoImage(self.pannel_image_obj)
		return self.static_photo
	
	def get_dynamic_photo(self):
		self.output_image_obj = Image.new('RGBA', (self.width, self.height))
		draw_obj = ImageDraw.Draw(self.output_image_obj)
		
		draw_obj.text(POS_OUTPUT_APPOINTMENT_TIME, self.time, fill = self.body_text_color, font = self.body_text_font)
		draw_obj.text(POS_OUTPUT_APPOINTMENT_PLACE, self.end_geo, fill = self.body_text_color, font = self.body_text_font)
		draw_obj.text(POS_OUTPUT_FROM, self.start_geo, fill = self.body_text_color, font = self.body_text_font)
		draw_obj.text(POS_OUTPUT_SUGGESTED_START_TIME, self.go_time, fill = self.body_text_color, font = self.date_text_font)
		draw_obj.text(POS_OUTPUT_TTA_CERTAINTY, self.certainty, fill = self.body_text_color, font = self.date_text_font)

		draw_obj.text(POS_OUTPUT_ZOOM_LEVEL, self.zoom_level, fill = self.body_text_color, font = self.body_text_font)

		draw_obj.text(POS_DATE, self.date, fill = self.title_text_color, font = self.title_text_font)

		self.dynamic_photo = ImageTk.PhotoImage(self.output_image_obj)
		return self.dynamic_photo
	
	def draw_pannel(self):
		self.draw_obj = ImageDraw.Draw(self.pannel_image_obj)
		self.draw_obj.text(POS_TITLE, TITLE_TEXT.decode('utf-8'), fill = self.title_text_color, font = self.title_text_font) #,.decode('utf8')

		self.draw_obj.text(POS_APPOINTMENT_TIME, APPOINTMENT_TIME_TEXT.decode('utf-8'), fill = self.body_text_color, font = self.body_text_font)
		self.draw_obj.text(POS_APPOINTMENT_PLACE, APPOINTMENT_PLACE_TEXT.decode('utf-8'), fill = self.body_text_color, font = self.body_text_font)
		self.draw_obj.text(POS_FROM, FROM_TEXT.decode('utf-8'), fill = self.body_text_color, font = self.body_text_font)
		self.draw_obj.text(POS_SUGGESTED_START_TIME, SUGGESTED_START_TIME_TEXT.decode('utf-8'), fill = self.body_text_color, font = self.date_text_font)
		self.draw_obj.text(POS_TTA_CERTAINTY, TTA_CERTAINTY_TEXT.decode('utf-8'), fill = self.body_text_color, font = self.date_text_font)
		self.draw_obj.text(POS_ZOOM_LEVEL, ZOOM_LEVEL_TEXT.decode('utf-8'), fill = self.body_text_color, font = self.body_text_font)
		
		self.draw_slider()
	
	def draw_slider(self):
		# slider

		pos_left = POS_SLIDER_DATE
		pos_right = [pos_left[0] + self.slider_length, pos_left[1]]
		pos = [pos_left[0],pos_left[1],pos_right[0],pos_right[1]]
		self.draw_obj.line(pos, fill = self.slider_line_color, width = self.line_width)
		
		pos_left = POS_SLIDER_TIME
		pos_right = [pos_left[0] + self.slider_length, pos_left[1]]
		pos = [pos_left[0]+5,pos_left[1],pos_right[0]+5,pos_right[1]]
		self.draw_obj.line(pos, fill = self.slider_line_color, width = self.line_width)

		pos_left = POS_SLIDER_ZOOM_LEVEL
		pos_right = [pos_left[0] + self.slider_length, pos_left[1]]
		pos = [pos_left[0],pos_left[1],pos_right[0],pos_right[1]]
		self.draw_obj.line(pos, fill = self.slider_line_color, width = self.line_width)
		
		
# Below is for helper functions

# unit test code

def main():

	# Here, your unit test code or main program

	# init Tkinter
	root_widget = Tk()
	
	map_area = LabelFrame(root_widget, text = "Traffic Map", padx=5,pady=5)
	map_area.pack(side = LEFT)

	map_canvas = Canvas(map_area, width = 1600, height = PANEL_HEIGHT + 50)
	map_canvas.pack()
	
	basemap_instance = BaseMap((1600,PANEL_HEIGHT + 50))
	basemap_instance.draw(map_canvas)
	
	
	pannel_obj = RFPannel(PANEL_WIDTH,PANEL_HEIGHT)
	
	photo_1 = pannel_obj.get_static_photo()
	map_canvas.create_image(1400,(PANEL_HEIGHT + 50)/2, image= photo_1)
	pannel_obj.set_data()
	photo_2 = pannel_obj.get_dynamic_photo()
	map_canvas.create_image(1400,(PANEL_HEIGHT + 50)/2, image= photo_2)

	root_widget.mainloop()


	
			
if __name__=='__main__':
	main()