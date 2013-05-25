# -*- coding: utf-8 -*-

from core import *


class Vertex(Element):

    def get_edge_ends( self ):
        unit = 360.0 / self.p.get('number_of_edges')

        return [ i * unit for i in range(self.p.get('number_of_edges') ) ]


    def create_centerpiece(self):
        return cylinder(
            r=self.prmtrs.get('centerpiece_radius'),
            h=self.s.z,
            center=True
        )

    def create_edges(self, length_factor=1):
        edges = []

        for angle in self.get_edge_ends():
            edges.append(
                rotate( angle, [0,0,1] ) (
                    translate( [0, self.s.half('y') * length_factor, 0] ) (
                        union() (
                            cube(
                                [ self.s.x, self.s.y * length_factor, self.s.z ],
                                center=True
                            ),

                            translate([0, self.s.half('y') * length_factor, 0]) (
                                cylinder(
                                    self.s.half('x'),
                                    self.s.z,
                                    center=True
                                )
                            )
                        )
                    )
                )
            )

        return union() ( *edges )


    def create_contours(self):

        return union() (
            self.create_centerpiece(),
            self.create_edges()
        )

    def create_inner_contours(self):

        return union() (
            self.create_centerpiece(),
            self.create_edges( length_factor=1.2 )
        )

    def create_angle( self ):

        angle_anchor = self.s.quarter('y') - ( self.p.get('mesh_thickness') / 2.0 )

        return union() (
            rotate( self.p.get('mesh_angle'),[0, 0, 1] ) (
                translate( [0, angle_anchor, 0] ) (
                    cube( [ self.p.get('mesh_thickness'), self.s.half('y'), self.s.z], center=True )
                )
            ),

            rotate( self.p.get('mesh_angle'), [0, 0, -1]) (
                translate( [0, angle_anchor, 0] ) (
                    cube( [ self.p.get('mesh_thickness'), self.s.half('y'), self.s.z], center=True )
                )
            )
        )

    def create_edge_mesh( self ):
        angles = []
        offset = self.p.get('centerpiece_radius')

        for i in range( self.s.y ):
            angles.append(
                translate( [ 0, offset, 0 ] ) (
                    self.create_angle()
                )
            )
            offset += self.p.get('mesh_spacing')

        return union() (
            *angles
        )


    def create_inner_mesh(self):

        centerpiece = self.create_centerpiece()

        edges = []

        for angle in self.get_edge_ends():
            edges.append(
                rotate( angle, [0,0,1] ) (
                    self.create_edge_mesh()
                )
            )

        return intersection() (
            difference() (
                union() (
                    *edges
                ),
                centerpiece
            ),
            self.create_inner_contours()
        )


    def get_inner_factor(self):
        return abs( float( self.s.x - self.p.get('wall_thickness') * 2 ) / self.s.x )


    def create( self ):

        factor = self.get_inner_factor()

        return union() (
            # the inner mesh
            scale( [factor, factor, 1] ) (
                self.create_inner_mesh()
            ),
            # the wall-size contour extrusion
            difference() (
                self.create_contours(),
                scale( [factor, factor, 1] ) (
                    self.create_inner_contours()
                )
            )
        )




if __name__ == "__main__":
    v = Vertex( Size( 10, 15, 5 ), parameters = {
        'number_of_edges': 3,
        'centerpiece_radius': 5.0,
        'wall_thickness': 0.5,
        'mesh_thickness': 0.5,
        'mesh_spacing': 3.0,
        'mesh_angle': 45
    })


    v.create()

    scad_render_to_file( v.put(), "project.scad" )