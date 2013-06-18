# -*- coding: utf-8 -*- 

from core import *

class Tower( Element ):

    def get_ring_size_distribution( self ):
        n           = self.p.get('number_of_rings')
        largest     = self.parameters.get( 'largest_radius' )
        smallest    = self.parameters.get( 'smallest_radius' )

        increment = ( largest - smallest ) / float( self.p.get('number_of_rings') - 1 )

        return [ smallest + ( i*increment ) for i in range( 0, n ) ]


    def create_ring( self, radius ):

        return difference() (
            cylinder( radius, self.p.get('ring_height'), center = True ),
            cylinder( self.p.get('hole_radius'), self.p.get('ring_height'), center = True )
        )

    def create( self ):

        rings = []

        for i,r in enumerate(self.get_ring_size_distribution()):
            rings.append(
                translate( [0, 0, i * self.p.get('ring_height')] ) (
                    self.create_ring( r )
                )
            )

        return union() ( *rings )

if __name__ == "__main__":

    t = Tower( Size( 0, 0, 0 ),  parameters = {
        'ring_height': 5,
        'smallest_radius': 8,
        'largest_radius': 26,
        'number_of_rings': 6,
        'hole_radius': 2
    })


    t.create()

    scad_render_to_file( t.put(), "project.scad" )