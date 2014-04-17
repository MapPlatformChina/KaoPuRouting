#!/usr/bin/python

from Tool import *
from LinkInfo import *
from LinkMatch import *
import math

link_match_obj = LinkMatch()    

class RouteOneDay:

    ##
    # NodePath[(lcd, length),(),...]
    # Geo ["latitude","longitude"]
    ##
    Debug=True
    NodePath=[]
    PlannedTime="201404090005"
    #Unit is in minute
    TraveledTime=[]
    RouteCertainty=[]
    RouteLinkInfo=LinkInfo()
    #start point and end point
    GEO0=[]
    GEO1=[]
    Nodes=[]
    MaxCertainty=5
    SpeedWeek={}
    CertaintyWeek={}
    LinksInstruction={}
    GivenTravelTime=0
    
    def __init__(self, route,geo0,geo1, time):
        
        self.NodePath=[]
        self.TraveledTime=[]
        self.RouteCertainty=[]
        self.GEO0=[]
        self.GEO1=[]
        self.Nodes=[]
        self.SpeedWeek={}
        self.CertaintyWeek={}
        self.LinksInstruction={}
        self.GivenTravelTime=0
        
        self.PlannedTime=time
        self.GEO0=geo0
        self.GEO1=geo1
        self.initRouteSections(route[0])
        self.LinksInstruction=route[1]
        self.GivenTravelTime=int(route[2])/60
        
        print self.GivenTravelTime
        print '--------------Initiate New Route --------------------'
        
    def initRouteSections(self,shape):
        
        sections=shape
        index=0
        end=len(sections)
        while index < end:
            geox=sections[index]
            index +=1
            geoy=sections[index]
            index +=1
            self.Nodes.append((geox,geoy))
        
        index=0
        end=len(self.Nodes)-1
        
        ##
        # generate links path for the route
        ##
        while index < end:
       
            geo_lat=float(self.Nodes[index][0])
            geo_log=float(self.Nodes[index][1])
            geo_start=(geo_lat,geo_log)
            
            index +=1
            
            geo_lat=float(self.Nodes[index][0])
            geo_log=float(self.Nodes[index][1])
            geo_next=(geo_lat,geo_log)
            
            lcd_direction = link_match_obj.match(geo_start,geo_next,True)
            lcd_direction =str(lcd_direction[0])+'_'+str(lcd_direction[1])
            
            link_length=math.ceil(Tool.coords_to_distance(geo_start,geo_next))
            self.NodePath.append((lcd_direction, int(link_length)))
            
            certainty7days=self.RouteLinkInfo.Load7DaysLinkCertainty(lcd_direction)
            self.CertaintyWeek.update({lcd_direction:certainty7days})
            
            speed7days=self.RouteLinkInfo.load7DaysLinkSpeed(lcd_direction)
            self.SpeedWeek.update({lcd_direction:speed7days})
            
            
    def getDefaultSpeed(self, time_str):
        hh=int(time_str[8:10])
        default_speed=60
        if hh >8 and hh<20 :
            default_speed=30
        return default_speed
        
    def getDefaultCertainty(self, time_str):
        default_certainty=5
        
        hh=int(time_str[8:10])
        if hh >8 and hh<20 :
            default_certainty=5
        
        return default_certainty
        
    def getLinkSpeed(self, lcd_direction, time_str):     
        speed_24=self.SpeedWeek.get(lcd_direction)

        if speed_24 == None or not speed_24 :
            return self.getDefaultSpeed(time_str)
        else:
            line=self.SpeedWeek.get(lcd_direction)
            day_index=Tool.getDayofWeek(time_str)
            day_index -=1
            time_index=int(Tool.getTimeIndex(time_str))
            line=line[day_index]
            pos=line.split(' ')
            return float(pos[time_index])

    
    def getLinkCertainty(self, lcd_direction, time_str):
        certainty_24=self.CertaintyWeek.get(lcd_direction)
        
        if certainty_24 == None or not certainty_24 :
            return self.getDefaultCertainty(time_str)
            
        else:
            line=self.CertaintyWeek.get(lcd_direction)
            day_index=Tool.getDayofWeek(time_str)
            day_index -=1
            time_index=int(Tool.getTimeIndex(time_str))
            line=line[day_index]
            pos=line.split(' ')
            return float(pos[time_index])
        
    
    
    def calculateRouteByNodes(self):
        self.TraveledTime=[]
        self.RouteCertainty=[]
       
        index=0
        total= 24*60
        step =5
        while index < total:
            mm=index%60
            hh=index/60
                
            if mm<10:
                mm_str='0'+str(mm)
            else:
                mm_str=str(mm)
                
            if hh<10:
                hh_str='0'+str(hh)
            else:
                hh_str=str(hh)
                
            planned_time=self.PlannedTime+hh_str+mm_str
            
            self.calculateRouteOneTime(planned_time)
            
            index +=step
            
            print "-"+planned_time+"\r",
            
            

    def calculateRouteOneTime(self,planned_time):
    
        traveltime=0
        certainty=0.00
        linkNo=0

        for node in self.NodePath:
        
            lcd_direction=node[0]
            link_length=node[1]
            nexttime=Tool.getNextTime(planned_time, int(traveltime))
            
            link_speed=self.getLinkSpeed(lcd_direction,nexttime)
            link_certainty=self.getLinkCertainty(lcd_direction,nexttime)
            
            cost=float(link_length*60)/(link_speed*1000)
            PANEL_FACTOR = 100
            cost += (float(PANEL_FACTOR)/(link_speed ** 2)) 
            
            traveltime=cost+traveltime
            certainty=certainty+link_certainty
            linkNo =linkNo+1
            
        self.TraveledTime.append(math.ceil(traveltime))
        certainty=float(certainty/(self.MaxCertainty*linkNo))
        self.RouteCertainty.append(round(certainty,2))


        
    def testCalculateRouteByNodes(self):
        self.calculateRouteByNodes()
    
    
