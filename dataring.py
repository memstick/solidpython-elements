# -*- coding: utf-8 -*-

from core import *
from csv import reader
from pandas.io.parsers import read_csv


class Representation( Element ):
    def create(self):
        return cube(5, center=True)



if __name__ == "__main__":

    e = Representation(
        Size(1,1,1),
        parameters={
            "a": 1
        }
    )


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

    print data[['accel_x', 'accel_y', 'accel_z']].copy().head()



    e.create()

    scad_render_to_file( e.put(), "project.scad" )