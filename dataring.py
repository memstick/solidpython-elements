# -*- coding: utf-8 -*-

from core import *
from csv import reader
from pandas.io.parsers import read_csv


class Representation( Element ):
    def create(self):
        return cube(5, center=True)



if __name__ == "__main__":


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

    range = interval[1] - interval[0]

    # print the range of values
    print "Data interval:", interval
    print "Range:", range

    # scale the data to the range
    scaled_total_acceleration = [
        (float(a) / range) for a in total_acceleration
    ]

    print scaled_total_acceleration[0:50]


    e = Representation(
        Size(1,1,1),
        parameters={
            "segments": 720,
            "values": data
        }
    )

    e.create()

    scad_render_to_file( e.put(), "project.scad" )