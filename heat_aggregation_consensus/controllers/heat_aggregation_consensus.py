#!/usr/bin/env python
# -*- coding: utf-8 -*-

from consensus_algorithm import ConsensusAlgorithm

from assisipy import casu

import sys
from threading import Thread, Event
from copy import deepcopy
import json

class ConsensusController(Thread):

    def __init__(self, rtc_file, consensus):
        
        Thread.__init__(self)

        self.casu = casu.Casu(rtc_file)
        self.nbg_ids = [int(name[-3:]) for name in self.casu._Casu__neighbors]
        self.consensus = deepcopy(consensus)
        self.Td = 1 # Sample time is 1 second
        
        self.stop_flag = Event()

    def update(self):
        # Hack for testing
        numbees = [6,3,0,0,0,0,0,0,0]
        casu_id = self.consensus.casu_id

        # Compute one step of the algorithm
        self.consensus.step(numbees[casu_id],0.1)

        # Communicate with neighbors

        for nbg in self.casu._Casu__neighbors:
            self.casu.send_message(nbg,json.dumps(self.consensus.zeta[-1][casu_id-1])
                                   + ';' + str(self.consensus.t_ref[casu_id-1]))

        recv_count = 0
        while recv_count < len(self.nbg_ids):
            msg = self.casu.read_message()
            if msg:
                recv_count += 1
                #print(self.casu.name(),msg)
        
        print(self.casu.name(),['%.3f' % z for z in self.consensus.zeta[-1][self.consensus.casu_id-1]],
              ['%.3f' % t for t in self.consensus.t_ref])

    def run(self):
        # Just call update every Td
        while not self.stop_flag.wait(self.Td):
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

    assert(len(sys.argv) > 1)

    rtc = sys.argv[1]
    
    # Parse rtc file name to get CASU id
    # assumes casu-xxx.rtc file name format
    casu_id = int(rtc[-7:-4])

    # Initialize consensus algorithm
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

    zeta = [[[0,0.1,0.1,0],
             [0.1,0,0,0.1],
             [0.1,0,0,0.1],
             [0,0.1,0.1,0]]]

    # Adjecency matrix
    A = [[0, 1, 0, 1, 0, 0, 0, 0, 0], 
        [1, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 1, 0]]

    A = [[0,1,1,0],
         [1,0,0,1],
         [1,0,0,1],
         [0,1,1,0]]

    ca = ConsensusAlgorithm(casu_id,zeta,A)
    ctrl = ConsensusController(rtc, ca)
    ctrl.run()

    
    
