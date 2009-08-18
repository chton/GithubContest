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
        a = 1
        userpool = Queue.Queue ( 0 )
        #print len(self.PreTestList)
        for user in self.PreTestList:
            userpool.put(user)
        for x in range(a):
            ThreadedLibCalcer(self, userpool).start()
        while not userpool.empty():
            time.sleep(10) 
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
            while (not self.userpool.empty()) and (i < 10000):   
                user = int(self.userpool.get()) 
                if not user in self.ListByPerson:
                    self.ListByPerson[user] = []
                #repos = self.ListByPerson[user]
                """self.TableConn[user] = {}
                self.TableRepos[user] = {}
                #neighbours = []
                for rep in repos:
                    for person in self.ListByRepos[rep]:
                        if not person in self.TableConn[user].keys():
                            self.TableConn[user][person] = 0
                        
                        current = self.TableConn[user].get(person)
                        if current is None:
                            current = 0
                        self.TableConn[user][person] = current + 1
                        for repos in self.ListByPerson[person]:
                            current = self.TableRepos[user].get(repos)
                            if current is None:
                                current = 0
                            self.TableRepos[user][repos] = current + 1
                    
                for person in self.TableConn[user].keys():
                    for repos in self.ListByPerson[person]:
                        current = self.TableRepos[user].get(repos)
                        if current is None:
                            current = 0
                        self.TableRepos[user][repos] = current + 1     
                        #self.TableRepos[user][repos] = current + self.TableConn[user][person]              
                     #print person
                #print len(self.TableConn[user])       
                #limitedsortedneighbours = self.sortByMostOcc(neighbours)
                #self.ListNeighbours[user] = dict(map(lambda i: (i,1),limitedsortedneighbours)).keys()
                #self.ListNeighbours[user] = neighbours
                #print len(limitedsortedneighbours)
                self.ListSecondGenerationRepos[user] = []
                secgenrep = []
                UPPERLIMIT = 10
                LOWERLIMIT = 0
                for person in self.TableConn[user].keys():
                        for rep in self.ListByPerson[person]:
                            length = len(self.ListByRepos[rep])
                            if length >= LOWERLIMIT and length <= UPPERLIMIT:
                                secgenrep.append(rep)        
                        #print person
                secgenrepsorted = list(set(secgenrep))
                secgenrepsorted.sort(key=lambda x:(secgenrep.count(x)))
                #secgenrepsorted.reverse()
                self.ListSecondGenerationRepos[user] = []
                l = len(secgenrepsorted)  
                #limit = 200     
                #if limit > l:
                #    limit = l   
                #for r in range(int(limit)):
                self.ListSecondGenerationRepos[user].extend(secgenrepsorted)     
                print len(self.ListSecondGenerationRepos[user])"""
                i = i+1
                #print str(i) + " added to NeighbourLists"
                """ if i%478 == 0:
                p = p+10
                print p
                """
                
            self.userpool.put(0)
            #self.lib.PreTestList.sort(key=lambda x:(len(self.ListSecondGenerationRepos[x])))
            #self.lib.PreTestList.reverse() 
            for key in self.lib.PreTestList:
                self.lib.TestList[int(key)] = []
            self.userpool.get()
                    
                
    def sortByMostOcc(self, list):     
        def comparer(left, right):
            return list.count(left) - list.count(right)               
        return sorted(list, comparer) 

        