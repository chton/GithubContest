'''
Created on 31-jul-2009

@author: Chton
'''
from MainReader import *
from MainCalculator import *
from MainWriter import *
from Library import *
from time import time



if __name__ == '__main__':
    begin = time()
    lib = Library()
    reader = MainReader(lib)
    calc = MainCalculator(lib)
    writer = MainWriter(lib)
    time1 = time()
    reader.run()
    time2 = time()
    read = time2 - time1
    print "read = " + str(read)
    lib.processData()
    calc.run()
    time3 = time()
    calc = time3 - time2
    print "calc = " + str(calc)
    writer.run()
    end = time()       
    write = end - time3
    total = end - begin
    print "write = " + str(write)
    print "total = " + str(total)


