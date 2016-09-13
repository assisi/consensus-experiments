#!/usr/bin/env python
# -*- coding: utf-8 -*-

from consensus_algorithm import ConsensusAlgorithm

from assisipy import casu

import sys
import time
from threading import Thread, Event
from datetime import datetime
from copy import deepcopy
import json
import csv

class ConsensusController(Thread):

    def __init__(self, rtc_file, consensus, log=False):
        
        Thread.__init__(self)

        self.casu = casu.Casu(rtc_file,log=True)
        nbg_ids = [int(name[-3:]) for name in self.casu._Casu__neighbors]
        self.nbg_data_buffer = {}
        for nb in nbg_ids:
            self.nbg_data_buffer[nb] = []
        self.consensus = deepcopy(consensus)

        self.Td = 0.25 # Sample time for consensus is 1 second
        #self.t_prev = time.time()
        self.t_prev = 0
        self.stop_flag = Event()

        # Bee density estimation variables
        self.numbees = [0]
        self.nb_buf_len = 5
        self.ir_thresholds = {}
        self.ir_thresholds['casu-001'] = [13500, 11500, 11500, 11500, 10500, 9500]
        self.ir_thresholds['casu-002'] = [12000, 10000, 14500, 13000, 10500, 11500]
        self.ir_thresholds['casu-003'] = [8000, 19500, 20000, 15500, 14000, 12500]
        self.ir_thresholds['casu-004'] = [12500, 17000, 20000, 20000, 20000, 13500]
        self.ir_thresholds['casu-005'] = [16000, 12500, 14000, 25000, 18000, 15500]
        self.ir_thresholds['casu-006'] = [18000, 12000, 18500, 14000, 12000, 12500]
        self.ir_thresholds['casu-007'] = [11500, 11500, 17500, 12500, 14500, 13500]
        self.ir_thresholds['casu-008'] = [14500, 12500, 16500, 14000, 15000, 13000]
        self.ir_thresholds['casu-009'] = [12000, 24000, 14500, 16500, 14200, 12000]

        # Set up zeta logging
        now_str = datetime.now().__str__().split('.')[0]
        now_str = now_str.replace(' ','-').replace(':','-')
        self.logfile = open(now_str + '-' + self.casu.name() + '-zeta.csv','wb')
        self.logger = csv.writer(self.logfile, delimiter=';')
        
    def update(self):
        
        casu_id = self.consensus.casu_id
        
        # Hack for testing
        numbees_fake = [0,3,0,0,0,0,0,0,0]
        self.update_numbees_estimate()
        numbees = sum(self.numbees)/float(len(self.numbees))
        numbees = numbees_fake[casu_id-1]
        #print(self.casu.name(),numbees)
        
        
        # Compute one step of the algorithm
        self.consensus.step(numbees,0.1)
        
        """
        #Testing the algorithm when on node updates it algorithm slower
        if (casu_id is 5) and (self.t_prev > 1):
            self.consensus.step(numbees,0.1)
            self.t_prev = 0
        else:
            self.consensus.step(numbees,0.1)
            self.t_prev += 1
        """     
        
        # Set temperature reference
        self.casu.set_temp(self.consensus.t_ref[casu_id-1])

        # Communicate with neighbors
        for nbg in self.casu._Casu__neighbors:
            self.casu.send_message(nbg,json.dumps(self.consensus.zeta[-1][casu_id-1])
                                   + ';' + str(self.consensus.t_ref[casu_id-1]))

        # Update data buffer with messages from all neighbors
        # We wait here until we have at least one message from every neighbor
        msg = self.casu.read_message()
        while msg:
            nbg_id = int(msg['sender'][-3:])
            self.nbg_data_buffer[nbg_id].append(msg['data'])            
            
            #if self.casu.name() == 'casu-001':
            #    print(nbg_id, self.nbg_data_buffer[nbg_id])
                   
            data = self.nbg_data_buffer[nbg_id].pop(0).split(';')
            rec_nbg_zeta = json.loads(data[0])
            rec_nbg_temp = float(data[1])
            self.consensus.zeta[-1][nbg_id -1] = deepcopy(rec_nbg_zeta)
            self.consensus.t_ref[nbg_id-1] = rec_nbg_temp  
            msg = self.casu.read_message()
                    
                    
        # Log zeta
        self.logger.writerow([time.time()] + [z for row in self.consensus.zeta[-1] for z in row])
        
        print(self.casu.name(),['%.3f' % z for z in self.consensus.zeta[-1][self.consensus.casu_id-1]], 'T_ref=', ['%.1f' % y for y in self.consensus.t_ref], numbees)
        #print(self.casu.name(),['%.3f' % z for z in self.consensus.zeta[-1][self.consensus.casu_id-1]], 'T_ref=', ['%.1f' % y for y in self.consensus.t_ref], 'nb=', numbees)
        #print(self.casu.name(),['%.3f' % z for z in self.consensus.zeta[-1][self.consensus.casu_id-1]],casu_sender,['%.3f' % z for z in rec_nbg_zeta])


    def run(self):
        # Just call update every Td
        while not self.stop_flag.wait(self.Td):
            self.update()

        # Turn off heating
        self.casu.temp_standby()
        print('Turned off heater, exiting...')

    def update_numbees_estimate(self):
        """
        Bee density estimator.
        """
        self.numbees.append(sum([x>t for (x,t) in zip(self.casu.get_ir_raw_value(casu.ARRAY),
                                                      self.ir_thresholds[self.casu.name()])]))
        if len(self.numbees) > self.nb_buf_len:
            self.numbees.pop(0)


if __name__ == '__main__':

    assert(len(sys.argv) > 1)

    rtc = sys.argv[1]
    
    # Parse rtc file name to get CASU id
    # assumes casu-xxx.rtc file name format
    casu_id = int(rtc[-7:-4])

    # Initialize consensus algorithm
    a1 = 0
    a = 0.1
    a2 = 0
    zeta = [[[a1, a, a2, a, a2, a2, a2, a2, a2], 
           [a, a1, a, a2, a, a2, a2, a2, a2],
           [a2, a, a1, a2, a2, a, a2, a2, a2],
           [a, a2, a2, a1, a, a2, a, a2, a2],
           [a2, a, a2, a, a1, a, a2, a, a2], 
           [a2, a2, a, a2, a, a1, a2, a2, a],
           [a2, a2, a2, a, a2, a2, a1, a, a2],
           [a2, a2, a2, a2, a, a2, a, a1, a],
           [a2, a2, a2, a2, a2, a, a2, a, a1]]] 

#    zeta = [[[0,0.1,0.1,0],
#             [0.1,0,0,0.1],
#             [0.1,0,0,0.1],
#             [0,0.1,0.1,0]]]

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
        

    ca = ConsensusAlgorithm(casu_id,zeta,A)
    ctrl = ConsensusController(rtc, ca, log=True)
    ctrl.run()

    
    
