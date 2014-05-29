#!/usr/bin/python

import sys
import json
import httplib
from RouteOneDay import *
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
        uri="/routing/7.2/calculateroute.json?routeattributes=wp,sm,lg&maneuverattributes=ac,po,tt,le,li&linkattributes=sh&legattributes=sh&jsonAttributes=41&verboseMode=5&metricSystem=metric&alternatives=2&waypoint0=geo!"+geo1[0]+","+geo1[1]+"&waypoint1=geo!"+geo2[0]+","+geo2[1]+"&language=zh_CN&mode=fastest;car;traffic:disabled;&app_code=5FcMtCOSxk5bQ-iikmqEWw&app_id=_alznH-RjhZ2TRrIhLA9&h=20"

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
                for maneuver in leg["maneuver"]:

                    link_action=maneuver["action"]
                    if link_action == "arrive":
                        break

                    link_length=str(maneuver["length"])
                    link_id=str(maneuver["toLink"])
                    link_instruction=(maneuver["instruction"]).encode('utf-8')
                    pos=maneuver["position"]
                    links.append((link_id,link_length,link_instruction))
                
                #only one leg
            travel_time=one_route['summary']['travelTime']
            routes.append((shape,links,travel_time))
            
            Tool.debugStaticMessage(self.Debug,"\nShape is:\n "+ str(shape))
            
            #only get one route
            break            
            
        return routes
    
    
    #planned_date= yyyymmdd
    #return Route list object
    def get24HrRoutes(self,geo0,geo1,planned_date):

        routes_info=self.listRoutes(geo0,geo1)
        
        for route in routes_info:
            route_result=RouteOneDay(route,geo0,geo1,planned_date)
            route_result.calculateRouteByNodes();
            break
        return route_result
    

#########################################################

    def testGet24HrRoutes(self):
        
        #"latitude":39.8909098,"longitude":116.4616548
        #"latitude":39.9453306,"longitude":116.4166836
  
        start_geoX="39.9515592744"
        start_geoY="116.41934259"
        end_geoX="39.9992530"
        end_geoY="116.4744977"
        planned_date="20140705"
        
        route=self.get24HrRoutes([start_geoX,start_geoY],[end_geoX,end_geoY],planned_date)
        
        print '***********************************************************'
        separator_str='|'
        output_str=route.PlannedTime +'\n' 
        index =0
        while index < len(route.TraveledTime):
            output_str +=str(route.TraveledTime[index]) + separator_str
            output_str +=str(route.RouteCertainty[index]) + '\n' 
            index +=1
            Tool.results2Log(output_str)

        
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
