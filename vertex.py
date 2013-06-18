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

    def create_edges( self ):
        edges = []


        for angle in self.get_edge_ends():
            edges.append(
                rotate( angle, [0,0,1] ) (
                    translate( [0, self.s.half('y'), 0] ) (
                        union() (
                            cube(
                                [ self.s.x, self.s.y, self.s.z ],
                                center=True
                            ),

                            translate([0, self.s.half('y'), 0]) (
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
<<<<<<< HEAD
            self.create_edges()
=======
            self.create_edges( length_factor=1 )
>>>>>>> 35492df303f9d3734a3d62acd3cc389b225acb37
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

        centerpiece_factor = \
            self.p.get('centerpiece_radius') / \
            float( self.size.x + self.p.get('centerpiece_radius') )

        cf = centerpiece_factor
        isp = self.p.get('inlay_size_proportion')

        # rotation for the number of edges
        r = 180.0 / self.p.get("number_of_edges")

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
            ),
            difference() (
                # the hole to accomodate inlay
                rotate(r, [0, 0, -1]) (
                    scale([cf, cf, self.s.z]) (
                        self.create_contours()
                    )
                ),
                # the inlay
                rotate(r, [0, 0, -1]) (
                    scale([cf / isp, cf / isp, self.s.z]) (
                        self.create_contours()
                    )
                ),
            )
        )




if __name__ == "__main__":
<<<<<<< HEAD
    v = Vertex( Size( 13, 35, 5 ), parameters = {
        'number_of_edges': 5,
        'centerpiece_radius': 10.0,
        'wall_thickness': 2.0,
        'mesh_thickness': 2.0,
        'mesh_spacing': 5.0,
        'mesh_angle': 45
=======
    v = Vertex( Size( 15, 35, 1 ), parameters = {
        'number_of_edges': 5,
        'centerpiece_radius': 5.0,
        'wall_thickness': 2.0,
        'mesh_thickness': 3.5,
        'mesh_spacing': 10.0,
        'mesh_angle': 45,
        'inlay_size_proportion': 1.614
>>>>>>> 35492df303f9d3734a3d62acd3cc389b225acb37
    })


    v.create()

    scad_render_to_file( v.put(), "project.scad" )