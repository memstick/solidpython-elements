

translate(v = [0, 0, 0]) {
	difference() {
		scale(v = [1, 1, 10.0000000000]) {
			difference() {
				union() {
					color(c = "red") {
						cube(center = true, size = [36.5000000000, 80.5000000000, 1]);
					}
					color(c = "yellow") {
						union() {
							translate(v = [15.7500000000, 37.7500000000, 0]) {
								cylinder(h = 1, r = 5.0000000000, center = true);
							}
							translate(v = [-15.7500000000, 37.7500000000, 0]) {
								cylinder(h = 1, r = 5.0000000000, center = true);
							}
							translate(v = [15.7500000000, -37.7500000000, 0]) {
								cylinder(h = 1, r = 5.0000000000, center = true);
							}
							translate(v = [-15.7500000000, -37.7500000000, 0]) {
								cylinder(h = 1, r = 5.0000000000, center = true);
							}
							cube(center = true, size = [41.5000000000, 75.5000000000, 1]);
							cube(center = true, size = [31.5000000000, 85.5000000000, 1]);
						}
					}
				}
				color(c = "blue") {
					cube(center = true, size = [27.2000000000, 72, 2.0000000000]);
				}
				color(c = "green") {
					union() {
						translate(v = [15.7500000000, 37.7500000000, 0]) {
							cylinder(h = 1, r = 1.2500000000, center = true);
						}
						translate(v = [-15.7500000000, 37.7500000000, 0]) {
							cylinder(h = 1, r = 1.2500000000, center = true);
						}
						translate(v = [15.7500000000, -37.7500000000, 0]) {
							cylinder(h = 1, r = 1.2500000000, center = true);
						}
						translate(v = [-15.7500000000, -37.7500000000, 0]) {
							cylinder(h = 1, r = 1.2500000000, center = true);
						}
					}
				}
			}
		}
		translate(v = [0, 0, 1]) {
			cube(center = true, size = [36.5000000000, 80.5000000000, 10.0000000000]);
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

    def create_rounded_frame( self, corner_offset, hole_diameter, hole_coordinates ):
        corners = []
        walls = []
        for x,y in hole_coordinates:
            corners.append(
                translate( [x, y, 0] ) (
                    cylinder(
                        corner_offset,
                        self.size.z,
                        center=True
                    )
                )
            )

        walls = [
            cube(
                [
                    self.size.x + (hole_diameter * 2),
                    self.size.y - (hole_diameter * 2),
                    self.size.z
                ],
                center=True
            ),

            cube(
                [
                    self.size.x - (hole_diameter * 2),
                    self.size.y + (hole_diameter * 2),
                    self.size.z
                ],
                center=True
            )
        ]

        return union() ( corners, walls )


    def create(self):

        total_height = self.parameters.get('total_height')
        screen_area_size = self.parameters.get('screen_area_size')
        hole_area_size =  self.parameters.get('hole_area_size')
        hole_diameter = self.parameters.get('hole_diameter')
        front_thickness = self.parameters.get('front_thickness')

        self.size.z = 1

        # pcb area
        pcb = cube( self.size(), center=True )

        # screen area
        screen = cube([
                screen_area_size.x,
                screen_area_size.y,
                screen_area_size.z + 1],
            center=True )

        # holes
        holes = []

        hole_coordinates = [
            ( hole_area_size.y / 2.0, hole_area_size.x / 2.0 ),
            ( - hole_area_size.y / 2.0, hole_area_size.x / 2.0 ),
            ( hole_area_size.y / 2.0, -hole_area_size.x / 2.0 ),
            ( - hole_area_size.y / 2.0, -hole_area_size.x / 2.0 )
        ]
        # [  1,  1 ]
        # [ -1,  1 ]
        # [  1, -1 ]
        # [ -1, -1 ]

        for x,y in hole_coordinates:
            holes.append(
                translate( [x, y, 0] ) (
                    cylinder(
                        hole_diameter / 2.0,
                        self.size.z,
                        center=True
                    )
                )
            )

        holes = union() ( *holes )


        bottom = union() (
            color("red") (pcb),
            color("yellow") (
                self.create_rounded_frame(
                    hole_diameter * 2,
                    hole_diameter,
                    hole_coordinates
                )
            )
        )


        bottom = difference() (
            bottom,
            color("blue") (screen),
            color("green") (holes)
        )


        # create walls
        body = scale([1, 1, total_height]) ( bottom )

        body_hull = translate([0,0,self.size.z]) (
            cube( [
                    self.size.x,
                    self.size.y,
                    total_height
                ],
                center=True
            )
        )

        body = difference() ( body, body_hull )

        return body



if __name__ == "__main__":
    e = KrydderinoDisplayCase(
        Size( 36.5, 80.5, 1 ),
        parameters = {
            "screen_area_size": Size( 27.2, 72 ),
            "hole_diameter": 2.5,
            "hole_area_size": Size( 75.5, 31.5 ),
            "front_thickness": 5.0,
            "total_height": 10.0
        }
    )

    scad_render_to_file( e.put(), "project.scad" ) 
 
***********************************************/
                            
