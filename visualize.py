# -*- coding: utf8 -*- 

from core import *



class Path(Element):
    def create( self ):

        timestamps = []
        vectors = []
        angles = []

        with open( "speedmonster.txt" ) as data:
            data = data.read().split('\n')
            data = data[::self.p.get("shrink_factor")] # select every nth line

            for l in data:
                current_line = l.split(',')
                timestamps.append( current_line[0:2] )
                angles.append( current_line[2:5] )

        print len( timestamps ), len( vectors ), len( angles )

        angles = [(float(x),float(y),float(z)) for (x,y,z) in angles]

        """
        arrows = []
        vel = [0, 0, 0]
        pos = [0, 0, 0]

        prev_pos = [0, 0, 0]

        mm = [ max([int(i), int(j), int(k)]) for (i, j, k) in vectors ]
        abs_max = max(mm)

        for i in range( 1, len(vectors) -1 ):
            previous_vector = vectors[i-1]
            current_vector = vectors[i]

            px, py, pz = [int(i) for i in previous_vector]
            x,y,z = [int(i) for i in current_vector]

            vel[0] += x
            vel[1] += y
            vel[2] += z

            pos[0] += vel[0]
            pos[1] += vel[1]
            pos[2] += vel[2]

            dpos = [
                pos[0] - prev_pos[0],
                pos[1] - prev_pos[1],
                pos[2] - prev_pos[2]
            ]


            print pos

            arrows.append(
                translate([pos[0], pos[1], pos[2]]) (
                    scale([dpos[0],dpos[1],dpos[2]]) (cube(1))
                )
            )

            prev_pos = pos
            """

        supports = []
        for (x,y,z) in angles:
            supports.append(
                rotate([x,y,z]) (
                    cube([1,10,1])
                )
            )

        return union() (*supports)

    def get_point_could( self ):
        pass




if __name__ == "__main__":

    p = Path(
        Size( 15, 35, 1 ), parameters = {
            "scale_factor": 1,
            "filename": "speedmonster.txt",
            "shrink_factor": 5
        }
    )

    p.create()

    scad_render_to_file( p.put(), "project.scad" )