#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is a lib file for Kao Pu Routing program 
# Created in 2014
# ######################################################################
from Tkinter import *
import tkFileDialog
from BaseMap import *
from KPRouteMain import *
from KaoPuBaseChart import *

WINDOWS_SIZE = (1024,768)
MAP_AREA_SIZE = (670,740)
PLANNING_AREA_SIZE = (340,760)
ZOOM_AREA_SIZE = (40,180)
INPUT_AREA_SIZE = (280,160)
ESTIMATED_TIME_DIAGRAM_SIZE = (320,240)
KAOPU_DIAGRAM_SIZE = (320,240)

INPUT_WIDTH = 15

PROGRAM_TITLE = '靠谱行程规划V1.0'
MAP_AREA_TITLE = '地图'
PLANNING_AREA_TITLE = '规划行程'
INPUT_AREA_TITLE = '输入参数'
RESULT_AREA_TITLE = '预计行驶时间'
KAOPU_AREA_TITLE = '靠谱指数'
ZOOM_AREA_TITLE = '图层'

POS_TEXT = '位置'
LAT_TEXT = '纬度:'
LON_TEXT = '经度:'
PA_TEXT = '起点'
PB_TEXT = '终点'
MAP_TEXT = '地图'
OPTION_TEXT = '选项'

DATE_TEXT = '日期'
ROUTE_BUTTON_TEXT = '预测'

ST_TEXT = '时间段'
ET_TEXT = '预计行使时间'
CI_TEXT = '准点到达风险'

CB_ARRIVAL_TEXT = "依据到达时间"

RISK_TEXT_5 = '超大风险'
RISK_TEXT_4 = '较大风险'
RISK_TEXT_3 = '有些风险'
RISK_TEXT_2 = '微小风险'
RISK_TEXT_1 = '无风险'

PAD_X = 2
PAD_Y = 2

DIAGRAM_ZERO = (20,20)

