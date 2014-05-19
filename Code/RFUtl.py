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

MAP_AREA_SIZE = (1600,900)
WINDOWS_SIZE = (1600,900)

PROGRAM_TITLE = '行程规划V1.0'
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
		
		# spot geo
		self.from_latitude = 39.9515592744
		self.from_longitude = 116.41934259
		self.to_latitude = 39.9992530
		self.to_longitude = 116.4744977
		self.basemap.add_spot((self.from_longitude, self.from_latitude), 10, '始')
		self.basemap.add_spot((self.to_longitude, self.to_latitude), 10, '终')
		
		# pannel
		self.pannel_obj = RFPannel(PANEL_WIDTH,PANEL_HEIGHT)
		
		# chart
		self.tta_chart = RFBaseChart(350,250)
		self.ci_chart = RFBaseChart(350,250,True)
		
		# date
		self.date = '2014-06-20'
		self.selected_time_slot = 8 * 12
				

		
		# tta and ci
		self.departure_time = '13:00'
		self.ci_value = 0.8
		
		# compute result
		self.tta_array = []
		self.ci_array = []
		self.path_array = []
		

		
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

		
	def draw(self):
		self.map_canvas.delete(ALL)
		self.basemap.draw(self.map_canvas, self.path_array)
		
		self.map_canvas.create_image(1400,450, image = self.pannel_obj.get_static_photo())
		self.pannel_obj.set_data()
		self.map_canvas.create_image(1400,450, image = self.pannel_obj.get_dynamic_photo())
		
		value_array = []
		for i in range(0,288):
			value_array.append(i)
		self.tta_chart.set_data(value_array)
		self.ci_chart.set_data(value_array)

		self.map_canvas.create_image(1400,450, image = self.tta_chart.get_static_photo())
		self.map_canvas.create_image(1400,690, image = self.ci_chart.get_static_photo())
		self.map_canvas.create_image(1400,450, image = self.tta_chart.get_dynamic_photo())
		self.map_canvas.create_image(1400,690, image = self.ci_chart.get_dynamic_photo())
'''
	def set_value(self):
		self.from_longitude, self.from_latitude = self.basemap.hot_spots[0][1]
		self.to_longitude, self.to_latitude = self.basemap.hot_spots[1][1]
		self.center_longitude,self.center_latitude = self.basemap.center_coords
		
		self.from_input_lat.delete(0,END)
		self.from_input_lat.insert(0,str(self.from_latitude))
		self.from_input_lon.delete(0,END)
		self.from_input_lon.insert(0,str(self.from_longitude))
		self.to_input_lat.delete(0,END)
		self.to_input_lat.insert(0,str(self.to_latitude))
		self.to_input_lon.delete(0,END)
		self.to_input_lon.insert(0,str(self.to_longitude))
		self.center_input_lat.delete(0,END)
		self.center_input_lat.insert(0,str(self.center_latitude))
		self.center_input_lon.delete(0,END)
		self.center_input_lon.insert(0,str(self.center_longitude))
		self.date_input.delete(0,END)
		self.date_input.insert(0,self.date_to_predict)
		self.week_day_input.delete(0,END)
		self.week_day_input.insert(0,WEEK_DAY_TEXT[self.vol_of_the_day])
		self.zoom_level_slider.set(self.zoom_level)

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