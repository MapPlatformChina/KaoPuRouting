#!/usr/bin/python

import sys
import json
import httplib
from Route import *
from Tool import *
import urllib 
import urllib2

class RoutesMain:

    #Server_Address="route.nlp.nokia.com.cn"
    Server_Address="211.151.53.78"
    Debug=False

    #GEO "latitude","longitude"
    def listRoutes(self, geo1,geo2):
        conn=httplib.HTTPConnection(self.Server_Address)
        headers={'accept':'application/json'}
        uri="/routing/7.2/calculateroute.json?routeattributes=wp,sm,lg&maneuverattributes=ac,po,tt,le,li&linkattributes=sh&legattributes=sh&jsonAttributes=41&verboseMode=5&metricSystem=metric&alternatives=2&waypoint0=geo!"+geo1[0]+","+geo1[1]+"&waypoint1=geo!"+geo2[0]+","+geo2[1]+"&language=zh_CN&mode=fastest;car;traffic:disabled;&app_id=90oGXsXHT8IRMSt5D79X&token=JY0BReev8ax1gIrHZZoqIg"

        Tool.debugStaticMessage(self.Debug,"/routing/7.2/calculateroute.json?"+uri)
        
        '''
        conn.request("GET", uri,"", headers)
        
        r=conn.getresponse() 
        if r.status != 200 :
            conn.close()
            Tool.errorLog(str(r.status)+" : "+str(r.reason))
            Tool.errorLog(" "+uri+"\n")
            raise Exception("Cannot get routes by HTTP RestAPI")

        content=json.loads(r.read())
        conn.close()
        '''
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
                    geo=[pos["latitude"],pos["longitude"]]
                    links.append((link_id,link_length,link_instruction,geo))
                 
                break   

       
            routes.append([shape,links])
            
            Tool.debugStaticMessage(self.Debug,"\nlinks number is:\n "+str(len(links)))
            Tool.debugStaticMessage(self.Debug,"\nShape is:\n "+ str(shape))
        
        Tool.debugStaticMessage(self.Debug,"route number is : "+ str(len(routes)))
            
            
        return routes
    
    #planned_time= yyyyddmmHHMM
    def getRoutes(self,geo0,geo1,planned_time):
        routeOption=[]
        init_routes_info=self.listRoutes(geo0,geo1)
        
        for route in init_routes_info:
            route_info=Route(route,planned_time,geo0,geo1)
            route_info.calculateRouteByNodes(0)
            routeOption.append(route_info)
        
            
        return routeOption
    
    #planned_date= yyyymmdd
    #return Route list object
    def get24HrRoutes(self,geo0,geo1,planned_date):
        
        route24Hr=[]
        init_routes_info=self.listRoutes(geo0,geo1)

        for route in init_routes_info:
            index=0
            total= 1*60
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
                route_info=Route(route,planned_time,geo0,geo1)
                route_info.calculateRouteByNodes()
                route24Hr.append(route_info);
                index +=step
            
            # ******   Attention ********
            # only select the first route
            break
        
        return route24Hr
    
    def pos2Link(self, name):
        f=open('../res/'+name+'.txt','r')
        f_log=open('../log_'+name+'.txt','w')
        f_linkid_lcd=open('../lcd_'+name+'.txt','w')
        

        while True:
            # read lcd positions and try to get all the links for one lcd
            line=f.readline();
            if not line: break
            
            pos=line.split(';')
            #lcd_start-lcd_end-direction, used to identify the specific line in the file
            lcd_start=Tool.refineString(str(pos[2]))
            lcd_end=Tool.refineString(str(pos[3]))
            direction=Tool.refineString(str(pos[4]))
            
            lcd= lcd_start+"-"+lcd_end+"-"+direction
            
            #it is used for generating output file
            #lcd_end;direction
            lcd_output=lcd_end+";"+direction
            geo0=[Tool.refineString(str(pos[8])),Tool.refineString(str(pos[9]))]
            geo1=[Tool.refineString(str(pos[10])),Tool.refineString(str(pos[11]))]
            

            try:
                ##
                ## need to check the f pointed file structure
                ###
                init_routes_info=self.listRoutes(geo0,geo1)
            except Exception as e :
                print "**** LCD: "+lcd+" cannot be queried ****  "
                print e
                continue
            
     
            if init_routes_info != None and init_routes_info :
                
                # several route options
                for route in init_routes_info:
                    # links in one route
                    for link in route:
                        #
                        #Route[(linkID,length,instruction,[lat,long]),(),...]
                        #
                        loginfo=lcd+"|"+link[0]+"|"+link[2]+"\n"
                        txt_linkid_lcd=lcd_output+";"+link[0]+"\n"
                    
                        f_log.write(loginfo)
                        f_linkid_lcd.write(txt_linkid_lcd)
                        
                        #suppose there should be one link for 1 lcd
                        #break;
                    #suppose there should only be one route option
                    #break;        
            else:
                print "None route is found for "+lcd
        f.close()
        f_log.close()
    
    '''      
    def analyzeLog(self, name):
        f=open('../log_'+name+'.txt','r')
        
        lcd_table={}
        while True:
            line=f.readline();
            if not line: break
            pos=line.split('|')
            lcd=pos[0]
            linkid=pos[1]
            
            value=lcd_table.get(lcd)
            
            if value == None:
                value=1
            else:
                value=value+1
            
            lcd_table.update({lcd:value})
        
        f.close()
        
        f_status=open('../status_'+name+'.txt','w')
        
        for (k,v) in lcd_table.items():  
            f_status.write(k+":"+str(v)+"\n")
        
        f_status.close()
        
    
    def getlcdNolinks(self, name, count):
        
        f_status=open('../status_'+name+'.txt','r')
        lcd_table={}
        while True:
            line=f_status.readline();
            if not line: break
            pos=line.split(':')
            lcd=pos[0]
            value=pos[1]
            if int(value)== int(count):
                lcd_table.update({lcd:value})
            
            
        f=open('../log_'+name+'.txt','r')
        
        f_noLinks=open('../nolinks_'+name+'.txt','w')
        
        print len(lcd_table)
        
        while True:
            line=f.readline();
            if not line: break
            pos=line.split('|')
            lcd=pos[0]
            linkid=pos[1]
            instruction=pos[2]
            
            if lcd_table.get(lcd) != None:
                f_noLinks.write(lcd+"|"+instruction)
                        
            
        
        f.close()
        f_noLinks.close()
        '''
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

def usage():
    print "Pls run the command with all parameters, like:"
    print "    python Route.py startGeoX StartGeoY EndGeoX EndGeoY Planned_Time(HHmm)"
    print "\n    Example,\n    python Route.py 39.89091 116.46166 39.89437471954941 116.46173521534428 1432"
    print ""
    

def main():

    '''
    args_size=len(sys.argv)
    if args_size != 6:
        usage()
        sys.exit()
        
    start_geoX=sys.argv[1]
    start_geoY=sys.argv[2]
    end_geoX=sys.argv[3]
    end_geoY=sys.argv[4]
    planned_time=sys.argv[5]
    
    req = urllib2.Request(request_string)
    response = urllib2.urlopen(req)
    image_data = response.read()
        
    '''
    my_route=RoutesMain()
    
    #my_route.testGetRoutes()
    
    my_route.testGet24HrRoutes()

    #my_route.testPos2Link(sys.argv[1])
    
    #my_route.testListRoutes()
    


if __name__=='__main__':
    main()
