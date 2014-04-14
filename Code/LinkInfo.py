#!/usr/bin/python
import os
from Tool import *
#
# {linkid:[lcd,direction]}
TABLE_LINK2LCD = {}

class LinkInfo:
    Path_Home='../'
    Debug= False
    
    def __init__(self):
        if not TABLE_LINK2LCD:
            self.loadLink2Lcd()
            
    def loadLink2Lcd(self):
        '''
		f=open(self.Path_Home+'/res/lcd_Link.txt','r')
        lineNo=0;
        while True:
            line=f.readline();
            if not line: break
            pos=line.split(';')
            lcd=pos[0]
            direction=pos[1]
            linkid=pos[2]
            lineNo +=1
            
            
            linkid=Tool.refineString(linkid)
                
            TABLE_LINK2LCD.update({linkid:[lcd,direction]})
        f.close()
        '''
        
        #print TABLE_LINK2LCD
        
        '''
        Tool.debugStaticMessage(self.Debug,'TABLE_LINK2LCD is loaded with: '+ str(len(TABLE_LINK2LCD)))
        Tool.debugStaticMessage(self.Debug,'File has processed lines: : '+ str(lineNo))
        '''
    def getLcd(self, linkid):
        if TABLE_LINK2LCD ==None or not TABLE_LINK2LCD:
            self.loadLink2Lcd()
        
        return TABLE_LINK2LCD.get(str(linkid))
        
    def findLinkSpeed(self, lcd_direction,time_str):
        speed=-1
        filepath=self.Path_Home+'res/Pattern/'+lcd_direction[0]+'_'+lcd_direction[1]+'.pattern'
        
        day_index=int(Tool.getDayofWeek(time_str))
        time_index=int(Tool.getTimeIndex(time_str))
        
        if day_index ==0:
            day_index=6
        else:
            day_index -=1
        
        
        if os.path.exists(filepath):
            index=0;
            f=open(filepath,'r')
            while True:
                line=f.readline();
                if not line: 
                    print "not find correctly at end of the file"
                    break
                
                if index == day_index:
                    line=line.strip()
                    pos=line.split(' ')
                    speed=pos[time_index]
                    Tool.debugStaticMessage(self.Debug,'Speed is: '+str(speed))
                    break
                else:
                    index +=1
            f.close()
        else:
            print filepath+' is not found'
        
        
        
        return speed
        
    
    def findLinkCertainty(self,lcd_direction,time_str):
        
        certainty=-1
        filepath=self.Path_Home+'res/CertaintyIndex/'+lcd_direction[0]+'_'+lcd_direction[1]+'.ci'
        
        day_index=Tool.getDayofWeek(time_str)
        day_index -=1
        
        time_index=int(Tool.getTimeIndex(time_str))
        
        
        
        if os.path.exists(filepath):
            index=0;
            f=open(filepath,'r')
            while True:
                line=f.readline();
                if not line: 
                    print "not find correctly at end of the file"
                    break
                
                if index == day_index:
                    line=line.strip()
                    pos=line.split(' ')
                    certainty=pos[time_index]
                    Tool.debugStaticMessage(self.Debug, filepath+', certainty is: '+str(certainty))
                    break
                else:
                    index +=1
            f.close()
        else:
            print filepath+' is not found'
        
        
        
        return certainty
    
#############################################################################   
    def testFindLinkCertainty(self):
        print self.findLinkCertainty(['5','0'],'201404092359')
    
    def testGetLcd(self):
        print '\n  testGetLcd() Method : '
        print self.getLcd('+1569069816105926780')
        
    def testFindLinkSpeed(self):
        self.findLinkSpeed(['5','0'],'201404092359')
        
def main():
    link=LinkInfo()
    
    
    
if __name__=='__main__':
    main()
