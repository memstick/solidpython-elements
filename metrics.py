# -*- coding: utf8 -*-

from math import sqrt

class Metric:
    def center( self, axis=None ):
        return self.half( axis )

    def half( self, axis=None ):
        """alias of center"""
        return self.divide( axis, 2 )

    def third( self, axis ):
        return self.divide( axis, 3 )

    def quarter( self, axis ):
        return self.divide( axis, 4 )

    def divide( self, axis, divisor ):
        """
        Returns a centerpoint between n equal parts.
        """

        x = self.x / float(divisor)
        y = self.y / float(divisor)
        z = self.z / float(divisor)

        if axis:
            if axis.lower() == 'x':
                return x
            elif axis.lower() == 'y':
                return y
            elif axis.lower() == 'z':
                return z
            else:
                raise Error(
                    'The requested axis >>> {axis} <<< was not found'.format(
                        axis=axis
                    )
                )
        else:
            return Position( x, y, z )

    def partition( self, n, axis=None ):
        pass


    def __call__( self, container_type=list ):
        if container_type is list:
            return [ self.x, self.y, self.z ];


    def __getitem__( self, item ):
        x, y, z = 'x', 'y', 'z'

        if item.lower() == x:
            return self.x
        elif item.lower() == y:
            return self.y
        elif item.lower() == z:
            return self.z
        else:
            raise Error( "Requested axis >>> {axis} <<< was not found".format(
                axis=item
            )
            )

    def __str__( self ):
        return "[{self.x}, {self.y}, {self.z}]".format( self=self )

    def __repr__( self ):
        return "[{self.x}, {self.y}, {self.z}]".format( self=self )

class Size( Metric ):
    def __init__( self, x=None, y=None, z=None ):
        # default size definitions
        self.x = x if x else 1.0
        self.y = y if y else 1.0
        self.z = z if z else 1.0

    def diagonal( self, dimensions=2 ):
        if dimensions == 2:
            return sqrt( self.x**2 + self.y**2 )
        else:
            return sqrt( self.x**2 + self.y**2 + self.z**2 )

    def stretch( self, x=None, y=None, z=None ):
        self.x = (self.x * x) if x else self.x
        self.y = (self.y * y) if y else self.y
        self.z = (self.z * z) if z else self.z

class Position( Metric ):
    def __init__( self, x=None, y=None, z=None ):
        self.x = x if x else 0.0
        self.y = y if y else 0.0
        self.z = z if z else 0.0

class Distance( Metric ):
    def __init__( self, x=None, y=None, z=None ):
        self.x = x if x else 0.0
        self.y = y if y else 0.0
        self.z = z if z else 0.0