# -*- coding: utf-8 -*-

from core import *
from csv import reader
from pandas.io.parsers import read_csv


def circle( self, r, n ):
    points = []

    for t in range( 0, int(2*pi) ):
        x = r * cos(t)
        y = r * sin(t)
        points.append( [x,y] )

    return points




class Representation( Element ):


    def get_circle( self, r, n ):
        points = []

        t = [ (i * ( (2*pi) / float(n) )) for i in range( 0, n ) ]

        for i in t:
            x = r * cos(i)
            y = r * sin(i)
            points.append( [x,y] )

        return points


    def create_linear( self ):
        data    =   self.p.get( 'values' )
        n       =   self.p.get( 'number_of_segments' )
        height  =   self.p.get( 'segment_height' )
        base_radius = self.p.get('base_radius')

        # calculate step
        if len(data) > n:
            step = int( len(data) / float(n) )
        else:
            step = 1

        filtered_data = data[::step]

        current_height = 0.0

        segments = []

        for v in filtered_data:
            segments.append(
                up(current_height) (
                    cylinder(
                        h=height,
                        r=((1.0 + v) * base_radius ),
                        center=True
                    )
                )
            )

            current_height += height


        return union() ( *segments )


    def create(self):
        data    =   self.p.get( 'values' )
        n       =   self.p.get( 'number_of_segments' )
        height  =   self.p.get( 'segment_height' )
        base_radius = self.p.get('base_radius')

        tick = 360.0 / n


        # calculate step
        if len(data) > n:
            step = int( len(data) / float(n) )
        else:
            step = 1

        filtered_data = data[::step]

        current_height = 0.0
        current_angle = 0.0

        segments = []

        positions = self.get_circle(
            self.p.get('circle_radius'), n
        )

        for (v, pos) in zip( filtered_data, positions ):
            segments.append(
                translate([ 0, pos[0], pos[1] ]) (
                    rotate( current_angle, [1, 0, 0] ) (
                        cylinder(
                            h=height,
                            r=( (1.0 + v) * base_radius ),
                            center=True
                        )
                    )
                )
            )

            current_height += height
            current_angle += tick


        return union() ( *segments )




if __name__ == "__main__":

    sys.setrecursionlimit( 12000 )

    with open( 'data.txt', 'rb' ) as source:
        data = read_csv(
            source,
            header=None,
            names=[
                'clock',
                'millis',
                'accel_x', 'accel_y', 'accel_z',
                'gyro_x', 'gyro_y', 'gyro_z',
                'magn_x', 'magn_y', 'magn_z' ]
        )

    acceleration = data[['accel_x', 'accel_y', 'accel_z']].copy()


    acceleration = acceleration[1250:3250]

    # calculates total acceleration from three axes
    total_acceleration = []
    for (x,y,z) in acceleration.values:
        total_acceleration.append(
            sqrt( pow(x,2) + pow(y,2) + pow(z,2) )
        )


    # find the working range for the total acceleration set

    interval = (
        min( total_acceleration ),
        max( total_acceleration )
    )

    data_range = interval[1] - interval[0]

    # print the range of values
    print "Data interval:", interval
    print "Range:", data_range

    # scale the data to the range
    scaled_total_acceleration = [
        (float(a) / data_range) for a in total_acceleration
    ]

    e = Representation(
        Size(1,1,1),
        parameters={
            "number_of_segments": 72,
            "base_radius": 25.0,
            "values": scaled_total_acceleration,
            "segment_height": 1.0,
            "circle_radius": 100.0
        }
    )


    e.create()

    scad_render_to_file( e.put(), "project.scad" )