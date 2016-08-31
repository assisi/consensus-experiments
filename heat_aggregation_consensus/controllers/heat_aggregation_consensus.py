#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assisipy import casu

from threading import Thread, Event

from copy import deepcopy

class ConsensusAlgorithm:

    def __init__(self, casu_id, zeta, A):

        self.casu_id = casu_id
        self.zeta = zeta
        self.A = A
        self.temp_setpoints = [27 for x in A[0]]

    def step(self, numbees, dt):
        """ One step of the algorithm """
        
        # Create zeta for next step
        self.zeta.append([[0 for x in row] for row in zeta[-1]])        
        self.update_zeta(numbees, dt)
        #self.update_setpoint()

    def update_zeta(self, numbees, dt):
        """
        Update the zeta matrix, based on neighbors' data
        and bee density estimate.
        """
        i = self.casu_id - 1
        
        for j in range (n):
            
            dzeta1 = 0
            dzeta2 = 0
            for k in range (n):
                dzeta1 += self.A[i][k]*self.zeta[-2][i][k]*(self.zeta[-2][k][j]-self.zeta[-2][i][j])

            """ Include IR detection"""
            if i == j:                
                dzeta2 = numbees/6.0 - self.zeta[-2][i][i]            

            self.zeta[-1][i][j] = self.zeta[-2][i][j] + dt*(dzeta1 + dzeta2)

    def print_zeta(self,k=-1):
        for row in self.zeta[k]:
            row_formated = [ '%.3f' % elem for elem in row ]
            print (row_formated)

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



def compute_setpoint(casu_id, zeta, nbg, x):
    """
    Compute temperature sensor setpoints
    from zeta matrix.
    """
    i = casu_id - 1
    zeta_i_max = max(zeta[i])
    i_leader = 0
    x_nbg_i_max = 0
    for j in range (9):
        if (i==j) and (zeta[i][j]==zeta_i_max):
            setpoint = 36
            i_leader = 1
        elif (i_leader == 0) and (nbg[j] == 1) and (x_nbg_i_max < x[j]):
            x_nbg_i_max = x[j]            
            setpoint = x_nbg_i_max - 4

    """ Reference limits """
    if setpoint < 26:
        setpoint = 26
    if setpoint > 38:
        setpoint = 38

    return setpoint 

if __name__ == '__main__':

    casu_id = 1
    """ Number of CASUs in the arena"""
    n = 9
    """ Discretization time in sec """
    Td = .1
    """ Experiment time in sec """
    Texp = 100
    """ Initial temperature """
    x = [27, 27, 27, 27, 27, 27, 27, 27, 27]
    """ Initial value for zeta """
    #zeta = [[0 for i in range(9)] for j in range(9)]
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
 
    #zeta[0][0] = 0.5

    """ Neighbours matrix"""
    nbg = [0, 1, 0, 1, 0, 0, 0, 0, 0]

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

    """ Debug print """
    #print(numbees)
    #print(readings[0])

    """ Fake data from neighbors """
    nbg_data = [[0,0,0,0,0,0,0,0,0,0],
               [0.1,0,0.1,0,0.1,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0]]
    
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

        t += Td     

  
    """ Debug print """
    """
    for cons in enumerate(consensuses):
        print('-------------------- Casu-00{0} --------------------'.format(k+1))
        cons.print_zeta()
    """

    #x_formated = [ '%.2f' % elem for elem in x ]
    #print('Temperature=')
    #print(x_formated)


