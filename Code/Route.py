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
    MaxCertainty=5
    def __init__(self, route, time, geo0,geo1):
        self.RouteLinks=route
        self.PlannedTime=time
        self.GEO0=geo0
        self.GEO1=geo1
    
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
                new_geo = (float(self.GEO0[1]),float(self.GEO0[1]))
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
        
    def printRoute(self):
        print "end"

    
    def testGetLinkCertainty(self):
        self.getLinkCertainty('+1569069816105926780')
    
def main():
    #	Line 1407: 5;1;+1569069816105926780
    route=Route(['+1569069816105926780','549','long road',['39.1','116.1']], '201404090000', ['39.1','116.1'],['39.1','116.1'])
    route.testGetLinkCertainty()
    

if __name__=='__main__':
    main()
