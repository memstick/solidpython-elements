from solid import *
from solid.utils import *
import doctest

class Metric:
    def half( self, axis=None ):
        return self.center( axis )

    def center( self, axis=None ):
        """
        >>> e = Size( 10, 5, 1 )
        >>> e.center()
        [5.0, 2.5, 0.5]
        
        >>> e.center('x')
        5.0
        >>> e.center('y')
        2.5
        >>> e.center('z')
        0.5
        """
    
        x, y, z = 'x', 'y', 'z'
        if axis:
            if axis.lower() == x:
                return self.x / 2.0
            elif axis.lower() == y:
                return self.y / 2.0
            elif axis.lower() == z:
                return self.z / 2.0
            else:
                raise Error( 'The requested axis >>> {axis} <<< was not found'.format( axis=axis ) )
        else:
            return Position( self.x / 2.0, self.y / 2.0, self.z / 2.0 )
            

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
    
    def stretch( self, x=None, y=None, z=None ):
        self.x = self.x * x if x else self.x
        self.y = self.y * y if y else self.y
        self.z = self.z * z if z else self.z
        

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
    def __init__( self ):
        
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

    
    e1 = PerforatedRoundedPlate( Size( 20, 20, 0 ), 5 )
    
    e2 = PerforatedRoundedPlate( Size( 20, 20, 0 ), 3 )
    
    
    e = union() (
        translate([0,0,0]) (
            mirror([-1,0,0]) (e1.put())
        ),
        e2.put()
    )
    
    scad_render_to_file( e, "project.scad" )
    
        