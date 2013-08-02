#! /usr/bin/python
# -*- coding: utf-8 -*- 

from core import *


class Inlay( Element ):

    def get_base_height(self):
        return self.p.get( 'bottom-height' ) / 2.0

    def create_top(self):
        height = self.p.get( 'bottom-height' ) + self.p.get( 'separator-height' )

        cyl1 = up(10)(
                rotate(90, [1,0,0]) (
                    cylinder(0.64, 30)
                    )
                )

        cyl2 = up(10)(
                right(1.74)(
                    rotate(90, [1,0,0]) (
                        cylinder(0.64, 30)
                        )
                    )
                )



        cyl3 = up(10)(
                right(3.5)(
                    rotate(90, [1,0,0]) (
                        cylinder(0.64, 30)
                        )
                    )
                )


        
        cyl4 = up(10)(
                right(5.23)(
                    rotate(90, [1,0,0]) (
                        cylinder(0.64, 30)
                        )
                    )
                )

        cyls = union()(cyl1, cyl2, cyl3, cyl4)

        cyls = down()

        form =  difference() (
                back(15)(
                    cube(
                        [ self.p.get('top-width'),
                            self.p.get('top-length') + 30.0,
                            self.p.get('top-height') ], center=True )),
                        self.create_bottom_hole()
                        )

        return up(height) (union()(form, cyls))

    def create_bottom_hole( self ):
        height = self.get_base_height()

        return up( height ) ( 
                        cube(
                            [ self.p.get('bottom-width'), self.p.get('bottom-length'), self.p.get('bottom-height') ],
                            center=True
                        ), 
                    )

    def create_separator( self ):
        height =  self.p.get('bottom-height')

        return up( height ) (
            cube(
                [ self.p.get('top-width'),
                  self.p.get('top-length'),
                  self.p.get('serparator-height') ], center=True )
        )

    def create_bottom( self ):
        height = self.get_base_height()

        c1 = cube(
                [ self.p.get('bottom-width'), self.p.get('bottom-length'), self.p.get('bottom-height') ],
                center=True
                )

        c2 = left(11.5) (
                up(1)(
                    cube( 
                        [ self.p.get('bottom-wire-width'), self.p.get('bottom-length'), self.p.get('bottom-wire-height'),], 
                        center=True
                        )
                    )
                )

        c3 = left(self.p.get('bottom-conn-off')) (
                up(self.p.get('bottom-conn-base-height'))(
                    back(29.0)(
                        cube(
                            [ self.p.get('bottom-conn-width'), self.p.get('bottom-conn-length'), self.p.get('bottom-conn-height')],
                            center=True
                        )
                    )
                )
            )


        return up( height ) ( 
                difference() (
                    c1, 
                    union()(c2, c3)
                )
            )

    def create( self ):
        top = self.create_top()
        bottom = self.create_bottom()
        separator = self.create_separator()

        return top

#        return union() (
#            top,
#            separator,
#            bottom
#        )




if __name__ == "__main__":

    e = Inlay(
        Size(1,1,1),
        parameters = {
            'top-height': 8.0,
            'top-width': 60.0,
            'top-length': 70.0,
            'separator-height': 1.0,
            'bottom-height': 6.0,
            'bottom-width': 47.0,
            'bottom-length': 59.0,
            'bottom-wire-width': 9.0,
            'bottom-wire-height': 5.0,
            'bottom-conn-off': 11.81,
            'bottom-conn-width': 10.5,
            'bottom-conn-base-height': 1,
            'bottom-conn-height':6.0,
            'bottom-conn-length':4.0
        }
    )

    scad_render_to_file( e.put(), "project.scad" )
