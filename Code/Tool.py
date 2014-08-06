#!/usr/bin/python

import time
from datetime import *
import math
 
class Tool:

    Debug=False

    def __init__(self, debug):
        self.Debug=debug
           
    def debugMessage(self, message):
        if self.Debug==True:
            print message

    @staticmethod    
    def debugStaticMessage(debug,message):
        if debug==True:
            print message
     
    @staticmethod    
    def errorLog(message):
        f=open('../error.log', 'a')
        f.write(message)
        f.close()
    
    @staticmethod    
    def results2Log(message, filename='app'):
        f=open('../'+filename+'.log', 'a')
        f.write(message)
        f.close()
        
    @staticmethod
    def getDayofWeek(time_str):
         date=datetime.strptime(time_str,'%Y%m%d%H%M')
         dayofweek=date.isoweekday()
         # an integer, where Monday is 1 and Sunday is 7
         return dayofweek
    
    @staticmethod
    def getTimeIndex(time_str):
        #
        #time_str yyyymmddHHMM
        # 0-4 mins , index=0
        # 5-9 mins, index=1
        hh=time_str[8:10]
        mm=time_str[10:12]
        index=(int(hh)*60+int(mm))/5

        return index
        
    @staticmethod
    def getNextTime(time_str, mins):
        #
        #time_str yyyymmddHHMM
        date=datetime.strptime(time_str,'%Y%m%d%H%M')

        mins=int(mins)
        span=timedelta(minutes=mins)
        date2= date+span
        
        nexttime_str=date2.strftime('%Y%m%d%H%M')        
        return nexttime_str
    
    @staticmethod
    def getNow():
        date=datetime.now()
        now=date.strftime('%Y%m%d%H%M')  
        
        return now
    
    @staticmethod
    def getPreTime(time_str, mins):
        #
        #time_str yyyymmddHHMM
        date=datetime.strptime(time_str,'%Y%m%d%H%M')

        mins=int(mins)
        span=timedelta(minutes=mins)
        date2= date-span
        
        pretime_str=date2.strftime('%Y%m%d%H%M')        
        return pretime_str    
    
    @staticmethod
    def refineString(str):
        str=str.strip()
        str=str.replace("\n","")
        str=str.replace("\r","")
        
        return str

    @staticmethod
    def coords_to_distance(coords_a, coords_b):
        lat_a = coords_a[0]
        lon_a = coords_a[1]
        lat_b = coords_b[0]
        lon_b = coords_b[1]

        c = math.sin(lat_a) * math.sin(lat_b) * math.cos(lon_a - lon_b) + math.cos(lat_a) * math.cos(lat_b)
        distance = 1000*6371.004 * math.acos(c)*math.pi/180
        #unit is meter
        return distance
        
    @staticmethod    
    def middlepoint(coords_a, coords_b):
        
        lat1=float(coords_a[0])
        lon1=float(coords_a[1])
        lat2=float(coords_b[0])
        lon2=float(coords_b[1])
        
        dLon = math.radians(lon2 - lon1)

        #convert to radians
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)
        lon1 = math.radians(lon1)

        Bx = math.cos(lat2) * math.cos(dLon)
        By = math.cos(lat2) * math.sin(dLon)
        lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), math.sqrt((math.cos(lat1) + Bx) * (math.cos(lat1) + Bx) + By * By))
        lon3 = lon1 + math.atan2(By, math.cos(lat1) + Bx)
        
        return [math.degrees(lat3),math.degrees(lon3)]
    
    @staticmethod 
    def middlepointS(coords_a, coords_b):
        lat1=float(coords_a[0])
        lon1=float(coords_a[1])
        lat2=float(coords_b[0])
        lon2=float(coords_b[1])
        
        lat3=(lat1+lat2)/2
        lon3= (lon1+lon2)/2
        
        return [lat3,lon3]
    
def main():
    
    geo=Tool.middlepoint(['39.1','116.1'],['39.3','116.3'])
    geo1=Tool.middlepointS(['39.1','116.1'],['39.3','116.3'])
    
    print Tool.getNow()
    print Tool.coords_to_distance([36.117,116.876],[36.1171,116.876])
    
if __name__=='__main__':
    main()
