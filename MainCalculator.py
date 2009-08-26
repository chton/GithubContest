'''
Created on 31-jul-2009

@author: Chton
'''
    
import random
import time
import threading
import Queue
import operator
from math import sqrt, log
import array
import collections
from collections import deque
from time import time, sleep
from heapq import nlargest

class MainCalculator(object):
    '''
    classdocs
    '''


    def __init__(self, lib):
        self.lib = lib
        
    def run(self):
        userpool = deque()
        userpool.append(0)
        ThreadedProcessor(self.lib, userpool).run()
       # while len(userpool) > 0:
       #     sleep(1)
    
    
    
    def sortByPop(self, dict):
        
        def comparer(left, right):
            if len(dict[left]) > len(dict[right]):
                return 1
            if len(dict[left]) == len(dict[right]):
                return 0
            if len(dict[left]) < len(dict[right]):
                return -1
                
        return sorted(dict.keys(), comparer)          
            
class ThreadedProcessor( object ):
        
    def __init__(self, lib, userpool):
        self.lib = lib
        self.ListByPerson = lib.ListByPerson
        self.ListByRepos = lib.ListByRepos
        self.ListNeighbours = lib.ListNeighbours
        self.ListSecGenRepos = lib.ListSecondGenerationRepos
        self.userpool = userpool
        self.TableConn = lib.TableConn
        self.TableRepos = lib.TableRepos
        self.ChildrenList = lib.ChildrenList
        #threading.Thread.__init__ ( self )
               
            
    def run(self):
        e = 0
        repossortedkeys = self.sortByPop(self.lib.ListByRepos)
        repossortedkeys.reverse()
        timeinit = 0
        timescoring = 0
        timeforks = 0
        timeauthors = 0
        timesorting = 0
        timefinal = 0
        for testuser in self.lib.TestList:       
            time1 = time()      
            user = int(testuser) 
            """closeness calc per user"""
            TableConn = collections.defaultdict(int)
            TableRepos = collections.defaultdict(int)
            ConnRepos = collections.defaultdict(int)
            Scoring = collections.defaultdict(int)
            ReposRatio = collections.defaultdict(float)
            knownauthors = []
            knownnames = []
            SecondGenReposList = []
            repos = self.ListByPerson[user]
            for rep in repos:
                for person in self.ListByRepos[rep]:
                    TableConn[person] +=  1
                    SecondGenReposList.extend(self.ListByPerson[person])
                knownauthors.append(self.lib.ReposData[rep]["author"])
                reponame = self.lib.ReposData[rep]["name"].lower()
                strippedreponame = reponame.replace('-', '.').replace('_', '.')
                knownnames.extend(strippedreponame.split('.'))
                
            time2 = time()
            """weighted closeness calc per repos"""
            currenthighest = 0
            for person in TableConn:
                for reps in self.ListByPerson[person]:
                    TableRepos[reps] += TableConn[person]
                    ConnRepos[reps] += 1                    
                    if TableRepos[reps] > currenthighest:
                        currenthighest = TableRepos[reps]
            for repos in TableRepos:
                ReposRatio[repos] = float(ConnRepos[repos])/len(self.lib.ListByRepos)
                Scoring[repos] = TableRepos[repos]*100/currenthighest
            time3 = time()
            """forks"""
            PARENTFACTOR = 30
            CHILDFACTOR = 10
            KNOWNFACTOR = 40
            BROTHERFACTOR = 10
            FACTOR = 0
            for repos in self.ChildrenList:
                alreadyknown = repos in self.ListByPerson[user]
                reposchildren = len(self.ChildrenList[repos])
                #alreadysuggested = TableRepos.get(repos) is not None
                purifiedlist = set(self.ChildrenList[repos]) - set(self.ListByPerson[user])
                commonlist = set(self.ChildrenList[repos]) - purifiedlist
                hasknownchild = len(commonlist) > 0    
                if hasknownchild:
                    FACTOR = BROTHERFACTOR
                    if not alreadyknown:
                        Scoring[repos] += (PARENTFACTOR + (KNOWNFACTOR*len(commonlist)))
                elif alreadyknown: 
                    FACTOR = CHILDFACTOR  
                if FACTOR > 0:
                    for rep in purifiedlist:
                        Scoring[rep] += FACTOR
                    
            time4 = time()
            """adding repos by known authors"""
            AUTHORFACTOR = 17             
            for repos in [x for x in Scoring.iterkeys() if self.lib.ReposData[x]["author"] in knownauthors]:
                    Scoring[repos] += AUTHORFACTOR
            time5 = time()
            
            """adding repos by names"""
            NAMEFACTOR = 10
            for repos in Scoring:
                 reponame = self.lib.ReposData[repos]["name"].lower()
                 strippedreponame = reponame.replace('-', '.').replace('_', '.')
                 commonlist = [x for x in strippedreponame.split('.') if x in knownnames]
                 if len(commonlist) > 0:
                     Scoring[repos] += NAMEFACTOR
            
            """sorting and filling of second suggestion list (repos of top common users)"""          
            #print tuples           
            sortedList =  nlargest(10, Scoring, key=Scoring.__getitem__)
            sortedPeopleList = nlargest(2, self.ListByPerson, key=TableConn.__getitem__)
            userset = set(self.ListByPerson[user])
            testsuggestions = sortedList
            secondsuggestions = []
            for person in sortedPeopleList:
                reposset = set(self.ListByPerson[person])
                secondsuggestions.extend(reposset.difference(userset))
            secondsuggestions.sort(key=lambda x: self.TableRepos.get(x))
            time6 = time()
            """filling final testlist"""
            l = len(testsuggestions)  
            d = len(secondsuggestions)          
            r = 10
            rt = 10
            t = 0
            if rt-t > r:
                rt = r+t
            self.lib.TestList[user] = testsuggestions[t:rt] 
            if rt-t < r:
                self.lib.TestList[user].extend([x for x in secondsuggestions if not x in self.lib.TestList[user] and not x in self.lib.ListByPerson[user]][0:r-(rt-t)])
            f = len(self.lib.TestList[user])
            if  f < r:
                self.lib.TestList[user].extend([x for x in repossortedkeys if not x in self.lib.TestList[user] and not x in self.lib.ListByPerson[user]][0:r-f])
            self.writeData(user)
            e = e + 1
            time7 = time()
            print str(e) + " added suggestions in " + str(time7 - time1)
            """
            timeinit = (timeinit + time2-time1)/2
            timescoring = (timescoring + time3-time2)/2
            timeforks = (timeforks + time4-time3)/2
            timeauthors = (timeauthors + time5-time4)/2
            timesorting = (timesorting + time6-time5)/2
            timefinal = (timefinal + time7-time6)/2
            print "timeinit = " + str(timeinit)
            print "timescoring = " + str(timescoring)
            print "timeforks = " + str(timeforks)
            print "timeauthors = " + str(timeauthors)
            print "timesorting = " + str(timesorting)
            print "timefinal = " + str(timefinal)
            """
        self.userpool.pop()
                  
    
    def writeData(self, user):
        f = open('results.txt', 'a')
        i = 1
        line = str(user) + ":"
        for repos in self.lib.TestList[user]:     
                if i < len(self.lib.TestList[user]):
                    line = line + str(repos) + ","
                    i = i + 1
                else:
                    line = line + str(repos)
        line = line  + "\n"
        f.write(line)
        f.close()
        
    def sortByPop(self, dict):
        return sorted(dict.keys(), key=lambda x:len(dict[x]))