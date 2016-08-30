#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assisipy import casu

from threading import Thread, Event

class ConsensusAlgorithm:

    def __init__(self, zeta):
        self.zeta = zeta
    
    def update(self, nbg_data, numbees):
        pass

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

def update(zeta, nbg_data, numbees):
    """
    Update the zeta matrix, based on neighbors' data
    and bee density estimate.
    """


    return zeta

def compute_setpoint(zeta):
    """
    Compute temperature sensor setpoints
    from zeta matrix.
    """
    setpoint = 26

    return setpoint 

if __name__ == '__main__':

    """ Initial value for zeta """
    zeta = [[0 for i in range(9)] for j in range(9)]

    """ Test stuff here """
    readings = [6 3 0 0 0 0 0 0 0]
    numbees = estimate_numbees(readings)

    """ Debug print """
    print(numbees)

    """ Fake data from neighbors """
    nbg_data = [[1 0 0 1 0 0 0 0 0 0],
                [0 1 0 1 0 1 0 1 0 1],
                [1 0 1 0 1 0 1 0 1 0],
                [1 0 0 1 0 0 0 0 0 0],
                [0 1 0 1 0 1 0 1 0 1],
                [1 0 1 0 1 0 1 0 1 0],
                [1 0 0 1 0 0 0 0 0 0],
                [0 1 0 1 0 1 0 1 0 1],
                [1 0 1 0 1 0 1 0 1 0]]

    zeta = update(zeta, nbg_data, numbees)

    """ Debug print """
    for row in zeta:
        print (zeta)

