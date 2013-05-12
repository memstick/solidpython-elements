

translate(v = [0, 0, 0]) {
	difference() {
		union() {
			color(c = "red") {
				cube(center = true, size = [36.5000000000, 80.5000000000, 1]);
			}
			color(c = "blue") {
				cube(center = true, size = [27.2, 72, 1.0]);
			}
		}
		color(c = "green") {
			cylinder(r = [37.7500000000, 15.7500000000, 1]);
			cylinder(r = [-37.7500000000, 15.7500000000, 1]);
			cylinder(r = [37.7500000000, -15.7500000000, 1]);
			cylinder(r = [-37.7500000000, -15.7500000000, 1]);
		}
	}
}
/***********************************************
******      SolidPython code:      *************
************************************************
 
# -*- coding: utf-8 -*- 

from core import *
from metrics import *

from elements import PerforatedSection



class KrydderinoDisplayCase( Element ):
    def create(self):

        screen_area_size = self.parameters.get('screen_area_size')
        hole_area_size =  self.parameters.get('hole_area_size')


        # pcb area
        pcb = cube( self.size(), center=True )

        # screen area
        screen = cube( screen_area_size, center=True )

        # holes
        holes = []

        hole_coordinates = [
            ( hole_area_size.x / 2.0, hole_area_size.y / 2.0 ),
            ( -hole_area_size.x / 2.0, hole_area_size.y / 2.0 ),
            ( hole_area_size.x / 2.0, -hole_area_size.y / 2.0 ),
            ( -hole_area_size.x / 2.0, -hole_area_size.y / 2.0 )
        ]

        for x,y in hole_coordinates:
            holes.append( cylinder([x, y, self.size.z]) )




        bottom = union() (
            color("red") (pcb),
            color("blue") (screen),
        )

        bottom = difference() (
            bottom,
            color("green") (holes)
        )



        return bottom



if __name__ == "__main__":
    e = KrydderinoDisplayCase(
        Size( 36.5, 80.5, 1 ),
        parameters = {
            "screen_area_size": Size( 27.2, 72 ),
            "hole_diameter": 2.5,
            "hole_area_size": Size( 75.5, 31.5 )

        }
    )

    scad_render_to_file( e.put(), "project.scad" ) 
 
***********************************************/
                            
