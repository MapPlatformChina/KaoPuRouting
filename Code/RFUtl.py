#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is a lib file for Kao Pu Routing program 
# Created in 2014
# ######################################################################
import sys
from Tkinter import *
import tkFileDialog
from BaseMap import *
from KPRouteMain import *
from RFBaseChart import *
from RFPannel import *
import datetime

MAP_AREA_SIZE = (1600,800)
WINDOWS_SIZE = (1600,830)
POS_PANNEL_DIS = (1400,400)

POS_SLIDER_DATE = [LEFT_POS_2, 105]
POS_SLIDER_TIME = [LEFT_POS_2, 120 + LINE_INTERVAL * 5.5 + 200 + 20 + 13]
POS_SLIDER_ZOOM_LEVEL = [LEFT_POS_2, PANEL_HEIGHT - 15 ]

Y_DIS_SHIFT = (MAP_AREA_SIZE[1] - PANEL_HEIGHT)/2
POS_SLIDER_CONTROL_DATE = [POS_PANNEL_DIS[0] - PANEL_WIDTH/2 + POS_SLIDER_DATE[0], Y_DIS_SHIFT + POS_SLIDER_DATE[1]]
POS_SLIDER_CONTROL_TIME = [POS_PANNEL_DIS[0] - PANEL_WIDTH/2  + POS_SLIDER_TIME[0] + 5, Y_DIS_SHIFT + POS_SLIDER_TIME[1]]
POS_SLIDER_CONTROL_ZOOM_LEVEL = [POS_PANNEL_DIS[0] - PANEL_WIDTH/2  + POS_SLIDER_ZOOM_LEVEL[0], Y_DIS_SHIFT + POS_SLIDER_ZOOM_LEVEL[1]]

# pos of button
POS_BUTTON = [POS_PANNEL_DIS[0]+105 ,Y_DIS_SHIFT+80]

PROGRAM_TITLE = '出行管家 V1.0'
MAP_AREA_TITLE = '地图'

WEEK_DAY_TEXT = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']

PAD_X = 2
PAD_Y = 2

DIAGRAM_ZERO = (20,20)

