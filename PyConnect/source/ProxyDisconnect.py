'''
Written By LEWIS SMEETON, 2012
'''

import numpy as np
import string
import os
import sys
from Disconnect import Disconnect as disc
#from KeywordDict import Keywords
from KeywordInit import Keywords
#--------------------------------------------------------------------#
__metaclass__ = type

class Disconnect(disc):
    '''
    Disconnect is the superclass of DisconnectPlot. It contains 
    methods to find and read input file 'dinfo', and to read data
    from minima and TS database files.
    '''
    
    def __init__(self, keyword):
        super(Disconnect,self).__init__(keyword)
        # Bind Keywords
        #self.kw = keyword

        # Initialising minima_index and ts_index
        # Not necesary for python, but helpful to know what to expect
        # to arrive in a data structure

        #self.InitialiseMin()
        #self.InitialiseTS()
        
        self.CountMin()
        self.CountTS()
        self.RemoveThreshold()
        self.RemoveUnderConnect()
        self.RemoveDisjoint()


        self.InitialiseBasin()
        