'''
Created on 1-aug-2009

@author: Chton
'''
import random
import time
import threading
import Queue

class Library(object):
    '''
    classdocs
    '''
    ListByPerson = {}
    ListByRepos = {}
    ListNeighbours = {}
    TestList = {}
    ListSecondGenerationRepos =  {}
    PreTestList = []
    ListData = []
    TableConn = {}
    TableRepos = {}
    ChildrenList = {}
    ReposData = {}

    def __init__(self):
        '''
        Constructor
        '''
        i=0
        print "BEGIN FILLING LISTS"
    #    for key in range ( 100000 ):
    #      self.ListByPerson[str(i)] = []
    #      i = i + 1
        i=0
   #     for key in range ( 124000 ):
   #         self.ListByRepos[str(i)] = []
   #         i = i+1
        self.TestList = {}
        print "END FILLING LISTS"
        
        
    def processData(self):
        print "FILLING ADDITIONAL LIBS"
        userpool = Queue.Queue ( 0 )
        #print len(self.PreTestList)
        userpool.put(0)
        ThreadedLibCalcer(self, userpool).start()
        while not userpool.empty():
            time.sleep(1) 
        print "FINISHED FILLING ADDITIONAL LIBS"


class ThreadedLibCalcer( threading.Thread ):
        
    def __init__(self, lib, userpool):
        self.lib = lib
        self.ListByPerson = lib.ListByPerson
        self.ListByRepos = lib.ListByRepos
        self.ListNeighbours = lib.ListNeighbours
        self.ListSecondGenerationRepos = lib.ListSecondGenerationRepos
        self.userpool = userpool
        self.TableConn = lib.TableConn
        self.TableRepos = lib.TableRepos
        self.PreTestList = lib.PreTestList
        threading.Thread.__init__ ( self )
    
    def run(self):
            i = 0
            p = 0
            for user in self.PreTestList: 
                if not user in self.ListByPerson:
                    self.ListByPerson[user] = []
                self.lib.TestList[user] = []
            self.userpool.get()
                    
                
    def sortByMostOcc(self, list):     
        def comparer(left, right):
            return list.count(left) - list.count(right)               
        return sorted(list, comparer) 

        