#!/usr/bin/python

import time
from datetime import *
 
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
    def refineString(str):
        str=str.strip()
        str=str.replace("\n","")
        str=str.replace("\r","")
        
        return str

def main():
    
    time_str=Tool.getNextTime('201404092304', 1)
    print time_str
    print Tool.getDayofWeek(time_str)
    print Tool.getTimeIndex(time_str)
    
if __name__=='__main__':
    main()
