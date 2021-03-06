# -*- coding: utf8 -*- 

from solid import *
from solid.utils import *


from metrics import *

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

        self.s = self.size
        self.p = self.parameters

        self.sz = self.size
        self.prmtrs = self.parameters

    def create( self ):
        pass

    def put( self, position=None ):
        position = position if position else [0, 0, 0]
        return translate(position) (
            self.create()
        )


class Parameters:
    def __init__( self, elements, default=0.0 ):
        self.elements = elements
        self.default = default

    def __getitem__( self, name ):
        if self.elements.get('name'):
            return self.elements['name']
        else:
            print "Warning, the '{0}' property was not found, defaults to {1}.".format(
                name, self.default )
            return self.default
