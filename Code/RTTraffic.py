#!/usr/bin/python
#coding: utf-8


class RTTraffic:

    TrafficData={}
    IncidentData=[]
    def __init__(self):   
        self.load_traffic('../Traffic/Beijing/Flow/FlowData.csv')
        self.load_incident('../Traffic/Beijing/Incident/IncidentData.csv')
        TrafficData={}
        IncidentData=[]
        
    def load_traffic(self, traffic_file_name):
        
        indexes = ('primary_location', 'direction', 'event_code','speed_limit_advice')
        self.TrafficData=self.getData(traffic_file_name,indexes, True)
        
    def load_incident(self, traffic_file_name):
        indexes = ('primary_location', 'direction','event_code', 'latitude', 'longitude')
        self.IncidentData=self.getData(traffic_file_name,indexes, False)
        
    def getData(self, traffic_file_name,headers, notList):
        seperator = ','
        file_csv = open(traffic_file_name,'r')
        line = file_csv.readline()
        
        line=line.replace('\xef\xbb\xbf', '')
        
        indexes = line.split(seperator)
        end= len(indexes)
        
        headers_pos=[]
        
        for header in headers:
            index=0
            while index<end:
                result=indexes[index].find(header)
                if result != -1:
                    headers_pos.append(index)
                    break
                index +=1
                
        if(len(headers_pos) != len(headers)):
            print 'Cannot find all data from ' + traffic_file_name
            raise Exception('Cannot find all data from ' + traffic_file_name)
        
        if notList:
            data={}
        else:
            data=[]
        while True:
            line = file_csv.readline()
            if not line:
                break
            split_array = line.split(seperator)
            
            lcd=str(split_array[headers_pos[0]])+'_'+str(split_array[headers_pos[1]])
            
            left_headers=headers_pos[2:]
            
            values=[]
            for pos in left_headers:
                values.append(split_array[pos])
            if notList :
                data.update({lcd:values})
            else:
                data.append([lcd,values])
            
        return data
        
def main():

    rt=RTTraffic()
    real_speed=2
    link_speed=27.8480035
    link_length=12
    mini_len=10
    mini_speed=10
    if(real_speed<link_speed and link_length > mini_len and real_speed < mini_speed):
        print 'found'
    else:
        print 'not found'
        
if __name__=='__main__':
    main()