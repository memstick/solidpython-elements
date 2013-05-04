from solid import *
from solid.utils import *
import doctest

from math import sqrt

class Metric:
    def center( self, axis=None ):
        return self.half( axis )
    
    def half( self, axis=None ):
        """alias of center"""
        return self.divide( axis, 2 )
        
    def third( self, axis ):
        return self.divide( axis, 3 )

    def quarter( self, axis ):
        return self.divide( axis, 4 )
    
    def divide( self, axis, divisor ):
        """
        Returns a centerpoint between n equal parts.
        """
    
        x = self.x / float(divisor)
        y = self.y / float(divisor)
        z = self.z / float(divisor)
        
        if axis:
            if axis.lower() == 'x':
                return x
            elif axis.lower() == 'y':
                return y
            elif axis.lower() == 'z':
                return z
            else:
                raise Error( 'The requested axis >>> {axis} <<< was not found'.format( axis=axis ) )
        else:
            return Position( x, y, z )
            

    def __call__( self, container_type=list ):
        if container_type is list:
            return [ self.x, self.y, self.z ];

            
    def __getitem__( self, item ):
        x, y, z = 'x', 'y', 'z'
        
        if item.lower() == x:
            return self.x
        elif item.lower() == y:
            return self.y
        elif item.lower() == z:
            return self.z
        else:
            raise Error( "Requested axis >>> {axis} <<< was not found".format(axis=item) )
            
    def __str__( self ):
        return "[{self.x}, {self.y}, {self.z}]".format( self=self )
    
    def __repr__( self ):
        return "[{self.x}, {self.y}, {self.z}]".format( self=self )

class Position( Metric ):
    def __init__( self, x=None, y=None, z=None ):
        self.x = x if x else 0.0
        self.y = y if y else 0.0
        self.z = z if z else 0.0

        
class Size( Metric ):
    def __init__( self, x=None, y=None, z=None ):
        # default size definitions
        self.x = x if x else 1.0
        self.y = y if y else 1.0
        self.z = z if z else 1.0

    def diagonal( self, dimensions=2 ):
        if dimensions == 2:
            return sqrt( self.x**2 + self.y**2 )
        else:
            return sqrt( self.x**2 + self.y**2 + self.z**2 )
    
    def stretch( self, x=None, y=None, z=None ):
        self.x = (self.x * x) if x else self.x
        self.y = (self.y * y) if y else self.y
        self.z = (self.z * z) if z else self.z
        

class Element:
    def __init__( self, size ):
        self.size = size
    
    def create( self ):
        pass
    
    def put( self, position=None ):
        position = position if position else [0, 0, 0]
        return translate(position) ( 
            self.create() 
        )

        
class Plate( Element ):
    def create_plate( self ):
        return cube( self.size() )

    def create( self ):
        return create_plate()
        
        

class PerforatedPlate( Plate ):
    def __init__( self, size, hole_radius=None ):
        Plate.__init__( self, size )
        self.hole_radius = hole_radius if hole_radius else 1.0

    def create_hole( self, radius=None, depth=None ):
        depth = depth if depth else self.size.z
        radius = self.hole_radius
        return cylinder( radius, depth)

    def create( self, position=None ):
        return difference() (
            # the solid part
            self.create_plate(),
            # the hole through the solid part
            # translated to the center of x/y-axes
            translate( [self.size.center('x'), self.size.center('y'), 0] ) (
                self.create_hole()
            )
        )
        


class PerforatedRoundedPlate( PerforatedPlate ):
    def __init__( self, size, hole_radius=None ):
        PerforatedPlate.__init__( self, size, hole_radius )
    
    def create_plate( self, reverse=False ):    
        depth =  self.size.z
        radius = self.size.center('y')
        
        result = difference() (
            cube( self.size() ),
            translate( [self.size.half('x'), 0, 0] ) (
                cube( [ self.size.x, self.size.y, self.size.z ] )
            )
        )
        
        return union() (
            result,
            translate( [self.size.half('x'), self.size.half('y'), 0] ) (
                cylinder( radius, depth )
            )
        )    


class PerforatedSection( Element ):
    def __init__( self, length=10, unit=20, hole_radius=5 ):
        # the length is calculated from the center of 
        # the center of the opposite hole
        self.length = length - unit # (lenght - 2 * (unit/2))
        self.unit = unit
        self.e1 = PerforatedRoundedPlate( Size( unit, unit, 1 ), hole_radius )
        self.e2 = PerforatedRoundedPlate( Size( unit, unit, 1 ), hole_radius )
        
    def create_bridge( self ):
        return translate([-self.length,0,0]) (
            cube([self.length, self.unit, 1])
        )
    
    def create( self, position=None ):        
        bridge = self.create_bridge()
    
        ends = union() (
            translate([-self.length,0,0]) (
                mirror([-1,0,0]) (self.e1.put())
            ),
            self.e2.put(),            
        )
        
        return union() (
            ends, 
            bridge
        )
    

    
class Grill(Element):
    def create_grill( self ):

        holes = []

        # parameterize
        width = 2
        step = width * 2

        for i in range( -1, self.size.x * 2, step ):
            holes.append(
                translate([i,-2,0]) (
                    rotate( 45 ) (
                        cube( [width, self.size.diagonal() * 2,self.size.z] )
                    )
                )
            )

        holes = union() (
            *holes
        )

        return holes

    def create( self ):
        return difference() (
            cube( self.size() ),
            self.create_grill()
        )


class Mesh( Grill ):
    def create( self ):
        grill_a = Grill( self.size )
        grill_b = Grill( self.size )

        grill_b = mirror([-1,0,0]) (
            grill_b.put([-self.size.x, 0, 0])
        )

        return union() (
            grill_a.put(),
            grill_b
        )
        
    
class HoleGrill(Grill):
    
    def create_hole( self, radius=1 ):
        return cylinder( radius, self.size.z )
    
    def find_holes( self, step=5 ):
        result = []
        odd = False
    
        x = self.size.x
        y = self.size.y
        z = self.size.z
        
        v = {}
    
        v['x'] = [i for i in range( 1, x, step )]
        v['y'] = [i for i in range( 1, y, step )]
        
        for d in range( -x, x+1, 2 ):
            odd = not odd
            for x, y in zip( v['x'], v['y'] ):
                if odd:
                    result.append( [x+d, y+step, 0] )
                else:
                    result.append( [x+d, y, 0] )
        
        return result
                
                
        
        
    def create( self ):
    
        g = cube( self.size() )
    
        holes = []
        
        for h in self.find_holes():
            h = translate(h) (
                self.create_hole()
            )        
            holes.append( h )

        holes = union() ( *holes )
        
        g = difference() (
            g,
            holes
        )   
        
        return g

        
        
class LineGrill( Grill ):
    pass
    
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

    e = PerforatedSection( 100 )

    e = Mesh( Size( 20, 20, 1) )

    scad_render_to_file( e.put(), "project.scad" )
    
        