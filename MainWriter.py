'''
Created on 1-aug-2009

@author: Chton
'''

class MainWriter(object):
    '''
    classdocs
    '''


    def __init__(self, lib):
        '''
        Constructor
        '''
        self.TestList = lib.TestList
        self.writeEmpty()
        
    def run(self):
        self.writeData()
        
    def writeData(self):
        f = open('results.txt', 'w')
        for user, data in self.TestList.iteritems():
            i = 1
            line = str(user) + ":"
            for repos in data:
                if i < len(data):
                    line = line + str(repos) + ","
                    i = i + 1
                else:
                    line = line + str(repos)
            line = line  + "\n"
            f.write(line)
        f.close()
        
    def writeEmpty(self):
        f = open('results.txt', 'w')
        f.write("")
        f.close()
        
        