# -*- coding: utf8 -*- 

from solid import *
from solid.utils import *


def partition( m, n ):

    result = []
    p = m / float(n)

    for i in range(n+1):
        result.append( p*i )
    return result







class Element:
    def __init__( self, size, parameters=None, *args, **kwargs ):
        """
        The constructor accepts the parameters common
        to all element children. It can also accept
        a dictionary of keyword-parameters (like
        hole_radius for hole element).
        """
        self.size = size
        self.parameters = parameters

    def create( self ):
        pass

    def put( self, position=None ):
        position = position if position else [0, 0, 0]
        return translate(position) (
            self.create()
        )
