#!/usr/bin/python

from Tool import *
from LinkInfo import *
from LinkMatch import *
import math

link_match_obj = LinkMatch()    

class Route:

    ##
    # RouteLInks[(linkID,length,instruction,[lat,long]),(),...]
    # Geo ["latitude","longitude"]
    ##
    Debug=False
    RouteLinks=[]
    PlannedTime="201404090005"
    #Unit is in minute
    TraveledTime=0
    RouteCertainty=0
    RouteLinkInfo=LinkInfo()
    #start point and end point
    GEO0=[]
    GEO1=[]
    Shape=''
    Nodes=[]
    MaxCertainty=5
    
    #route[[shape,links], [...], ...]
    def __init__(self, route, time, geo0,geo1):
        
        self.Shape=route[0]
        self.RouteLinks=route[1]
        self.PlannedTime=time
        self.GEO0=geo0
        self.GEO1=geo1
        self.initRouteSections(self.Shape)
  
    def getDefaultSpeed(self, time_str):
        hh=int(time_str[8:10])
        default_speed=60
        if hh >8 and hh<20 :
            default_speed=30
        return default_speed
        
    def getLinkSpeed(self, linkID, time_str):
        lcd_direction=linkID
        
        speed=30
        
        if lcd_direction != None:
            speed=self.RouteLinkInfo.findLinkSpeed(lcd_direction,time_str)
            if speed == -1:
                Tool.debugStaticMessage(self.Debug,"For Speed LCD is not found by "+linkID[0]+'_'+linkID[1])
                speed = self.getDefaultSpeed(time_str)
        else:
            Tool.debugStaticMessage(self.Debug,"For Speed LCD is not found by "+linkID[0]+'_'+linkID[1])
            speed = self.getDefaultSpeed(time_str)
        return float(speed)
    
    def getDefaultCertainty(self, time_str):
        default_certainty=5
        
        hh=int(time_str[8:10])
        if hh >8 and hh<20 :
            default_certainty=5
        
        return default_certainty
        
    def getLinkCertainty(self, lcd_direction, time_str):
    
  
        certainty=0
        
        if lcd_direction != None:
            certainty=self.RouteLinkInfo.findLinkCertainty(lcd_direction,time_str)
            if certainty == -1:
                #Tool.debugStaticMessage(self.Debug,"For Certainty LCD is not found by "+linkID)
                certainty = self.getDefaultCertainty(time_str)
        else:
            
            certainty = self.getDefaultCertainty(time_str)
            #Tool.debugStaticMessage(self.Debug,"For Certainty LCD is not found by "+linkID)
        return float(certainty)
        
        
    def calculateRoute(self, round_of_cal):
        traveltime=0.00
        certainty=0.00
        linkNo=0
        starttime=self.PlannedTime
        
        last_geo = (float(self.GEO0[0]),float(self.GEO0[1]))
        for link in self.RouteLinks:
            new_geo = link[3]
            if new_geo == None:
                new_geo = (float(self.GEO0[0]),float(self.GEO0[1]))
            lcd_direction = link_match_obj.match(last_geo,new_geo)
            
            link_id=link[0]
            link_length=float(link[1])
            
            if round_of_cal == 0:
                print link_id, last_geo, new_geo, link_length, 'matched to:', lcd_direction
            las_geo = new_geo
            
            nexttime=Tool.getNextTime(starttime, int(traveltime))
            link_speed=self.getLinkSpeed(lcd_direction,nexttime)
            link_certainty=self.getLinkCertainty(lcd_direction,nexttime)
            
            cost=float(link_length*60)/(link_speed*1000)
            
            traveltime =cost+traveltime
            certainty =certainty+link_certainty
            linkNo =linkNo+1
            

        self.TraveledTime=math.ceil(traveltime)
        certainty=float(certainty/(self.MaxCertainty*linkNo))
        self.RouteCertainty=round(certainty,2)

        Tool.debugStaticMessage(self.Debug,"Travel Cost(min): "+str(self.TraveledTime))
        Tool.debugStaticMessage(self.Debug,"Certainty: "+str(self.RouteCertainty))
        
    def initRouteSections(self,shape):
        
        sections=shape.split(',')
        index=0
        end=len(sections)
        while index < end:
            geox=sections[index]
            index +=1
            geoy=sections[index]
            index +=1
            self.Nodes.append([geox,geoy])
    
    def calculateRouteByNodes(self, round_of_cal):
        traveltime=0.00
        certainty=0.00
        linkNo=0
        starttime=self.PlannedTime
        
        index=0
        end=len(self.Nodes)-1
        
        while index < end:
       
            geo_lat=float(self.Nodes[index][0])
            geo_log=float(self.Nodes[index][1])
            geo_start=(geo_lat,geo_log)
            
            index +=1
            
            geo_lat=float(self.Nodes[index][0])
            geo_log=float(self.Nodes[index][1])
            geo_next=(geo_lat,geo_log)
            
            lcd_direction = link_match_obj.match(geo_start,geo_next)
            
            link_length=Tool.coords_to_distance(geo_start,geo_next)
            
            if round_of_cal == 0:
                print geo_next, geo_start, link_length, 'matched to:', lcd_direction

            
            nexttime=Tool.getNextTime(starttime, int(traveltime))
            link_speed=self.getLinkSpeed(lcd_direction,nexttime)
            link_certainty=self.getLinkCertainty(lcd_direction,nexttime)
            
            cost=float(link_length*60)/(link_speed*1000)
            
            traveltime =cost+traveltime
            certainty =certainty+link_certainty
            linkNo =linkNo+1
            

        self.TraveledTime=math.ceil(traveltime)
        certainty=float(certainty/(self.MaxCertainty*linkNo))
        self.RouteCertainty=round(certainty,2)

        Tool.debugStaticMessage(self.Debug,"Travel Cost(min): "+str(self.TraveledTime))
        Tool.debugStaticMessage(self.Debug,"Certainty: "+str(self.RouteCertainty))
        
    def testCalculateRouteByNodes(self):
        self.calculateRouteByNodes(0)
    
    
def main():
    #	Line 1407: 5;1;+1569069816105926780
    shape='39.9867797,116.3580358,39.9869299,116.3586259,39.9871552,116.3654494,39.9874127,116.3741183,39.9874556,116.376425,39.98752,116.3781846,39.9875951,116.3813603,39.9877238,116.3848686,39.9877346,116.3864458,39.9877882,116.3874865,39.9877775,116.3876259,39.9878418,116.3891602,39.9880779,116.3972819,39.9881637,116.3995671,39.9881959,116.4013267,39.9883032,116.4050603,39.9883246,116.4063799,39.9884105,116.408987,39.9884856,116.4122593,39.9885821,116.4149952,39.9886358,116.41698,39.988625,116.4172375,39.9887323,116.4203167,39.9889898,116.4296937,39.9891078,116.434865,39.9891078,116.4373326,39.9890113,116.4380622,39.9889469,116.4383841,39.9886572,116.4394999,39.9883783,116.440326,39.9875951,116.442461,39.9874985,116.4426756,39.9874449,116.4428473,39.9859965,116.4465487,39.985739,116.447171,39.9854815,116.447686,39.984988,116.448555,39.9839365,116.4501321'
    
    shape='39.9891078,116.434865,39.9891078,116.4373326'
    route=Route([shape,[('+1569069816105926780','549','long road',['39.1','116.1'])]], '201404090000', ['39.1','116.1'],['39.1','116.1'])
    route.testCalculateRouteByNodes()
    

if __name__=='__main__':
    main()
