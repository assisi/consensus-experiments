#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assisipy import casu

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

