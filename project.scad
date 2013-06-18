

translate(v = [0, 0, 0]) {
	union() {
		translate(v = [0, 0, 0]) {
			difference() {
				cylinder(h = 5, r = 8.0000000000, center = true);
				cylinder(h = 5, r = 2, center = true);
			}
		}
		translate(v = [0, 0, 5]) {
			difference() {
				cylinder(h = 5, r = 11.6000000000, center = true);
				cylinder(h = 5, r = 2, center = true);
			}
		}
		translate(v = [0, 0, 10]) {
			difference() {
				cylinder(h = 5, r = 15.2000000000, center = true);
				cylinder(h = 5, r = 2, center = true);
			}
		}
		translate(v = [0, 0, 15]) {
			difference() {
				cylinder(h = 5, r = 18.8000000000, center = true);
				cylinder(h = 5, r = 2, center = true);
			}
		}
		translate(v = [0, 0, 20]) {
			difference() {
				cylinder(h = 5, r = 22.4000000000, center = true);
				cylinder(h = 5, r = 2, center = true);
			}
		}
		translate(v = [0, 0, 25]) {
			difference() {
				cylinder(h = 5, r = 26.0000000000, center = true);
				cylinder(h = 5, r = 2, center = true);
			}
		}
	}
}
/***********************************************
******      SolidPython code:      *************
************************************************
 
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
 
***********************************************/
                            
