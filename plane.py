from solid import *
from solid.utils import *

def perforation( radius, height=1 ):
	inner = cylinder( radius, height, center=True )
	outer = cylinder( radius+2, height, center=True )
	return outer - inner


def sausage( inner_length, width=5 ):
	start = cylinder( width )
	end = cylinder( width )
	end = forward( inner_length )( end )
	
	bridge = left(width) ( 
		linear_extrude(1)( square([2*width, inner_length]) )
	)
	
	return union() ( start, bridge, end )
	

def plane( x, y, z ):
	return linear_extrude(z) ( square([x, y]) )



def rounded_plane( width, length, offset):
	total_length = length + (2 * offset)
	bridge = plane( width, total_length, 1 )
	bridge = left( width ) ( bridge )
	bridge = back( offset ) ( bridge )
	
	b = sausage(length, offset) + left(width) ( sausage(length, offset) ) + bridge
	return b


def rounded_perforated_plane( width, length, offset, radius=3, outer_radius=4, height=5 ):

	length = length + outer_radius + offset
	width = width + outer_radius + offset

	total_length = length + (2 * offset)
	bridge = plane( width, total_length, 1 )
	bridge = left( width ) ( bridge )
	bridge = back( offset ) ( bridge )
	
	elements = union() (
		sausage(length, offset),
		left(width) ( sausage(length, offset) ),
		bridge
	)
	
	hole_coordinates = (
		( 0, 0 ),
		( length, 0 ),
		( 0, -width ),
		( length, -width )
	)
	
	holes = []
	walls = []
	
	for c in hole_coordinates:
		walls.append(
			translate([c[1],c[0],0]) (
				cylinder( outer_radius, height ),
			)
		)	
	
	for c in hole_coordinates:
		holes.append(
			translate([c[1],c[0],0]) (
				cylinder( radius, height ),
			)
		)
	
	
	
	return elements + walls - holes

    


        
   
if __name__ == "__main__":
	
	b = rounded_perforated_plane( 50, 50, 5 )
	
	scad_render_to_file(b, "project.scad")