class KaoPuTKUtl:
	def __init__(self, root_widget):
		self.widget = root_widget
		self.from_latitude = 39.9515592744
		self.from_longitude = 116.41934259
		self.to_latitude = 39.9992530
		self.to_longitude = 116.4744977
		self.center_latitude = 39.9065759877
		self.center_longitude = 116.399459839
		self.zoom_level = 12
		self.ci_value = 5
		self.selected_slot = 8 * 12
		self.is_arrival_oriented_on = False
		self.date_to_predict = '20140705'
		
		self.estimated_time_array = []
		self.ci_array = []
		
		self.path_array = []
		
		print 'Initiate map view ...',
		self.basemap = BaseMap(MAP_AREA_SIZE,256, [self.center_longitude,self.center_latitude])
		self.basemap.add_spot((self.from_longitude, self.from_latitude), 10, '始')
		self.basemap.add_spot((self.to_longitude, self.to_latitude), 10, '终')
		print 'done!'
		
		print 'Initiate RouteMain ...',
		self.route_obj = KPRouteMain()
		print 'done!'

		
							
	def draw_point_with_Label(self, canvas, pos, r, txt):
		the_circle = canvas.create_oval([pos[0]-r,pos[1]-r,pos[0]+r,pos[1]+r],fill='blue')
		canvas.create_text(pos[0],pos[1],text=txt, fill='white')
		return the_circle
	
	def construct_layout(self):
		
		# resize window and add title
		geometry_msg = ('%dx%d' % WINDOWS_SIZE)
		self.widget.geometry(geometry_msg)
		self.widget.title(PROGRAM_TITLE)
		
		# initiate all frames
		self.map_frame = LabelFrame(self.widget, text = MAP_AREA_TITLE, padx = PAD_X, pady = PAD_Y)
		self.planning_frame = LabelFrame(self.widget, text = PLANNING_AREA_TITLE, padx = PAD_X, pady = PAD_Y)
		
		self.control_frame = Frame(self.planning_frame,padx = PAD_X, pady = PAD_Y)
		self.input_frame = LabelFrame(self.control_frame, text = INPUT_AREA_TITLE, padx = PAD_X, pady = PAD_Y)
		self.zoom_frame = LabelFrame(self.control_frame, text = ZOOM_AREA_TITLE, padx = PAD_X, pady = PAD_Y)
		
		self.et_frame = LabelFrame(self.planning_frame, text = RESULT_AREA_TITLE, padx = PAD_X, pady = PAD_Y)
		self.ci_frame = LabelFrame(self.planning_frame, text = KAOPU_AREA_TITLE, padx = PAD_X, pady = PAD_Y)
		
		# add controls into frames
		self.map_canvas = Canvas(self.map_frame, width = MAP_AREA_SIZE[0], height = MAP_AREA_SIZE[1])
		self.et_canvas = Canvas(self.et_frame, width = ESTIMATED_TIME_DIAGRAM_SIZE[0], height = ESTIMATED_TIME_DIAGRAM_SIZE[1])
		self.ci_canvas = Canvas(self.ci_frame, width = KAOPU_DIAGRAM_SIZE[0], height = KAOPU_DIAGRAM_SIZE[1])

		self.zoom_level_slider = Scale(self.zoom_frame, from_ = 3, to = 20, orient = VERTICAL, length = ZOOM_AREA_SIZE[1] - 10, sliderlength=15, width = 20, resolution = 1)
		
		self.line1_label_pos = Label(self.input_frame, text = POS_TEXT)
		self.line1_label_lat = Label(self.input_frame, text = LAT_TEXT)
		self.line1_label_lon = Label(self.input_frame, text = LON_TEXT)
		
		self.from_label = Label(self.input_frame, text = PA_TEXT)
		self.to_label = Label(self.input_frame, text = PB_TEXT)
		self.center_label = Label(self.input_frame, text = MAP_TEXT)
		self.date_label = Label(self.input_frame, text = DATE_TEXT)
		self.selected_timeslot_label = Label(self.input_frame, text = ST_TEXT)
		self.estimated_time_label = Label(self.input_frame, text = ET_TEXT)
		self.ci_result_label = Label(self.input_frame, text = CI_TEXT)
		self.option_label = Label(self.input_frame, text = OPTION_TEXT)
		
		self.from_input_lat = Entry(self.input_frame, width = INPUT_WIDTH)
		self.from_input_lon = Entry(self.input_frame, width = INPUT_WIDTH)
		self.to_input_lat = Entry(self.input_frame, width = INPUT_WIDTH)
		self.to_input_lon = Entry(self.input_frame, width = INPUT_WIDTH)
		self.center_input_lat = Entry(self.input_frame, width = INPUT_WIDTH)
		self.center_input_lon = Entry(self.input_frame, width = INPUT_WIDTH)
		self.date_input = Entry(self.input_frame, width = INPUT_WIDTH)
		self.selected_timeslot_input = Entry(self.input_frame, width = 5)
		self.estimated_time_input = Entry(self.input_frame, width = INPUT_WIDTH)
		self.ci_result_input = Entry(self.input_frame, width = INPUT_WIDTH)

		self.is_arrival_oriented_cb = Checkbutton(self.input_frame, text=CB_ARRIVAL_TEXT, variable=self.is_arrival_oriented_on)
		
		self.route_button = Button(self.input_frame, text=ROUTE_BUTTON_TEXT, width=INPUT_WIDTH)

		# set initial value
		self.set_value()
		
		# bind events
		self.map_canvas.bind("<Button-1>", self.handler_b1_down)
		self.map_canvas.bind("<B1-Motion>", self.handler_b1_move)
		self.map_canvas.bind("<ButtonRelease-1>", self.handler_b1_release)

		self.et_canvas.bind("<Button-1>", self.handler_change_slot)
		self.et_canvas.bind("<B1-Motion>", self.handler_change_slot)
		self.et_canvas.bind("<ButtonRelease-1>", self.handler_change_slot)

		self.ci_canvas.bind("<Button-1>", self.handler_change_slot)
		self.ci_canvas.bind("<B1-Motion>", self.handler_change_slot)
		self.ci_canvas.bind("<ButtonRelease-1>", self.handler_change_slot)
		
		self.zoom_level_slider.bind("<ButtonRelease-1>", self.handler_value_update)
		self.from_input_lon.bind("<FocusOut>", self.handler_value_update)
		self.from_input_lat.bind("<FocusOut>", self.handler_value_update)
		self.to_input_lon.bind("<FocusOut>", self.handler_value_update)
		self.to_input_lat.bind("<FocusOut>", self.handler_value_update)
		self.center_input_lon.bind("<FocusOut>", self.handler_value_update)
		self.center_input_lat.bind("<FocusOut>", self.handler_value_update)
		self.date_input.bind("<FocusOut>", self.handler_value_update)
		
		self.route_button.bind("<ButtonRelease-1>", self.handler_predict)
		
		self.ci_chart = KaoPuBaseChart(self.ci_canvas, KAOPU_DIAGRAM_SIZE[0],KAOPU_DIAGRAM_SIZE[1])
		self.et_chart = KaoPuBaseChart(self.et_canvas, ESTIMATED_TIME_DIAGRAM_SIZE[0],ESTIMATED_TIME_DIAGRAM_SIZE[1])

		# arrange all controls into right place
		self.map_frame.grid(row = 0, column = 0)
		self.planning_frame.grid(row = 0, column = 1)

		self.control_frame.grid(row = 0, column = 0)
		self.et_frame.grid(row = 1, column = 0)
		self.ci_frame.grid(row = 2, column = 0)

		self.zoom_frame.grid(row = 0,column = 0)
		self.input_frame.grid(row = 0, column = 1)
		
		self.line1_label_pos.grid(row = 0, column = 0)
		self.line1_label_lat.grid(row = 0, column = 1)
		self.line1_label_lon.grid(row = 0, column = 2)
		
		self.from_label.grid(row = 1, column = 0, sticky=E)
		self.to_label.grid(row = 2, column = 0, sticky=E)
		self.center_label.grid(row = 3, column = 0, sticky=E)
		self.date_label.grid(row = 4, column = 0, sticky=E)
		
		self.from_input_lat.grid(row = 1, column = 1)
		self.from_input_lon.grid(row = 1, column = 2)
		self.to_input_lat.grid(row = 2, column = 1)
		self.to_input_lon.grid(row = 2, column = 2)
		self.center_input_lat.grid(row = 3, column = 1)
		self.center_input_lon.grid(row = 3, column = 2)
		
		self.date_input.grid(row = 4, column = 1)
		self.route_button.grid(row = 4, column = 2)

		self.option_label.grid(row = 5, column = 0)
		self.is_arrival_oriented_cb.grid(row = 5, column = 1)

		self.option_label.grid(row = 6, column = 0)
		self.estimated_time_label.grid(row = 6, column = 1)
		self.ci_result_label.grid(row = 6, column = 2)
		
		self.selected_timeslot_input.grid(row = 7, column = 0)
		self.estimated_time_input.grid(row = 7, column = 1)
		self.ci_result_input.grid(row = 7, column = 2)
		
		
		self.zoom_level_slider.grid(row = 0, column = 0)
		
	def draw(self):
		self.map_canvas.pack()
		self.et_canvas.pack()
		self.ci_canvas.pack()
		
		self.basemap.draw(self.map_canvas, self.path_array)
		
		self.ci_chart.set_value_array(self.ci_array)
		self.ci_chart.draw()
		
		self.et_chart.set_value_array(self.estimated_time_array)
		self.et_chart.draw()
		
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
		self.zoom_level_slider.set(self.zoom_level)

	def update_value(self):
		self.from_latitude = float(self.from_input_lat.get())
		self.from_longitude = float(self.from_input_lon.get())
		self.to_latitude = float(self.to_input_lat.get())
		self.to_longitude = float(self.to_input_lon.get())
		self.center_latitude = float(self.center_input_lat.get())
		self.center_longitude = float(self.center_input_lon.get())
		self.date_to_predict = self.date_input.get()
		
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
		self.draw()
		print 'num of nodes:', len(route_result.Nodes)
		print 'num of certainty index:',len(route_result.RouteCertainty)
		print 'num of estimated time:',len(route_result.TraveledTime)
'''
	
# sample url
# http://1.maps.nlp.nokia.com.cn/maptile/2.1/maptile/newest/normal.day.grey/13/6748/3108/256/png8?app_id=demo_qCG24t50dHOwrLQ&token=NYKC67ShPhQwqaydGIW4yg&lg=chi

'''




# unit test code

def main():
	root_widget = Tk()
	inst = KaoPuTKUtl(root_widget)
	inst.construct_layout()
	inst.draw()
	root_widget.mainloop()

			
if __name__=='__main__':
	main()