def main():
    #	Line 1407: 5;1;+1569069816105926780
    shape=[39.9515573, 116.4195518, 39.9510098, 116.4195442, 39.950881, 116.4195549, 39.9508703, 116.4195764, 39.9508917, 116.4213252, 39.9509132, 116.4223123, 39.9503446, 116.4223123, 39.9502909, 116.4223123, 39.9502051, 116.4223123, 39.9502265, 116.4229453, 39.9502587, 116.4238572, 39.9502695, 116.4242542, 39.9503446, 116.4251876, 39.9503446, 116.4252841, 39.9502695, 116.4252949, 39.9499583, 116.4252949, 39.9497652, 116.4253056, 39.9494112, 116.42537, 39.9494541, 116.4268291, 39.9494863, 116.4279878, 39.9495399, 116.4280951, 39.9495614, 116.4281809, 39.9495828, 116.4297259, 39.9496043, 116.4297795, 39.949615, 116.4299834, 39.949615, 116.4307451, 39.9495828, 116.4310563, 39.9494863, 116.431582, 39.9491644, 116.4325905, 39.9491322, 116.4328587, 39.9491751, 116.433202, 39.9493146, 116.4336419, 39.949379, 116.4339209, 39.9494541, 116.4343822, 39.9494648, 116.4345431, 39.9494541, 116.4349401, 39.9494648, 116.4363992, 39.949379, 116.4425576, 39.9493897, 116.4436948, 39.9494326, 116.4442742, 39.9495184, 116.4447677, 39.9496257, 116.445111, 39.9498403, 116.4456046, 39.9499691, 116.4458621, 39.9502051, 116.4461946, 39.9505699, 116.4466345, 39.9516642, 116.4477718, 39.9523079, 116.4485013, 39.9540782, 116.4504433, 39.9547219, 116.4511836, 39.9555588, 116.4520955, 39.9572861, 116.4540374, 39.9578869, 116.4546812, 39.9581552, 116.4549816, 39.9581981, 116.4550674, 39.9582517, 116.4552176, 39.9582624, 116.4553893, 39.958241, 116.4555287, 39.9581444, 116.455754, 39.958005, 116.4558613, 39.9579406, 116.4558828, 39.9577904, 116.4558828, 39.9576616, 116.4558184, 39.9575651, 116.4557326, 39.9575007, 116.4556146, 39.9574578, 116.4554429, 39.9574471, 116.4551747, 39.9574792, 116.4550352, 39.9579298, 116.4543486, 39.9579835, 116.4542842, 39.9580371, 116.454252, 39.9581659, 116.4541769, 39.9581981, 116.4541662, 39.9582732, 116.4541769, 39.958359, 116.4542413, 39.9588311, 116.4547563, 39.9599683, 116.4560544, 39.9609339, 116.4570951, 39.9611807, 116.4573848, 39.9616957, 116.4578998, 39.9618137, 116.4579749, 39.9618781, 116.4579856, 39.9638629, 116.460228, 39.9668133, 116.4634681, 39.967972, 116.464777, 39.9692166, 116.4661396, 39.9693346, 116.4662898, 39.9697423, 116.4667082, 39.9705148, 116.4675772, 39.9728215, 116.4700985, 39.9728751, 116.4701736, 39.9729609, 116.4702487, 39.9734008, 116.4707637, 39.9742591, 116.4717185, 39.9746776, 116.4721584, 39.9757719, 116.473403, 39.9762332, 116.473875, 39.9762654, 116.4739287, 39.977349, 116.4750981, 39.9782181, 116.4760637, 39.9783146, 116.4761388, 39.9800634, 116.4781344, 39.9802244, 116.4782953, 39.9842906, 116.48278, 39.9862754, 116.4849901, 39.9866617, 116.4853978, 39.9881637, 116.4870715, 39.9887967, 116.4878118, 39.9889898, 116.4880157, 39.9890649, 116.4880908, 39.9905348, 116.4857841, 39.9912214, 116.4847541, 39.9919403, 116.4836597, 39.9925196, 116.4827478, 39.992584, 116.4826727, 39.9936354, 116.4810526, 39.9962962, 116.4770508, 39.9963713, 116.4769542, 39.9969292, 116.4760423, 39.9971867, 116.4756668, 39.9974549, 116.4753127, 39.998678, 116.4734352, 39.9987209, 116.4733815, 39.9987531, 116.4734352, 39.9987853, 116.4734566, 39.999311, 116.4740467, 39.9992681, 116.4741004, 39.9991023, 116.4743121]
    
 
    route=RouteOneDay((shape, [], 10),['39.1','116.1'],['39.1','116.1'], '20140409')
    route.testCalculateRouteByNodes()
    
    print len(route.Nodes)
    #print route.NodePath
    

if __name__=='__main__':
    main()
