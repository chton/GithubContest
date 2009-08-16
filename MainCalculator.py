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

class MainCalculator(object):
    '''
    classdocs
    '''


    def __init__(self, lib):
        self.lib = lib
        
    def run(self):
        a = 1
        userpool = Queue.Queue ( 0 )
        for user in self.lib.TestList.keys():
            userpool.put(user)
        for x in range(a):
            ThreadedProcessor(self.lib, userpool).start()
        while not userpool.empty():
            time.sleep(1)   
    
    
                
    def oldrun1(self):
        print "STARTING CALCULATIONS"
        repostotal = self.lib.ListByRepos.keys()
        repossortedkeys = self.sortByPop(self.lib.ListByRepos)
        repossortedkeys.reverse()                              
        for user, reposlist in self.lib.TestList.items():
            i = 0 
            while len(reposlist) < 10:
                
                if  not ( user in self.lib.ListByPerson ) or not ( repossortedkeys[i] in self.lib.ListByPerson[user]) :
                    reposlist.append(repossortedkeys[i])
                i = i + 1
        print "FINISH CALC"
    
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
    
    def run1(self):
            print "STARTING CALCULATIONS"
            i = 0
            while (not self.userpool.empty()) and (i < 10000):   
                user = self.userpool.get() 
                if user in self.ListNeighbours.keys():  
                    e = 0
                    while len(self.lib.TestList[user]) < 10 and e < 30:
                        imp = 0
                        bestrepos = 0
                        reposlist = []
                        for person in self.ListNeighbours[user]:
                            for repos in self.ListByPerson[person]:
                                if not repos in self.ListByPerson[user] and not repos in self.lib.TestList[user] and not repos in reposlist:
                                    newneighb = 0
                                    f = 0
                                    for secgen in self.ListByRepos[repos]:
                                        if not secgen in self.ListNeighbours[user]:
                                            newneighb = newneighb + 1
                                    f = f + 1
                                    if newneighb > imp:
                                        imp = newneighb
                                        bestrepos = repos
                                    reposlist.append(repos)
                        e = e + 1
                        print "e = " + str(e)
                        if bestrepos > 0:
                            self.lib.TestList[user].append(bestrepos)
                i = i + 1
                print "i = " + str(i)
                
    def run2(self):
        print "STARTING CALCULATIONS"
        i = 0
        while (not self.userpool.empty()) and (i < 10000):   
            user = self.userpool.get() 
            if user in self.ListNeighbours.keys():
                reposlist = {}
                personlist = []
                for person in self.ListNeighbours[user]:
                    if self.ListNeighbours[user].count(person) > 2 and not person in personlist and not len(reposlist) > 3000:
                        for repos in self.ListByPerson[person]:
                            if not repos in self.ListByPerson[user] and not repos in reposlist:
                                newneighb = len(repos)
                               # for secgen in self.ListByRepos[repos]:
                               #     if not secgen in self.ListNeighbours[user]:
                               #         newneighb = newneighb + 1
                                
                                reposlist[repos] = newneighb
                        personlist.append(person)
                sortedreposlist = self.sortByMostNew(reposlist)
                l = len(sortedreposlist)
                for r in range(10):
                    if r < l:
                        self.lib.TestList[user].append(sortedreposlist[r-1])
                
                self.writeData(user)
            i = i+1
            print i
            
            
    def run3(self):
        print "STARTING CALCULATIONS"
        e = 0
        while (not self.userpool.empty()) and (e < 5000):   
            user = self.userpool.get() 
            if user in self.ListNeighbours.keys():
                reposlist = []
                personlist = []
                i = 0
                while len(reposlist) < 10 and i < 10:
                    for person in self.ListNeighbours[user]:
                        if len(reposlist) < 10:
                            for repos in self.ListByPerson[person]:
                                if not repos in self.ListByPerson[user] and not repos in reposlist and len(reposlist) < 10:
                                    reposlist.append(repos)
                    i = i + 1
                l = len(reposlist)
                for r in range(10):
                    if r < l:
                        self.lib.TestList[user].append(reposlist[r-1])
               # self.writeData(user)
                e = e+1
                print e
                
    def run4(self):
        print "STARTING CALCULATIONS"
        e = 0
        while (not self.userpool.empty()) and (e < 5000):   
            user = self.userpool.get() 
            if user in self.ListNeighbours.keys():
                reposlist = []
                finlist = []
                replist = {}
                personlist = []
                limit = 2
                neighbourset = set(self.ListNeighbours[user])
                while len(replist) < 10 and limit > 1:
               # for person in self.ListNeighbours[user]:
                   # if not person in personlist and len(personlist) < 5:                        
                    for repos in self.ListByRepos.keys():
                        smallset = set(self.ListByRepos[repos]).intersection(neighbourset)
                        smalllist = list(smallset)
                        if not repos in finlist:
                            reposscore = 0
                            for x in range(len(smalllist)):
                                    reposscore = reposscore + self.ListNeighbours[user].count(smalllist[x-1])
                            if not repos in replist and reposscore > limit:
                                replist[repos] = 0
                            if repos in replist:
                                if replist[repos] < reposscore:
                                    replist[repos] = reposscore
                                    print str(repos) + " = " + str(reposscore)
                            finlist.append(repos)
                         #   personlist.append(person)
                    limit = limit/2 
                reposlist = self.sortByMostOcc(replist)
                l = len(reposlist)
                for r in range(10):
                    if r < l:
                        self.lib.TestList[user].append(reposlist[r-1])
               # self.writeData(user)
                e = e+1
                print str(e) + " sug: " + str(l)
                
    def run5(self):
        print "STARTING CALCULATIONS"
        e = 0
        repossortedkeys = self.sortByPop(self.lib.ListByRepos)
        repossortedkeys.reverse()   
        while (not self.userpool.empty()) and (e < 5000):   
            user = self.userpool.get() 
            if user in self.TableConn.keys():
                reposlist = []
                finlist = []
                replist = {}
                personlist = []
                neighbourset = set()
                secgenset = set()
                reposset = set()
                secgenusersofrepos = set()
                neighbourset = set(self.TableConn[user].keys())
                secgenset = set(self.ListSecGenRepos[user])
                #print len(secgenset)
                reposset = set(self.ListByPerson[user])
                secgenusersofrepos = secgenset.difference(reposset)
                #print len(secgenusersofrepos)
                for repos in secgenusersofrepos.difference(set(replist.keys())):
                    smallset = set(self.ListByRepos[repos]).intersection(neighbourset)
                    reposscore = 0
                    tmp = [self.TableConn[user][per] for per in smallset]
                    reposscore = sum(tmp)
                    replist[repos] = reposscore
                    #print str(repos) + " = " + str(reposscore)
                     #   personlist.append(person)
                limit = 1024
                shortlist = []
                while len(shortlist) < 10 and limit >= 1:
                    shortlist = [x for x in replist.keys() if replist[x] >= limit]
                    limit = limit/2                    
                reposlist = sorted(shortlist, key=lambda x:(replist[x]))                
                l = len(reposlist)            
                for r in range(10):
                    if r < l:
                        self.lib.TestList[user].append(reposlist[r-1])
                y = 0
            while len(self.lib.TestList[user]) < 10:
                if repossortedkeys[y] not in self.lib.TestList[user] and repossortedkeys[y] not in  self.lib.ListByPerson[user]:
                    self.lib.TestList[user].append(repossortedkeys[y])
                y = y + 1
            self.writeData(user)
            e = e+1
            print str(e)
            
            
    def run(self):
        e = 0
        repossortedkeys = self.sortByPop(self.lib.ListByRepos)
        repossortedkeys.reverse()
        while (not self.userpool.empty()) and (e < 5000):               
            user = int(self.userpool.get()) 
            if user in  self.lib.ListByPerson:
                TableConn = {}
                TableRepos = {}
                repos = self.ListByPerson[user]
                for rep in repos:
                    for person in self.ListByRepos[rep]:
                        current = TableConn.get(person)
                        if current is None:
                            current = 0
                        TableConn[person] = current + 1
                for person in TableConn.keys():
                    for reps in self.ListByPerson[person]:
                        current = TableRepos.get(reps)
                        if current is None:
                            current = 0
                        TableRepos[reps] = current + 1
                PARENTFACTOR = 1000
                CHILDFACTOR = 1000
                BROTHERFACTOR = 100
                for repos in self.lib.ChildrenList.keys():
                    current = TableRepos.get(repos)
                    if current is None:
                        current = 0
                    purifiedlist = [x for x in self.lib.ChildrenList[repos] if x not in self.ListByPerson[user]]
                    commonlist = [x for x in self.lib.ChildrenList[repos] if x in self.ListByPerson[user]]
                    if repos in self.ListByPerson[user] and len(commonlist) == 0:            
                        for rep in purifiedlist:
                            TableRepos[rep] = current + CHILDFACTOR
                    elif repos in self.ListByPerson[user] and len(commonlist) > 0:
                        for rep in purifiedlist:
                            TableRepos[rep] = current + BROTHERFACTOR  
                    elif repos not in self.ListByPerson[user] and len(commonlist) > 0:
                        TableRepos[repos] = current + PARENTFACTOR   
                        for rep in purifiedlist:
                            TableRepos[rep] = current + BROTHERFACTOR
                tuples = [(i, TableRepos[i]) for i in TableRepos.keys()] # if not self.TableConn[user][i] is None]  
                peopletuples = [(i, TableConn[i]) for i in TableConn.keys()] 
                #print tuples           
                sortedtuples = sorted(tuples , key=operator.itemgetter(1))
                sortedpeopletuples = sorted(tuples , key=operator.itemgetter(1))
                #print len(sortedtuples)
                sortedtuples.reverse()
                sortedpeopletuples.reverse()
                testsuggestions = []
                y = 0
                userset = set(self.ListByPerson[user])
                testsuggestions.extend([i for i, y in sortedtuples])
                secondsuggestions = []
                while y < len(sortedtuples):
                    person, score = sortedtuples[y]
                    if person in self.ListByPerson:
                        reposset = set(self.ListByPerson[person])
                        secondsuggestions.extend(reposset.difference(userset))
                    y = y + 1
                testsuggestions.sort(key=lambda x: self.TableRepos.get(x))
                secondsuggestions.sort(key=lambda x: self.TableRepos.get(x))
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
            #self.writeData(user)
            e = e + 1
            print str(e) + " added Suggestions"
                


            
    def sortByMostOcc(self, replist):     
        #def comparer(left, right
        #    return dict[left] - dict[right]               
        return sorted(replist.keys(), key=lambda x:(replist[x]))


                    
    def sortByMostNew(self, dict):     
        def comparer(left, right):
            if dict[left] > dict[right]:
                return -1
            if dict[left] == dict[right]:
                return 0
            if dict[left] < dict[right]:
                return 1               
        return sorted(dict.keys(), comparer)          
    
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
        
        def comparer(left, right):
            if len(dict[left]) > len(dict[right]):
                return 1
            if len(dict[left]) == len(dict[right]):
                return 0
            if len(dict[left]) < len(dict[right]):
                return -1
                
        return sorted(dict.keys(), comparer)