class RFUtl:
	def __init__(self, root_widget):
		self.widget = root_widget
		
		# map view
		self.center_latitude = 39.9065759877
		self.center_longitude = 116.399459839
		self.basemap = BaseMap(MAP_AREA_SIZE,256, [self.center_longitude,self.center_latitude])

		# map view para
		self.zoom_level = 12
		self.zero_level = 6
		
		# spot geo
		self.from_latitude = 39.9515592744
		self.from_longitude = 116.41934259
		self.to_latitude = 39.9992530
		self.to_longitude = 116.4744977
		self.basemap.add_spot((self.from_longitude, self.from_latitude), 10, '始')
		self.basemap.add_spot((self.to_longitude, self.to_latitude), 10, '终')
		
		# pannel
		self.pannel_obj = RFPannel(PANEL_WIDTH,PANEL_HEIGHT)
		self.button_pressed = False
		
		# chart
		self.tta_chart = RFBaseChart(350,250)
		self.ci_chart = RFBaseChart(350,250,True)
		
		# date
		self.date = datetime.datetime(2014, 4, 28)
		self.time = datetime.time(0,0,0,0)
		self.selected_time_slot = 8 * 12
				

		
		# tta and ci
		self.departure_time = '13:00'
		self.ci_value = 0.8
		
		# compute result
		self.tta_array = []
		self.ci_array = []
		self.path_array = []
		
		self.set_pannel_data()
		
		button_file_1 = '../res/button_1.png'
		self.button_image_1 = Image.open(button_file_1)
		button_file_2 = '../res/button_2.png'
		self.button_image_2 = Image.open(button_file_2)
		self.button_photo_1 = ImageTk.PhotoImage(self.button_image_1)
		self.button_photo_2 = ImageTk.PhotoImage(self.button_image_2)
		
		# slider controls
		self.sliders = []
		self.add_slider(POS_SLIDER_CONTROL_DATE, 288)
		self.add_slider(POS_SLIDER_CONTROL_TIME, 288)
		zoom_value =int(288.0 / 18 * (self.zoom_level - self.zero_level) + 288.0/18/2)
		self.add_slider(POS_SLIDER_CONTROL_ZOOM_LEVEL, 288,zoom_value)

		
		self.slider_date_pressed = False
		self.slider_time_pressed = False
		self.slider_zoom_level_pressed = False
		
		# route computation obj
		self.route_obj = KPRouteMain()
		
	def construct_layout(self):
		
		# resize window and add title
		geometry_msg = ('%dx%d' % WINDOWS_SIZE)
		self.widget.geometry(geometry_msg)
		self.widget.title(PROGRAM_TITLE)
		
		# initiate all frames
		self.map_frame = LabelFrame(self.widget, text = MAP_AREA_TITLE, padx = PAD_X, pady = PAD_Y)
		
		# add controls into frames
		self.map_canvas = Canvas(self.map_frame, width = MAP_AREA_SIZE[0], height = MAP_AREA_SIZE[1])

		self.map_frame.pack()
		self.map_canvas.pack()
		
		self.map_canvas.bind("<Button-1>", self.handler_b1_down)
		self.map_canvas.bind("<B1-Motion>", self.handler_b1_move)
		self.map_canvas.bind("<ButtonRelease-1>", self.handler_b1_release)
		
	def draw(self):
		self.map_canvas.delete(ALL)
		self.basemap.draw(self.map_canvas, self.path_array)
		
		self.map_canvas.create_image(POS_PANNEL_DIS[0],POS_PANNEL_DIS[1], image = self.pannel_obj.get_static_photo())
		self.map_canvas.create_image(POS_PANNEL_DIS[0],POS_PANNEL_DIS[1], image = self.pannel_obj.get_dynamic_photo())
		
		self.map_canvas.create_image(POS_PANNEL_DIS[0],POS_PANNEL_DIS[1] , image = self.tta_chart.get_static_photo())
		self.map_canvas.create_image(POS_PANNEL_DIS[0],POS_PANNEL_DIS[1] + 240, image = self.ci_chart.get_static_photo())
		self.map_canvas.create_image(POS_PANNEL_DIS[0],POS_PANNEL_DIS[1]  , image = self.tta_chart.get_dynamic_photo())
		self.map_canvas.create_image(POS_PANNEL_DIS[0],POS_PANNEL_DIS[1] + 240, image = self.ci_chart.get_dynamic_photo())
		self.map_canvas.create_image(POS_PANNEL_DIS[0],POS_PANNEL_DIS[1] , image = self.tta_chart.get_pot_photo(self.selected_time_slot))
		self.map_canvas.create_image(POS_PANNEL_DIS[0],POS_PANNEL_DIS[1] + 240, image = self.ci_chart.get_pot_photo(self.selected_time_slot))
		
		if self.button_pressed:
			b_photo = self.button_photo_2
		else:
			b_photo = self.button_photo_1
		self.map_canvas.create_image(POS_BUTTON[0],POS_BUTTON[1], image = b_photo)
		
		self.draw_sliders(self.map_canvas)
		
	def add_slider(self, slider_pos, slider_length, slider_value = 0, slider_radius = 7, is_selected = False):
		slider_current = 0
		self.sliders.append([slider_pos, slider_length, slider_value, slider_radius, is_selected])

	def get_slider(self, index):
		return self.sliders[index]
	
	def draw_sliders(self, canvas):
		for slider in self.sliders:
			pos = slider[0]
			length = slider[1]
			r = slider[3]
			value = slider[2]
			if value < length:
				canvas.create_oval([pos[0] + value -r,pos[1]-r,pos[0]+value+r,pos[1]+r],fill='blue')
	
	def check_pos_of_click(self,pos):
		button_width = 120
		button_height = 40
		slider_radius = 5
		self.slider_length = 288

		pos_left = POS_SLIDER_DATE
		pos_right = [pos_left[0] + self.slider_length, pos_left[1]]
		pos_date = [pos_left[0],pos_left[1],pos_right[0],pos_right[1]]
		
		pos_left = POS_SLIDER_TIME
		pos_right = [pos_left[0] + self.slider_length, pos_left[1]]
		pos_time = [pos_left[0]+5,pos_left[1],pos_right[0]+5,pos_right[1]]

		pos_left = POS_SLIDER_ZOOM_LEVEL
		pos_right = [pos_left[0] + self.slider_length, pos_left[1]]
		pos_zoom_level = [pos_left[0],pos_left[1],pos_right[0],pos_right[1]]

		if POS_BUTTON[0] - button_width / 2 <= pos[0] and\
				POS_BUTTON[0] + button_width / 2 >= pos[0] and\
				POS_BUTTON[1] - button_height / 2 <= pos[1] and\
				POS_BUTTON[1] + button_height / 2 >= pos[1]:
			self.button_pressed = True
			return True
			
		for slider in self.sliders:
			pos_slider = slider[0]
			length = slider[1]
			r = slider[3]
			value = slider[2]
			pos_slider = [pos_slider[0] + value, pos_slider[1]]
			if (pos[0] - pos_slider[0]) ** 2 + (pos[1] - pos_slider[1]) ** 2 < r ** 2:
				slider[4] = True
				return True
	
	def handler_b1_down(self,event):
		self.last_zoom_level = self.zoom_level
		if self.check_pos_of_click((event.x,event.y)):
			pass
		else:
			self.basemap.handler_button1_down(event)
		self.set_value()
		self.draw()

	def handler_b1_move(self,event):
		if self.button_pressed:
			return

		flag = False
		for slider in self.sliders:
			if slider[4]:
				flag = True
				if event.x >= slider[0][0] and event.x < slider[0][0] + slider[1]:
					slider[2] = event.x - slider[0][0]
				elif event.x < slider[0][0]:
					slider[2] = 0
				elif event.x >= slider[0][0] + slider[1]:
					slider[2] = slider[1] - 1
		if not flag:
			self.basemap.handler_button1_move(event)

		self.set_value()
		self.draw()
		
	def handler_b1_release(self,event):
		flag = False
		if self.button_pressed:
			flag = True
			self.handler_forecast()
			self.button_pressed = False
		for slider in self.sliders:
			if slider[4]:
				flag = True
				slider[4] = False
				
		if not flag:
			self.basemap.handler_button1_released(event)
		self.set_value()
		if self.zoom_level != self.last_zoom_level:
			self.basemap.set_zoom_level(self.zoom_level)
		self.draw()

	def set_value(self):
		self.from_longitude, self.from_latitude = self.basemap.hot_spots[0][1]
		self.to_longitude, self.to_latitude = self.basemap.hot_spots[1][1]
		self.center_longitude,self.center_latitude = self.basemap.center_coords
		self.zoom_level = math.ceil(self.sliders[2][2] / 1.0 / self.sliders[2][1] * (20-self.zero_level)) + self.zero_level

		self.selected_time_slot = self.sliders[1][2]
		self.time = datetime.datetime(2014,4,28,0,0,0) + datetime.timedelta(minutes = self.selected_time_slot * 5)

		diff = datetime.timedelta(days = self.sliders[0][2])
		zero_date = datetime.datetime(2014,4,28)
		self.date = zero_date + diff
		
		self.set_pannel_data()
		
	
	def set_pannel_data(self):
		self.pannel_obj.start_geo = ('%.5f,%.5f' % (self.from_longitude,self.from_latitude))
		self.pannel_obj.end_geo = ('%.5f,%.5f' % (self.to_longitude,self.to_latitude))
		self.pannel_obj.date = ('%d-%02d-%02d' % (self.date.year, self.date.month, self.date.day))
		self.pannel_obj.time = ('%02d:%02d' % (self.time.hour, self.time.minute))
		
		self.pannel_obj.go_time = '13:00'
		if len(self.ci_array) > self.selected_time_slot:
			self.pannel_obj.certainty = ('%.2f%%' % (self.ci_array[self.selected_time_slot]))
		else:
			self.pannel_obj.certainty = '??%'
		
		datetime_data = datetime.datetime(self.date.year, self.date.month, self.date.day, self.time.hour,self.time.minute,0)
		if len(self.tta_array) > self.selected_time_slot:
			datetime_data = datetime_data - datetime.timedelta(minutes = int(self.tta_array[self.selected_time_slot]))
			self.pannel_obj.go_time = ('%02d:%02d' % (datetime_data.hour, datetime_data.minute))
		else:
			self.pannel_obj.go_time = '??:??'
		
		self.pannel_obj.zoom_level = ('%d' % self.zoom_level)

	def draw_button(self):
		button_file_1 = '../res/button_1.png'
		self.button_image_1 = Image.open(button_file_1)
		button_file_2 = '../res/button_1.png'
		self.button_image_2 = Image.open(button_file_2)
	
	def handler_forecast(self):
		self.date_to_predict = ('%d%02d%02d' % (self.date.year, self.date.month, self.date.day))
		print 'predicting your route in:', self.date_to_predict
		route_result = self.route_obj.get24HrRoutes([str(self.from_latitude),str(self.from_longitude)],
								[str(self.to_latitude), str(self.to_longitude)], self.date_to_predict)

		self.tta_array = route_result.TraveledTime
		self.ci_array = route_result.RouteCertainty

		for i in range(0,len(self.ci_array)):
			self.ci_array[i] *= 100

		self.path_array = []
		for link in route_result.Nodes:
			geo = link
			if geo != None:
				self.path_array.append(( float(geo[1]),float(geo[0]) ))

		self.tta_chart.set_data(self.tta_array)
		self.ci_chart.set_data(self.ci_array)
		
		self.draw()
		print 'num of nodes:', len(route_result.Nodes)
		print 'num of certainty index:',len(route_result.RouteCertainty)
		print 'num of estimated time:',len(route_result.TraveledTime)
		
			
