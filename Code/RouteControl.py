#!/usr/bin/python

import sys
import json
from Tool import *
from RouteSession import *
from AdRoute import *
from RTTraffic import * 

class RouteControl:

    RealTraffic=''
    Debug=False
    def reportPos(self, pos, routeSession):

        self.RealTraffic=RTTraffic()
         
        adRoute=routeSession.RouteObj
        geoList=routeSession.PassedPos
        passedIndex=routeSession.PassedIndex
        
        index=self.nearestPath(pos,adRoute.NodePath,passedIndex)
        
        if index<0:
            #not found current position in the route path
            #either need to recalculate or need to trigger new event to collect new position
            print 'not found nearest path'
            return -1
            
        routeSession.setPassedIndex(index)
        routeSession.PassedPos.append(pos)
        
        found=self.checkSpeedAfterIndex(adRoute,index,10, 45, 20,10)
        
        if found>0:
            #found incident
            print 'find speed is not normal or incident at path ', found
            return found
        
        return 0
        
    def checkSpeedAfterIndex(self,adRoute, passedIndex, from_mins, to_mins, mini_len, mini_speed):
        traveltime=0        
        end=len(adRoute.NodePath)
        now=Tool.getNow()
        index=passedIndex
        found=-1
        
        while index < end:
            node=adRoute.NodePath[index]
            lcd_direction=node[0]
            link_length=node[1]
            nexttime=Tool.getNextTime(now, int(traveltime))
            
            link_speed=adRoute.getLinkSpeed(lcd_direction,nexttime)
            
            cost=float(link_length*60)/(link_speed*1000)
            PANEL_FACTOR = 100
            cost += (float(PANEL_FACTOR)/(link_speed ** 2)) 
            
            traveltime=cost+traveltime
            
            if traveltime>from_mins and traveltime < to_mins:
                real_speed=self.getLinkRealSpeed(lcd_direction,nexttime)
                #detected incident and need to report
                if self.Debug:
                    print lcd_direction, real_speed, link_speed, link_length, traveltime
                if real_speed < link_speed and real_speed < float(mini_speed) and link_length > mini_len: 
                    print 'founded ', lcd_direction, real_speed, link_speed, link_length, traveltime
                    found=index
                    break
            elif traveltime > to_mins:
                break
                
            index +=1
            
        return found
        
    #geo[lat,log]
    #nodePath[[lcd_direction,length], [], ...]
    def nearestPath(self, geo, nodePath, passedIndex):
        index=passedIndex
        found=-1
        end=len(nodePath)
        while index < end:
            node =nodePath[index]
            
            path_len=node[1]
            geo_start=node[2]
            geo_next=node[3]
            
            geo_middle=Tool.middlepoint(geo_start,geo_next)
            pos2ceter_len=Tool.coords_to_distance(geo,geo_middle)
            
            path_len= path_len/2+10
            if path_len>pos2ceter_len :
                found=index
                break
            
            index +=1
        
        return found
    
    
    def getLinkRealSpeed(self,lcd_direction,nexttime):
        speed=self.RealTraffic.TrafficData.get(lcd_direction)
        if speed == None or not speed :
            value=self.getDefaultSpeed(nexttime)
        else:
            value=speed[1]
        return float(value)
        
    def getDefaultSpeed(self, time_str):
        hh=int(time_str[8:10])
        default_speed=60
        if hh >8 and hh<20 :
            default_speed=30
        return default_speed    
    
    def getIncident(self,lcd_direction):
        incidents=[]
        for inc in self.RealTraffic.IncidentData:
            result=inc[0].find(lcd_direction)
            if result != -1:
                incidents.append(inc)
        
        return incidents
        
