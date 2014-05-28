#!/usr/bin/python

import sys
import json
from Tool import *
from AdRoute import *


class RouteSession:

    PassedIndex=0
    RouteObj=''
    PassedPos=[]
    
    def __init__(self, route): 
        self.RouteObj=route
        self.PassedIndex=0
        self.PassedPos=[]
        

    def setPassedIndex(self, index):
        self.PassedIndex=index

    def appendPos(self,geo,pathIndex):
        self.PassedPos.append((geo,pathIndex))
        
def main():

    routeSS=RouteSession()


if __name__=='__main__':
    main()