'''
	def update_value(self):
		self.from_latitude = float(self.from_input_lat.get())
		self.from_longitude = float(self.from_input_lon.get())
		self.to_latitude = float(self.to_input_lat.get())
		self.to_longitude = float(self.to_input_lon.get())
		self.center_latitude = float(self.center_input_lat.get())
		self.center_longitude = float(self.center_input_lon.get())
		self.date_to_predict = self.date_input.get()

		year = int(self.date_to_predict[0:4])
		month = int(self.date_to_predict[4:6])
		day = int(self.date_to_predict[6:8])
		date_value = datetime(year, month, day)
		self.vol_of_the_day = date_value.weekday()
		self.week_day_input.delete(0,END)
		self.week_day_input.insert(0,WEEK_DAY_TEXT[self.vol_of_the_day])
		
		self.zoom_level = int(self.zoom_level_slider.get())
		
		# below line is to be optimized later
		self.center_coords = [self.center_latitude,self.center_longitude]	

	def handler_value_update(self,event):
		self.update_value()
		self.update_map()
		self.draw()
		

	def update_map(self):
		#	self.center_coords = ((self.from_longitude + self.to_longitude) / 2, (self.from_latitude + self.to_latitude) / 2)
		self.basemap.set_zoom_level(self.zoom_level)
		self.basemap.set_center([self.center_longitude, self.center_latitude])
		self.basemap.hot_spots[0][1] = [self.from_longitude, self.from_latitude]
		self.basemap.hot_spots[1][1] = [self.to_longitude, self.to_latitude]

	def handler_b1_down(self,event):
		self.basemap.handler_button1_down(event)
		self.set_value()

	def handler_b1_move(self,event):
		self.basemap.handler_button1_move(event)
		self.set_value()
		self.draw()
		
	def handler_b1_release(self,event):
		self.basemap.handler_button1_released(event)
		self.set_value()
		self.draw()
	
	def handler_change_slot(self,event):
		self.et_chart.handler_slot_change(event)
		self.ci_chart.handler_slot_change(event)
		slot = self.ci_chart.selected_slot
		if len(self.et_chart.value_array) >=  slot:
			et_value = self.et_chart.value_array[slot]
			ci_value = self.ci_chart.value_array[slot]
			
			hour = int(round(slot / 12 , 0))
			min = int((slot - hour * 12) * 5)
			time_msg = ('%02d:%02d' % (hour, min))
			self.selected_timeslot_input.delete(0,END)
			self.selected_timeslot_input.insert(0,str(time_msg))
			self.estimated_time_input.delete(0,END)
			self.estimated_time_input.insert(0,str(et_value))
			
			if ci_value >=90:
				ci_msg = RISK_TEXT_1
			elif ci_value >=80:
				ci_msg = RISK_TEXT_2
			elif ci_value >=70:
				ci_msg = RISK_TEXT_3
			elif ci_value >=60:
				ci_msg = RISK_TEXT_4
			else:
				ci_msg = RISK_TEXT_5
			self.ci_result_input.delete(0,END)
			self.ci_result_input.insert(0,ci_msg)
		self.draw()

	def handler_predict(self,event):
		self.update_value()
		print 'predicting your route in:', self.date_to_predict
		route_result = self.route_obj.get24HrRoutes([str(self.from_latitude),str(self.from_longitude)],
								[str(self.to_latitude), str(self.to_longitude)], self.date_to_predict)
		self.estimated_time_array = route_result.TraveledTime
		self.ci_array = route_result.RouteCertainty
		for i in range(0,len(self.ci_array)):
			self.ci_array[i] *= 100
		#for i in range(0,len(self.estimated_time_array)):
		#	self.estimated_time_array[i] *= 100

		# latitude and logitude reverted below in order to work with old class
		self.path_array = []
		#self.path_array.append((float(route_result[0].GEO0[1]),float(route_result[0].GEO0[0])))
		for link in route_result.Nodes:
			geo = link
			if geo != None:
				self.path_array.append(( float(geo[1]),float(geo[0]) ))
		self.et_chart.set_benchmark_value(route_result.GivenTravelTime)
		self.draw()
		print 'num of nodes:', len(route_result.Nodes)
		print 'num of certainty index:',len(route_result.RouteCertainty)
		print 'num of estimated time:',len(route_result.TraveledTime)
		
		# please change this flag if you want to find data behind the scene
		analysis_flag = True
		
		if analysis_flag:
			file_output = open('link_list_for_analysis.dat','w')
			#output_str = ('Predict [%f %f] - [%f %f] of %s\n==================================\n' % (self.from_longitude, self.from_latitude, 
			#						self.to_longitude, self.to_latitude, self.date_to_predict))
			#file_output.write(output_str)
			year = int(self.date_to_predict[0:4])
			month = int(self.date_to_predict[4:6])
			day = int(self.date_to_predict[6:8])
			date_value = datetime(year, month, day)
			vol_index = date_value.weekday()
			link_exist_dict = {}
			count = 0
			for data_item in route_result.NodePath:
				lcd,direction = data_item[0].split('_')
				output_str = ('%s\t%s\t%d\n' % (lcd,direction,vol_index))
				if link_exist_dict.has_key(output_str):
					continue
				file_output.write(output_str)
				link_exist_dict[output_str]=True
				count += 1
			file_output.close()
			print count, 'links are used in computation'
			
'''
'''
	
# sample url
# http://1.maps.nlp.nokia.com.cn/maptile/2.1/maptile/newest/normal.day.grey/13/6748/3108/256/png8?app_id=demo_qCG24t50dHOwrLQ&token=NYKC67ShPhQwqaydGIW4yg&lg=chi

'''




# unit test code

def main():
	print 'Initiate TK windows/framework and commponents ...',
	sys.stdout.flush()
	root_widget = Tk()
	inst = RFUtl(root_widget)
	inst.construct_layout()
	inst.draw()
	print 'done!\nStart to take events ...'
	sys.stdout.flush()
	root_widget.mainloop()

			
if __name__=='__main__':
	main()