#!/usr/bin/env python
# -*- coding: utf-8 -*-

from consensus_algorithm import ConsensusAlgorithm

from assisipy import casu

import sys
from threading import Thread, Event
from copy import deepcopy
import json
import numpy as np

class ConsensusController(Thread):

    def __init__(self, rtc_file, consensus):
        
        Thread.__init__(self)

        self.casu = casu.Casu(rtc_file)
        self.nbg_ids = [int(name[-3:]) for name in self.casu._Casu__neighbors]
        self.consensus = deepcopy(consensus)
        self.Td = 1 # Sample time is 1 second
        
        self.stop_flag = Event()

    def update(self):
        
        np.set_printoptions(precision=3)    
        # Hack for testing
        numbees = [6,3,0,0,0,0,0,0,0]
        casu_id = self.consensus.casu_id

        # Compute one step of the algorithm
        self.consensus.step(numbees[casu_id],1)

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
                casu_sender = msg['sender']
                rec_data = msg['data'].split(';')
                rec_nbg_temp = float(rec_data[1])
                rec_nbg_zeta = json.loads(rec_data[0])

                #print(self.casu.name(),['%.3f' % z for z in self.consensus.zeta[-1][self.consensus.casu_id-1]],casu_sender,['%.3f' % z for z in rec_nbg_zeta])

                for nbg in self.nbg_ids:
                    #print(self.casu.name(), nbg, ['%.3f' % z for z in self.consensus.zeta[-1][nbg-1]])                
                    #print(self.casu.name(), nbg, self.consensus.t_ref)     
     
                    self.consensus.zeta[-1][int(casu_sender[-3:]) -1] = deepcopy(rec_nbg_zeta)
                    self.consensus.t_ref[int(casu_sender[-3:])-1] = rec_nbg_temp     
                    
                    #print('NEW',self.casu.name(), nbg, self.consensus.t_ref) 
                    #print(self.casu.name(), nbg, int(casu_sender[-3:]), np.array(rec_nbg_zeta), np.array(self.consensus.zeta[-1]))

#['%.3f' % z for z in self.consensus.zeta[-1][nbg-1]])
        
        print(self.casu.name(), np.array(self.consensus.zeta[-1]), 'T_ref', self.consensus.t_ref)
    


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

    
    
