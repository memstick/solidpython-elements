

translate(v = [0, 0, 0]) {
	union() {
		rotate(a = 0.0000000000, v = [0, 1, 0]) {
			translate(v = [0, 50.0000000000, 0.0000000000]) {
				cylinder(h = 0.5000000000, r = 36.1920641476, center = true);
			}
		}
		rotate(a = 1.0000000000, v = [0, 1, 0]) {
			translate(v = [0, 27.0151152934, 42.0735492404]) {
				cylinder(h = 0.5000000000, r = 36.5144392636, center = true);
			}
		}
		rotate(a = 2.0000000000, v = [0, 1, 0]) {
			translate(v = [0, -20.8073418274, 45.4648713413]) {
				cylinder(h = 0.5000000000, r = 36.8190022839, center = true);
			}
		}
		rotate(a = 3.0000000000, v = [0, 1, 0]) {
			translate(v = [0, -49.4996248300, 7.0560004030]) {
				cylinder(h = 0.5000000000, r = 36.4299700549, center = true);
			}
		}
		rotate(a = 4.0000000000, v = [0, 1, 0]) {
			translate(v = [0, -32.6821810432, -37.8401247654]) {
				cylinder(h = 0.5000000000, r = 36.5824714476, center = true);
			}
		}
		rotate(a = 5.0000000000, v = [0, 1, 0]) {
			translate(v = [0, 14.1831092732, -47.9462137332]) {
				cylinder(h = 0.5000000000, r = 36.5610386722, center = true);
			}
		}
	}
}
/***********************************************
******      SolidPython code:      *************
************************************************
 
# -*- coding: utf-8 -*-

from core import *
from csv import reader
from pandas.io.parsers import read_csv


sys.setrecursionlimit(12000)


class Representation( Element ):


    def get_circle( self, r, n ):
        points = []

        for t in range( 0, int(2*pi) ):
            x = r * cos(t)
            y = r * sin(t)
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
                rotate( current_angle, [0, 1, 0] ) (
                    translate([ 0, pos[0], pos[1] ]) (
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


    from pandas import DataFrame
    import matplotlib.pyplot as plt

    """
    p = DataFrame( scaled_total_acceleration )
    p.plot()
    plt.show()
    """


    e = Representation(
        Size(1,1,1),
        parameters={
            "number_of_segments": 360,
            "base_radius": 25.0,
            "values": scaled_total_acceleration,
            "segment_height": 0.5,
            "circle_radius": 50.0
        }
    )


    e.create()

    scad_render_to_file( e.put(), "project.scad" ) 
 
***********************************************/
                            