def main():

    routeCtrl=RouteControl()
    routeCtrl.RealTraffic=RTTraffic()
    #print routeCtrl.getLinkRealSpeed('10_1', '201405270905')
    #print routeCtrl.getIncident('1124_0')
    
    shape=[39.9515573, 116.4195518, 39.9510098, 116.4195442, 39.950881, 116.4195549, 39.9508703, 116.4195764, 39.9508917, 116.4213252, 39.9509132, 116.4223123, 39.9503446, 116.4223123, 39.9502909, 116.4223123, 39.9502051, 116.4223123, 39.9502265, 116.4229453, 39.9502587, 116.4238572, 39.9502695, 116.4242542, 39.9503446, 116.4251876, 39.9503446, 116.4252841, 39.9502695, 116.4252949, 39.9499583, 116.4252949, 39.9497652, 116.4253056, 39.9494112, 116.42537, 39.9494541, 116.4268291, 39.9494863, 116.4279878, 39.9495399, 116.4280951, 39.9495614, 116.4281809, 39.9495828, 116.4297259, 39.9496043, 116.4297795, 39.949615, 116.4299834, 39.949615, 116.4307451, 39.9495828, 116.4310563, 39.9494863, 116.431582, 39.9491644, 116.4325905, 39.9491322, 116.4328587, 39.9491751, 116.433202, 39.9493146, 116.4336419, 39.949379, 116.4339209, 39.9494541, 116.4343822, 39.9494648, 116.4345431, 39.9494541, 116.4349401, 39.9494648, 116.4363992, 39.949379, 116.4425576, 39.9493897, 116.4436948, 39.9494326, 116.4442742, 39.9495184, 116.4447677, 39.9496257, 116.445111, 39.9498403, 116.4456046, 39.9499691, 116.4458621, 39.9502051, 116.4461946, 39.9505699, 116.4466345, 39.9516642, 116.4477718, 39.9523079, 116.4485013, 39.9540782, 116.4504433, 39.9547219, 116.4511836, 39.9555588, 116.4520955, 39.9572861, 116.4540374, 39.9578869, 116.4546812, 39.9581552, 116.4549816, 39.9581981, 116.4550674, 39.9582517, 116.4552176, 39.9582624, 116.4553893, 39.958241, 116.4555287, 39.9581444, 116.455754, 39.958005, 116.4558613, 39.9579406, 116.4558828, 39.9577904, 116.4558828, 39.9576616, 116.4558184, 39.9575651, 116.4557326, 39.9575007, 116.4556146, 39.9574578, 116.4554429, 39.9574471, 116.4551747, 39.9574792, 116.4550352, 39.9579298, 116.4543486, 39.9579835, 116.4542842, 39.9580371, 116.454252, 39.9581659, 116.4541769, 39.9581981, 116.4541662, 39.9582732, 116.4541769, 39.958359, 116.4542413, 39.9588311, 116.4547563, 39.9599683, 116.4560544, 39.9609339, 116.4570951, 39.9611807, 116.4573848, 39.9616957, 116.4578998, 39.9618137, 116.4579749, 39.9618781, 116.4579856, 39.9638629, 116.460228, 39.9668133, 116.4634681, 39.967972, 116.464777, 39.9692166, 116.4661396, 39.9693346, 116.4662898, 39.9697423, 116.4667082, 39.9705148, 116.4675772, 39.9728215, 116.4700985, 39.9728751, 116.4701736, 39.9729609, 116.4702487, 39.9734008, 116.4707637, 39.9742591, 116.4717185, 39.9746776, 116.4721584, 39.9757719, 116.473403, 39.9762332, 116.473875, 39.9762654, 116.4739287, 39.977349, 116.4750981, 39.9782181, 116.4760637, 39.9783146, 116.4761388, 39.9800634, 116.4781344, 39.9802244, 116.4782953, 39.9842906, 116.48278, 39.9862754, 116.4849901, 39.9866617, 116.4853978, 39.9881637, 116.4870715, 39.9887967, 116.4878118, 39.9889898, 116.4880157, 39.9890649, 116.4880908, 39.9905348, 116.4857841, 39.9912214, 116.4847541, 39.9919403, 116.4836597, 39.9925196, 116.4827478, 39.992584, 116.4826727, 39.9936354, 116.4810526, 39.9962962, 116.4770508, 39.9963713, 116.4769542, 39.9969292, 116.4760423, 39.9971867, 116.4756668, 39.9974549, 116.4753127, 39.998678, 116.4734352, 39.9987209, 116.4733815, 39.9987531, 116.4734352, 39.9987853, 116.4734566, 39.999311, 116.4740467, 39.9992681, 116.4741004, 39.9991023, 116.4743121]
    
 
    route=RouteOneDay((shape, [], 10),['39.1','116.1'],['39.1','116.1'], '20140409')
    #print routeCtrl.nearestPath([39.950881, 116.4195549], route.NodePath,0 )
    
    print routeCtrl.checkSpeedAfterIndex(route,0, 2, 25, 10, 5)
    
if __name__=='__main__':
    main()