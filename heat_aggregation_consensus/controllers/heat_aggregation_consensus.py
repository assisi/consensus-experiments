#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assisipy import casu

from threading import Thread, Event

from copy import deepcopy

class ConsensusController(Thread):

    def __init__(self, rtc_file, zeta):
        
        Thread.__init__(self)
        self.stopped = event

        self.casu = casu.Casu(rtc_file)
        self.consensus = ConsensusAlgorithm(zeta)
        self.Td = 1 # Sample time is 1 second
        
        self.stop_flag = Event()

    def update(self):
        pass

    def run(self):
        # Just call update every Td
        while not self.stopped.wait(self.Td):
            self.update()

        # Turn off heating
        self.casu.temp_standby()
        print('Turned off heater, exiting...')

def estimate_numbees(readings):
    """
    Bee density estimator.
    """
    numbees = 0

    return numbees

if __name__ == '__main__':

    casu_id = 1
    """ Number of CASUs in the arena"""
    n = 9
    """ Discretization time in sec """
    Td = 0.1
    """ Experiment time in sec """
    Texp = 100
    """ Initial temperature """

    """ Initial value for zeta """
    a1 = 0
    a = 0.1
    zeta = [[[a1, a, 0, a, 0, 0, 0, 0, 0], 
           [a, a1, a, 0, a, 0, 0, 0, 0],
           [0, a, a1, 0, 0, a, 0, 0, 0],
           [a, 0, 0, a1, a, 0, a, 0, 0],
           [0, a, 0, a, a1, a, 0, a, 0], 
           [0, 0, a, 0, a, a1, 0, 0, a],
           [0, 0, 0, a, 0, 0, a1, a, 0],
           [0, 0, 0, 0, a, 0, a, a1, a],
           [0, 0, 0, 0, 0, a, 0, a, a1]]] 

    """ Test stuff here """
    readings = [6,3,0,0,0,0,0,0,0]
    numbees = estimate_numbees(readings)

    """ Adjacency matrix - used for debugging """  
    A = [[0, 1, 0, 1, 0, 0, 0, 0, 0], 
        [1, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 1, 0]]

    
    consensuses = [ConsensusAlgorithm(i+1,deepcopy(zeta),deepcopy(A)) for i in range(n)]

    """ Main loop """
    t = 0
    while t<Texp:

        # Update one consensus step for each casu
        for index in range (n):    #for loop is used for debugging
            numbees = readings[index] 
            consensuses[index].step(numbees,Td)
            
        # Exchange information between CASUs
        for index in range(n):
            for (k,nbg) in enumerate(A[index]):
                if nbg:
                    consensuses[index].zeta[-1][k] = deepcopy(consensuses[k].zeta[-1][k])
                    consensuses[index].t_ref[k] = deepcopy(consensuses[k].t_ref[k])

        t += Td     

