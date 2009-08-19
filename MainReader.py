'''
Created on 31-jul-2009

@author: Chton
'''
import threading
import Queue
import time
import random

class MainReader(object):
    '''
    classdocs
    '''

    def __init__(self, lib):
        self.lib = lib
     
    def run(self):
        self.readData()
        self.readTest()
        self.readRepos()
        
    def readData(self):
        print "STARTING FILE READ"
        f = open('data/data.txt')
        i = 0
        linepool = Queue.Queue ( 0 )
        for line in f.readlines():
            linepool.put(line)
            i = i + 1
       #     print i
        f.close()
        print "END FILE READ"
        print "STARTING THREADS"
        for x in range(1):
            ThreadedProcessor(self.lib, linepool).start()
        while not linepool.empty():
            time.sleep(1)   
        print "THREADS ALL FINISHED!" 
        print "Processed entries: " + str(i)
                
    def readTest(self):
        print "STARTING TEST DATA READ"
        f = open('data/test.txt')
        i = 0
        for line in f.readlines():
            line = line.strip()
            self.addToTestLib(line)
            i = i + 1
        f.close()
        print "FINISHED TEST DATA READ"
        print "Data in repostable: " + str(len(self.lib.ListByRepos.keys()))
        print "Data in usertable: " + str(len(self.lib.ListByPerson.keys()))
        print "Data in testusertable: " + (str(len(self.lib.PreTestList)))
        #print self.lib.ListByPerson
        
    def readRepos(self):
        print "STARTING REPOS DATA READ"
        f = open('data/repos.txt')
        i = 0
        for line in f.readlines():
            line = line.strip()
            lineparts = line.split(',')
            repos = lineparts[0].split(':')
            reposnumber = int(repos[0])
            repodata = repos[1].split('/')
            if len(lineparts) > 2:
                forkedfrom = int(lineparts[2])
                if forkedfrom not in self.lib.ChildrenList.keys():
                    self.lib.ChildrenList[forkedfrom] = []
                self.lib.ChildrenList[forkedfrom].append(reposnumber)  
            self.lib.ReposData[reposnumber] = {} 
            self.lib.ReposData[reposnumber]["author"] = repodata[0]
            self.lib.ReposData[reposnumber]["name"] = repodata[1]
            i = i + 1
        f.close()
        print "FINISHED REPOS DATA READ"
        print "Data in Children: " + str(len(self.lib.ChildrenList.keys()))
        
    def addToTestLib(self, line):
        self.lib.PreTestList.append(int(line))
        #if not line in self.lib.ListByPerson.keys():
        #        self.lib.ListByPerson[line] = []

class ThreadedProcessor( threading.Thread ):
        
    def __init__(self, lib, linepool):
        self.lib = lib
        self.linepool = linepool
        threading.Thread.__init__ ( self )
    
    def run(self):
        i = 0
        while (not self.linepool.empty()) and (i < 500000):       
            line = self.linepool.get()
            line = line.strip()
            lineparts = line.split(":")
            self.addToLib(lineparts[0], lineparts[1])
            i = i + 1
                
        print "THREAD PROCESSED LINES: " + str(i)
        
    def addToLib(self, user, repos):
        self.addToDict(self.lib.ListByPerson, user, repos)
        self.addToDict(self.lib.ListByRepos, repos, user)

    def addToDict(self, dict, key, value):
            if not int(key) in dict:
                dict[int(key)] = []
            dict[int(key)].append(int(value))
            
    
        