#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assisipy import casu

def estimate_numbees(readings):
    """
    Bee density estimator.
    """
    numbees = 0

    return numbees

def update(casu_id, zeta, A, numbees, dt):
    """
    Update the zeta matrix, based on neighbors' data
    and bee density estimate.
    """
    i = casu_id - 1
    
    for j in range (n):
        
        dzeta1 = 0
        dzeta2 = 0
        for k in range (n):
            dzeta1 += A[i][k]*zeta[-2][i][k]*(zeta[-2][k][j]-zeta[-2][i][j])
            #print("nbg(%d)=%d" %(k, nbg[k]))
            #print("dzeta1(%d, %d)=%f" %(j, k, dzeta1))
            #print('dzeta1={0}'.format(dzeta1))
            #import ipdb; ipdb.set_trace()
        
        """ Include IR detection"""
        if i == j:                
            dzeta2 = numbees/6.0 - zeta[-2][i][i]
            #print('dzeta2={0}'.format(dzeta2))
            #print("dzeta2(%d)=%f" %(i, dzeta2))           
        
        
        zeta[-1][i][j] = zeta[-2][i][j] + dt*(dzeta1 + dzeta2)

    return zeta

def compute_setpoint(casu_id, zeta, A, x):
    """
    Compute temperature sensor setpoints
    from zeta matrix.
    """
    i = casu_id - 1
    zeta_i_max = max(zeta[-2][i])   #zeta in step k
    i_leader = 0
    x_nbg_i_max = 0
    for j in range (n):
        #CASUi is a leader if its zeta is max
        if (i==j) and (zeta[-2][i][j]==zeta_i_max):
            setpoint = 36
            i_leader = 1
        elif (i_leader == 0) and (A[i][j] == 1) and (x_nbg_i_max < x[j]):
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
    Td = 0.1
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
    readings = [0,3,0,0,0,0,0,5,0]
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
    
    """ Main loop """
    t = 0
    while t<Texp:
        zeta.append([[0 for a in row] for row in zeta[-1]])        
        for index in range (n):    #for loop is used for debugging 
            """ Read zeta from neighbours and copy to zeta[ngb_id-1] """
            #zeta[i] = nbg_data[i]
            nbg = A[index]
            numbees = readings[index] 
            casu_id = index+1
            """ Update zeta """
            zeta = update(casu_id, zeta, A, numbees, Td)
             
            """ Read temperature from neighbours - x(index) = [temp1, ..., temp9] """
            #x = read_nbg_temp
            uref = compute_setpoint(casu_id, zeta, A, x)

            """ Reference filter """
            x[index] += 0.1*Td*(uref - x[index])

        t += Td     

  
    """ Debug print """
    for row in zeta[-1]:
        row_formated = [ '%.3f' % elem for elem in row ]
        print (row_formated)
    
    x_formated = [ '%.2f' % elem for elem in x ]
    print('Temperature=')
    print(x_formated)


