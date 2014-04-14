#!/usr/bin/python

import sys
import json
import httplib
from Route import *
from Tool import *
import urllib 
import urllib2

class KPRouteMain:

    #Server_Address="route.nlp.nokia.com.cn"
    Server_Address="211.151.53.78"
    Debug=False

    #GEO "latitude","longitude"
    def listRoutes(self, geo1,geo2):
        conn=httplib.HTTPConnection(self.Server_Address)
        headers={'accept':'application/json'}
        uri="/routing/7.2/calculateroute.json?routeattributes=wp,sm,lg&maneuverattributes=ac,po,tt,le,li&linkattributes=sh&legattributes=sh&jsonAttributes=41&verboseMode=5&metricSystem=metric&alternatives=2&waypoint0=geo!"+geo1[0]+","+geo1[1]+"&waypoint1=geo!"+geo2[0]+","+geo2[1]+"&language=zh_CN&mode=fastest;car;traffic:disabled;&app_id=90oGXsXHT8IRMSt5D79X&token=JY0BReev8ax1gIrHZZoqIg"

        Tool.debugStaticMessage(self.Debug,"/routing/7.2/calculateroute.json?"+uri)
        

        uri ='http://'+self.Server_Address+uri
        req = urllib2.Request(uri)
        req.add_header('accept', 'application/json')
        
        response = urllib2.urlopen(req)
        
        r=response.getcode()
        if r != 200 :
            conn.close()
            Tool.errorLog(str(r))
            Tool.errorLog(" "+uri+"\n")
            raise Exception("Cannot get routes by HTTP RestAPI")
            
        content = json.loads(response.read())
        
        routes_txt=content["response"]["route"]

        ## parse links info
        routes=[]
        for one_route in routes_txt:
            links=[]
            shape=''
            for leg in one_route["leg"]:
            
                shape=leg['shape']
                break
            
            routes.append(shape)
            
            Tool.debugStaticMessage(self.Debug,"\nShape is:\n "+ str(shape))
            
            #only get one route
            break            
            
        return routes
    
    
    #planned_date= yyyymmdd
    #return Route list object
    def get24HrRoutes(self,geo0,geo1,planned_date):
        
        route24Hr=[]
        init_routes_info=self.listRoutes(geo0,geo1)

        for route in init_routes_info:
            
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
                
                planned_time=planned_date+hh_str+mm_str
                route_info=RouteOneDay(route,planned_time,geo0,geo1)
                route_info.calculateRouteByNodes()
                route24Hr.append(route_info);
                index +=step
            
            # ******   Attention ********
            # only select the first route
            break
        
        return route24Hr
    

#########################################################

    def testGet24HrRoutes(self):
        
        #"latitude":39.8909098,"longitude":116.4616548
        #"latitude":39.9453306,"longitude":116.4166836
  
        start_geoX="39.9515592744"
        start_geoY="116.41934259"
        end_geoX="39.9992530"
        end_geoY="116.4744977"
        planned_date="20140705"
        
        routes=self.get24HrRoutes([start_geoX,start_geoY],[end_geoX,end_geoY],planned_date)
        
        print '***********************************************************'
        separator_str='|'
        for route in routes:
            output_str=route.PlannedTime +separator_str
            output_str +=str(route.TraveledTime) + separator_str
            output_str +=str(route.RouteCertainty) + separator_str
            output_str +=str(route.GEO0) + separator_str
            output_str +=str(route.GEO1)
            output_str +='\nLinks Info:'
            output_str +=str(len(route.RouteLinks)) +' links \n'
            Tool.results2Log(output_str)
            
            
            output_str=''            
            for link in route.RouteLinks:
                output_str +=link[2]+ separator_str
                output_str += str(link[3])
                output_str +='\n'
                
            Tool.results2Log(output_str)
            Tool.results2Log('\n')
        
        
    def testGetRoutes(self):
    
        start_geoX="39.9515592744"
        start_geoY="116.41934259"
        end_geoX="39.9992530"
        end_geoY="116.4744977"
        planned_time="201404090000"
        
        self.getRoutes([start_geoX,start_geoY],[end_geoX,end_geoY],planned_time)
    
    def testPos2Link(self, filename):
        
        self.pos2Link(filename)
        
    def testListRoutes(self):
    
        start_geoX="39.871990"
        start_geoY="116.433120"
        end_geoX="39.871680"
        end_geoY="116.439420"
        
        start_geoX="39.9515592744"
        start_geoY="116.41934259"
        end_geoX="39.9992530"
        end_geoY="116.4744977"
        
        routes=self.listRoutes([start_geoX,start_geoY],[end_geoX,end_geoY])
        
        Tool.results2Log(str(routes[0]))
        
        
###############################################################
#


def main():


    my_route=KPRouteMain()
    
    #my_route.testGetRoutes()
    
    my_route.testGet24HrRoutes()

    #my_route.testPos2Link(sys.argv[1])
    
    #my_route.testListRoutes()
    


if __name__=='__main__':
    main()
