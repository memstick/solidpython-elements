

translate(v = [0, 0, 0]) {
	cube(size = [101.6000000000, 53.3000000000, 1.0000000000]);
}
/***********************************************
******      SolidPython code:      *************
************************************************
 
# -*- coding: utf8 -*-

from core import *



class Enclosure( Element ):
    def create( self ):
        return cube( [ self.s.x, self.s.y, self.s.z ] )



if __name__ == "__main__":

    e = Enclosure(
        Size( 101.6, 53.3, 1.0 ),
        parameters={
            "": 1.0
        }
    )

    e.create()

    scad_render_to_file( e.put(), "project.scad" ) 
 
***********************************************/
                            
