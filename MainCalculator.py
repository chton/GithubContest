'''
Created on 31-jul-2009

@author: Chton
'''
    
import random
import time
import threading
import Queue
import operator
from math import sqrt
import array
import collections
from collections import deque

class MainCalculator(object):
    '''
    classdocs
    '''


    def __init__(self, lib):
        self.lib = lib
        
    def run(self):
        userpool = deque()
        userpool.append(0)
        ThreadedProcessor(self.lib, userpool).start()
        while len(userpool) > 0:
            time.sleep(1)   
    
    
    
    def sortByPop(self, dict):
        
        def comparer(left, right):
            if len(dict[left]) > len(dict[right]):
                return 1
            if len(dict[left]) == len(dict[right]):
                return 0
            if len(dict[left]) < len(dict[right]):
                return -1
                
        return sorted(dict.keys(), comparer)          
            
class ThreadedProcessor( threading.Thread ):
        
    def __init__(self, lib, userpool):
        self.lib = lib
        self.ListByPerson = lib.ListByPerson
        self.ListByRepos = lib.ListByRepos
        self.ListNeighbours = lib.ListNeighbours
        self.ListSecGenRepos = lib.ListSecondGenerationRepos
        self.userpool = userpool
        self.TableConn = lib.TableConn
        self.TableRepos = lib.TableRepos
        threading.Thread.__init__ ( self )
               
            
    def run(self):
        e = 0
        repossortedkeys = self.sortByPop(self.lib.ListByRepos)
        repossortedkeys.reverse()
        for testuser in self.lib.TestList:             
            user = int(testuser) 
            """closeness calc per user"""
            TableConn = collections.defaultdict(int)
            TableRepos = collections.defaultdict(int)
            repos = self.ListByPerson[user]
            for rep in repos:
                for person in self.ListByRepos[rep]:
                    TableConn[person] +=  1
            """weighted closeness calc per repos"""
            currenthighest = 0
            for person in TableConn:
                for reps in self.ListByPerson[person]:
                    TableRepos[reps] += TableConn[person]
                    if TableRepos[reps] > currenthighest:
                        currenthighest = TableRepos[reps]
            for repos in TableRepos:
                TableRepos[repos] = TableRepos[repos]*100/currenthighest
            """forks"""
            PARENTFACTOR = 30
            CHILDFACTOR = 10
            KNOWNFACTOR = 40
            BROTHERFACTOR = 10
            for repos in self.lib.ChildrenList:
                alreadyknown = repos in self.ListByPerson[user]
                reposchildren = len(self.lib.ChildrenList[repos])
                #alreadysuggested = TableRepos.get(repos) is not None
                purifiedlist = [x for x in self.lib.ChildrenList[repos] if x not in self.ListByPerson[user]]
                commonlist = [x for x in self.lib.ChildrenList[repos] if x in self.ListByPerson[user]]
                hasknownchild = len(commonlist) > 0
                if alreadyknown and not hasknownchild:            
                    for rep in purifiedlist:                        
                        TableRepos[rep] += CHILDFACTOR
                elif alreadyknown and hasknownchild:
                    for rep in purifiedlist:
                        TableRepos[rep] += BROTHERFACTOR
                elif not alreadyknown and hasknownchild: 
                    TableRepos[repos] += PARENTFACTOR
                    for rep in purifiedlist:
                        TableRepos[rep] += BROTHERFACTOR
                    for rep in commonlist:
                        TableRepos[repos] += KNOWNFACTOR
            
            """adding repos by known authors"""
            AUTHORFACTOR = 40
            knownauthors = []
            for repos in self.ListByPerson[user]:
                knownauthors.append(self.lib.ReposData[repos]["author"])
            for repos in [x for x in TableRepos.iterkeys() if self.lib.ReposData[x]["author"] in knownauthors]:
                    TableRepos[repos] += AUTHORFACTOR
                
            """sorting and filling of second suggestion list (repos of top common users)"""          
            #print tuples           
            sortedList =  sorted(TableRepos, key=TableRepos.__getitem__)
            sortedPeopleList = sorted(TableConn, key=TableRepos.__getitem__)
            sortedList.reverse()
            sortedPeopleList.reverse()
            #print len(sortedtuples)
            testsuggestions = []
            y = 0
            userset = set(self.ListByPerson[user])
            testsuggestions.extend(sortedList)
            secondsuggestions = []
            while y < len(sortedPeopleList):
                person = sortedPeopleList[y]
                if person in self.ListByPerson:
                    reposset = set(self.ListByPerson[person])
                    secondsuggestions.extend(reposset.difference(userset))
                y = y + 1
            testsuggestions.sort(key=lambda x: self.TableRepos.get(x))
            secondsuggestions.sort(key=lambda x: self.TableRepos.get(x))
            
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
            print str(e) + " suggestion scores:"
            print [ TableRepos.get(x) for x in self.lib.TestList[user] ]
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