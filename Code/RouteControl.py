#!/usr/bin/python

import sys
import json
from Tool import *
from RouteSession import *
from AdRoute import *

class RouteControl:

    def reportPos(self, pos, routeSession):

        adRoute=routeSession.RouteObj
        geoList=routeSession.PassedGeos
        passedIndex=routeSession.PassedIndex
        
        index=self.nearestPath(pos,adRoute.NodePath,passedIndex)
        
        if(index<0):
            #not found current position in the route path
            #either need to recalculate or need to trigger new event to collect new position
            return -1
            
        routeSession.setPassedIndex(index)
        routeSession.appendPos(pos)
        
        found=self.checkSpeedAfterIndex(adRoute,index,10, 50,10)
        
        if(found>0):
            #found incident
            return found
        
        return 0
        
    def checkSpeedAfterIndex(self,adRoute, passedIndex, aftermins, min_len, min_speed):
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
            
            if(traveltime>aftermins):
                real_speed=adRoute.getLinkRealSpeed(lcd_direction,nexttime)
                if(real_speed<link_speed and link_length > min_len and real_speed < min_speed)
                    #detected incident and need to report
                        found=index
                        break
                            
            index +=1    
        return found
        
    #geo[lat,log]
    #nodePath[[lcd_direction,length], [], ...]
    def nearestPath(self, geo, nodePath, passedIndex):
        index=passedIndex
        found=-1
        end=len(self.NodePath)
        while index < end:
            node =NodePath[index]
            
            path_len=node[1]
            geo_start=node[2]
            geo_next=node[3]
            
            geo_middle=Tool.middlepointS(geo_start,geo_next)
            pos2ceter_len=Tool.coords_to_distance(geo,geo_middle)
            
            path_len= path_len/2
            if(path_len>pos2ceter_len):
                found=index
                break
            
            index +=1
        
        return found
        
def main():

    routeCtrl=RouteControl()


if __name__=='__main__':
    main()