#!/usr/bin/python
#coding: utf-8

# ######################################################################
# This file is a lib file for Kao Pu Routing program 
# Created in 2014
# ######################################################################
from Tkinter import *
import tkFileDialog
from BaseMap import *
from RoutesMain import *
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
		
		self.basemap = BaseMap(MAP_AREA_SIZE,256, [self.center_longitude,self.center_latitude])
		self.basemap.add_spot((self.from_longitude, self.from_latitude), 10, '始')
		self.basemap.add_spot((self.to_longitude, self.to_latitude), 10, '终')
		
		self.route_obj = RoutesMain()

		
							
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
		
		#path_a = [39.9515573,116.4195518,39.9510098,116.4195442,39.950881,116.4195549,39.9508703,116.4195764,39.9508917,116.4213252,39.9509132,116.4223123,39.9503446,116.4223123,39.9502909,116.4223123,39.9502051,116.4223123,39.9502265,116.4229453,39.9502587,116.4238572,39.9502695,116.4242542,39.9503446,116.4251876,39.9503446,116.4252841,39.9502695,116.4252949,39.9499583,116.4252949,39.9497652,116.4253056,39.9494112,116.42537,39.9494541,116.4268291,39.9494863,116.4279878,39.9495399,116.4280951,39.9495614,116.4281809,39.9495828,116.4297259,39.9496043,116.4297795,39.949615,116.4299834,39.949615,116.4307451,39.9495828,116.4310563,39.9494863,116.431582,39.9491644,116.4325905,39.9491322,116.4328587,39.9491751,116.433202,39.9493146,116.4336419,39.949379,116.4339209,39.9494541,116.4343822,39.9494648,116.4345431,39.9494541,116.4349401,39.9494648,116.4363992,39.949379,116.4425576,39.9493897,116.4436948,39.9494326,116.4442742,39.9495184,116.4447677,39.9496257,116.445111,39.9498403,116.4456046,39.9499691,116.4458621,39.9502051,116.4461946,39.9505699,116.4466345,39.9516642,116.4477718,39.9523079,116.4485013,39.9540782,116.4504433,39.9547219,116.4511836,39.9555588,116.4520955,39.9572861,116.4540374,39.9578869,116.4546812,39.9581552,116.4549816,39.9581981,116.4550674,39.9582517,116.4552176,39.9582624,116.4553893,39.958241,116.4555287,39.9581444,116.455754,39.958005,116.4558613,39.9579406,116.4558828,39.9577904,116.4558828,39.9576616,116.4558184,39.9575651,116.4557326,39.9575007,116.4556146,39.9574578,116.4554429,39.9574471,116.4551747,39.9574792,116.4550352,39.9579298,116.4543486,39.9579835,116.4542842,39.9580371,116.454252,39.9581659,116.4541769,39.9581981,116.4541662,39.9582732,116.4541769,39.958359,116.4542413,39.9588311,116.4547563,39.9599683,116.4560544,39.9609339,116.4570951,39.9611807,116.4573848,39.9616957,116.4578998,39.9618137,116.4579749,39.9618781,116.4579856,39.9638629,116.460228,39.9668133,116.4634681,39.967972,116.464777,39.9692166,116.4661396,39.9693346,116.4662898,39.9697423,116.4667082,39.9705148,116.4675772,39.9728215,116.4700985,39.9728751,116.4701736,39.9729609,116.4702487,39.9734008,116.4707637,39.9742591,116.4717185,39.9746776,116.4721584,39.9757719,116.473403,39.9762332,116.473875,39.9762654,116.4739287,39.977349,116.4750981,39.9782181,116.4760637,39.9783146,116.4761388,39.9800634,116.4781344,39.9802244,116.4782953,39.9842906,116.48278,39.9862754,116.4849901,39.9866617,116.4853978,39.9881637,116.4870715,39.9887967,116.4878118,39.9889898,116.4880157,39.9890649,116.4880908,39.9905348,116.4857841,39.9912214,116.4847541,39.9919403,116.4836597,39.9925196,116.4827478,39.992584,116.4826727,39.9936354,116.4810526,39.9962962,116.4770508,39.9963713,116.4769542,39.9969292,116.4760423,39.9971867,116.4756668,39.9974549,116.4753127,39.998678,116.4734352,39.9987209,116.4733815,39.9987531,116.4734352,39.9987853,116.4734566,39.999311,116.4740467,39.9992681,116.4741004,39.9991023,116.4743121]
		#fake_array = []
		#for index in range(0,len(path_a) / 2):
		#	geo = (float(path_a[index * 2 + 1]),float(path_a[index * 2]))
		#	fake_array.append(geo)
		#self.path_array = fake_array
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
				ci_msg = '无风险'
			elif ci_value >=80:
				ci_msg = '微小风险'
			elif ci_value >=70:
				ci_msg = '有些风险'
			elif ci_value >=60:
				ci_msg = '较大风险'
			else:
				ci_msg = '超大风险'
			self.ci_result_input.delete(0,END)
			self.ci_result_input.insert(0,ci_msg)
		self.draw()

	def handler_predict(self,event):
		self.update_value()
		print 'predicting your route in:', self.date_to_predict
		route_result = self.route_obj.get24HrRoutes([str(self.from_latitude),str(self.from_longitude)],
								[str(self.to_latitude), str(self.to_longitude)], self.date_to_predict)
		self.estimated_time_array = []
		self.ci_array = []
		for route_obj in route_result:
			self.estimated_time_array.append(route_obj.TraveledTime)
			self.ci_array.append( route_obj.RouteCertainty * 100)

		# latitude and logitude reverted below in order to work with old class
		self.path_array = []
		self.path_array.append((float(route_result[0].GEO0[1]),float(route_result[0].GEO0[0])))
		for link in route_result[0].RouteLinks:
			geo = link[3]
			if geo != None:
				self.path_array.append(( float(geo[1]),float(geo[0]) ))
		self.path_array.append((float(route_result[0].GEO1[1]),float(route_result[0].GEO1[0])))
		self.draw()
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