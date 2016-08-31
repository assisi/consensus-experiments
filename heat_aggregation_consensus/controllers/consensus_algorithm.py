#!/usr/bin/env python
# -*- coding: utf-

from copy import deepcopy

class ConsensusAlgorithm:

    def __init__(self, casu_id, zeta, A):

        self.casu_id = casu_id
        self.zeta = zeta
        self.A = A
        self.t_ref = [0 for x in A[0]]

    def step(self, numbees, dt):
        """ One step of the algorithm """
        
        # Create zeta for next step
        self.zeta.append([[0 for x in row] for row in zeta[-1]])        
        self.update_zeta(numbees, dt)
        self.update_setpoint(dt)

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

    def update_setpoint(self,dt):
        """
        Compute temperature sensor setpoints
        from zeta matrix.
        """
        i = self.casu_id - 1
        t_ref_new = self.t_ref[i]
        zeta_i_max = max(self.zeta[-2][i])   #zeta in step k
        i_leader = 0
        t_nbg_i_max = 0
        for j in range (n):
            #CASUi is a leader if its zeta is max
            if (i==j) and (self.zeta[-2][i][j]==zeta_i_max):
                t_ref_new = 36
                i_leader = 1
            elif (i_leader == 0) and (A[i][j] == 1) and (t_nbg_i_max < self.t_ref[j]):
                t_nbg_i_max = self.t_ref[j]            
                t_ref_new = t_nbg_i_max - 4
    
        """ Reference limits """
        t_ref_new = sorted([26,t_ref_new,38])[1]

        """ Reference filter """
        self.t_ref[i] += 0.1*dt*(t_ref_new - self.t_ref[i])

    def print_setpoints(self):
        print(['%.2f' % t for t in self.t_ref])

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

