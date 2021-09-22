'''
________________________________________
    Requirements:
pygame:
https://www.pygame.org/news
pip install pygame
________________________________________
    Description:
"pygame" was used so I wouldn't have to reinvent the wheel, plus it gave me a visual representation of what I was doing, which helped me test and understand if it was working.
If you don't want to see a GUI, simply change the variable "render_gui" to False. It can be found in the first lines of this file under "Basic Variables"
To print out the statistics for the random sample points, press SPACE BAR when using the pygame window. 
Statistics will be automatically printed when not using the GUI. ("render_gui" set to False)

This is certainly not the best implementation as the time complexity is not friendly to large inputs. 
I've optimized it a little by distributing the shapes into cells (render buckets), but due to time constraints I won't attempt to implement a different approach.
Probably a ray marching solution would have reduced the collision check times quite significantly.

________________________________________
    Requirements:
You have a rectangular 2d area, 1000.0 x 1000.0 float units. 
You need to populate it with 1000 shapes, randomly selected from 3 types rectangle, circle, diamond (diamond is symmetrical around the X and Y axis). 
Each shape is assigned an integer ID upon creation. 
Their sizes and positions are also selected randomly, with the following restrictions their maximum dimension should not be smaller than 10x10 units or larger than 100x100 units. 
They should be randomly but uniformly distributed inside our 1000x1000 area and not touch or cross its boundaries. 

Once it’s done, we need to generate 1000 random point samples within the area and test which shape(s) each of them hits. 
A point can hit more than one shape. 
Print out the statistics how many of the 1000 shapes have been hit in total, and the median hit rate (shape hits per point sample).
'''
from pygame.constants import KEYDOWN, QUIT
from math import sqrt
import statistics
import pygame
import random
import sys

# Basic Variables
render_gui = True
WINDOW_SIZE = (1000, 1000) # 1000x1000 requirement
pygame.display.set_caption("Python Assignment")
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE) if render_gui else None
display = pygame.Surface(WINDOW_SIZE)
drawn_shapes = []
running = True

### Classes ###

class Point:
    ''' 
    A class used to represent a Point. It also carries a few extra attributes so it can behave like a particles.
    
            Attributes:
                x (int) : X position
                y (int) : Y position
                pscale (int) : particle/point scale. Value that can be inherited by instancers or used to calculate bbox before replacing it.
                bbox (tuple or None) : A tuple composed of (upper_left_corner, upper_right_corner, lower_left_corner, lower_right_corner) describing the bounding box of the point.
                                       This becomes available once the function "calculate_bbox" is called.
                shape_type : (int) : Essentially an object index for the instancer. It stores a values (usually random) used to determine if the shape will be a rectangle, circle of diamond.
    '''
    def __init__(self, xy_pos, pscale, shape_type=None):
        ''' 
                Parameters:
                    xy_pos (tuple, list) : X and Y positions. [x, y]
                    pscale (int) : particle/point scale. Value that can be inherited by instancers or used to calculate bbox before replacing it.
                    shape_type : (int, optional) : Essentially an object index for the instancer. It stores a values (usually random) used to determine if the shape will be a rectangle, circle of diamond.
        '''
        self.x = xy_pos[0]
        self.y = xy_pos[1]
        self.pscale = pscale
        self.bbox = None
        self.shape_type = shape_type

    def calculate_bbox(self, object=None, overwrite_type=None, draw_bbox_points=False):
        ''' 
        Calculates the bounding box of a point or the current point.
        If no point is provided, it calculates and stores the bbox of the current shape.
        If a point is provided, it uses its data to determine the bbox.

                Parameters:
                    object (Shape, Point or None) : Object used to calculate bbox. If an object is provided it means that an alternative method will be called. (to determine if a box or a circle)
                    overwrite_type (int, optional) : Overwrites the stored type. Either 0 = Rectangle, 1 = Circle or 2 = Diamond.
                    draw_bbox_points : (bool, optional) : Whether or not to draw the points of the bbox (usually used to debug)

                Returns:
                    bbox (tuple) : A tuple composed of (X,Y) coordinate tuples: (upper_left_corner, upper_right_corner, lower_left_corner, lower_right_corner) describing the bounding box of the point.
        '''
        if isinstance(object, Shape):
            radius = object.scale
            shape_type = object.shape_type
        elif isinstance(object, Point):
            radius = object.pscale
            shape_type = overwrite_type if overwrite_type else 1 # Default to circle if no value was provided
        else:
            object = self
            radius = object.pscale
            shape_type = object.shape_type

        if shape_type != 1:
                radius = radius/2

        upper_left_corner = (object.x - radius, object.y - radius)
        upper_right_corner = (object.x + radius, object.y - radius)
        lower_left_corner = (object.x - radius, object.y + radius)
        lower_right_corner = (object.x + radius, object.y + radius)

        if shape_type == 0:
            upper_left_corner = (upper_left_corner[0] + radius, upper_left_corner[1] + radius)
            upper_right_corner = (upper_right_corner[0] + radius, upper_right_corner[1] + radius)
            lower_left_corner = (lower_left_corner[0] + radius, lower_left_corner[1] + radius)
            lower_right_corner = (lower_right_corner[0] + radius, lower_right_corner[1] + radius)

        bbox = (upper_left_corner, upper_right_corner, lower_left_corner, lower_right_corner)

        if draw_bbox_points == True and screen:
            pygame.draw.circle(screen, (255,255,255), bbox[0], 2)
            pygame.draw.circle(screen, (255,255,255), bbox[1], 2)
            pygame.draw.circle(screen, (255,255,255), bbox[2], 2)
            pygame.draw.circle(screen, (255,255,255), bbox[3], 2)

        self.bbox = bbox
        return bbox

class Shape:
    ''' 
    A class used to represent a Shape.
    
            Attributes:
                unique_id (int) = Unique id number used to indentify object. (Key value)
                shape_type (int) : Either 0 = Rectangle, 1 = Circle or 2 = Diamond. (this value is extracted from the provided point)
                x (int) : X position. (this value is extracted from the provided point)
                y (int) : Y position. (this value is extracted from the provided point)
                pscale (int) : Object scale. For example, if 10, then a rectangle will be made of 10px x 10px.
                bbox (tuple or None) : A tuple composed of (upper_left_corner, upper_right_corner, lower_left_corner, lower_right_corner) 
                                       describing the bounding box of the shape. Value inherited from point.
    '''
    def __init__(self, unique_id, point_obj):
        ''' 
                Parameters:
                    unique_id (int) : Unique id number used to indentify object. (Key value)
                    point_obj (Point) : A Point object used to extract position, scale, shape and bbox.
        '''
        self.unique_id = unique_id
        self.shape_type = point_obj.shape_type
        self.x = point_obj.x
        self.y = point_obj.y
        self.scale = point_obj.pscale
        self.bbox = point_obj.bbox


        self.diamond_points = ((self.x+(self.scale/2), self.y),
                               (self.x, self.y+(self.scale/2)),
                               (self.x-(self.scale/2), self.y),
                               (self.x, self.y-(self.scale/2)))


    def is_point_inside_triangle(self, point, triangle):
        """
        Returns True if a point is inside the triangle and returns False if it is outside.

                Parameters:
                point (Point) : Point object used to find X and Y coordinates.
                triangle (tuple) : A tuple with three elements each element consisting of a tuple of X,Y coordinates.

                Returns:
                is_inside (bool) : True if point is inside, False if it's outside.

        How it works:
        Walk clockwise or counterclockwise around the triangle and project the point onto the segment we are crossing by using the dot product.
        Then, check that the vector created is on the same side for each of the triangle's segments.
        """
        # Unpack arguments
        x, y = point.x, point.y
        ax, ay = triangle[0]
        bx, by = triangle[1]
        cx, cy = triangle[2]
        # A to B
        side_1 = (x - bx) * (ay - by) - (ax - bx) * (y - by)
        # B to C
        side_2 = (x - cx) * (by - cy) - (bx - cx) * (y - cy)
        # C to A
        side_3 = (x - ax) * (cy - ay) - (cx - ax) * (y - ay)
        # All the signs must be positive or all negative
        return (side_1 < 0.0) == (side_2 < 0.0) == (side_3 < 0.0)

    def is_point_inside_shape(self, point):
        """
        Returns True if a point is inside the shape and returns False if it is outside.
        This function uses the previous "is_point_inside_triangle" function to determine if point is inside the diamond shape.

                Parameters:
                point (Point) : Point object used to find X and Y coordinates.

                Returns:
                is_inside (bool) : True if point is inside, False if it's outside.
        """
        if isinstance(point, tuple):
            point = type('QuickPoint', (object,), {'x' : point[0], 'y' : point[1] })()
            print(random.randint(0,5))
        if self.shape_type == 0: # Rectangle
            if point.x > self.x-self.scale and point.x < self.x+self.scale:
                if point.y > self.y-self.scale and point.y < self.y+self.scale:
                    return True
            return False
        elif self.shape_type == 1: # Circle
            distance = sqrt( (point.x - self.x) ** 2 + (point.y - self.y) ** 2 )
            if (distance - self.scale) > 0:
                return False
            return True
        else: # Diamond
            triangle_a = (self.diamond_points[0], self.diamond_points[1], self.diamond_points[2])
            triangle_b = (self.diamond_points[0], self.diamond_points[2], self.diamond_points[3])
            if self.is_point_inside_triangle(point, triangle_a) or self.is_point_inside_triangle(point, triangle_b):
                return True
            else:
                return False

    def draw(self):
        """
        Draws shapes to the main window (only if "screen" object is available)
        """      
        COLOR_RED = (255,0,0)
        COLOR_GREEN = (0,255,0)
        COLOR_BLUE = (0,0,255)

        if screen:
            if self.shape_type == 0: # Diamond
                shape = pygame.draw.rect(screen, COLOR_RED, pygame.Rect(self.x, self.y, self.scale, self.scale))
            elif self.shape_type == 1: # Circle
                shape = pygame.draw.circle(screen, COLOR_GREEN, (self.x, self.y), self.scale)
            else: # Must be 2 : Diamond
                shape = pygame.draw.polygon(screen, COLOR_BLUE, self.diamond_points)

### Functions ###

def generate_shapes(total_num_shapes, shape_max_scale, shape_min_scale, print_log=True):
    """
    Populates a display grid with shapes without allowing them to go out of the display boundaries or to intersect with one another.
    This function uses regions (cells or buckets) to reduce the amount of checks it needs to perform.
    Current options set to 64 cells per grid.  

            Parameters:
            total_num_shapes (int) : Number of shapes to create.
            shape_max_scale (int) : Maximum scale allows for shapes.
            shape_max_scale (int) : Minimum scale allows for shapes.
            print_log (bool, optional) : Whether or not to print information regarding the number of shapes that were created.

            Returns:
            drawn_shapes (list) : A list containing all Shape objects that were successfully drawn.
    """
    def is_bbox_intersecting(bbox_one, bbox_two):
        """
        Checks if bounding box one is intersecting with bounding box two

            Parameters:
                bbox_one (tuple) : A tuple composed of (X,Y) coordinate tuples: (upper_left_corner, upper_right_corner, lower_left_corner, lower_right_corner) describing the bounding box of a point.
                bbox_two (tuple) : A tuple composed of (X,Y) coordinate tuples: (upper_left_corner, upper_right_corner, lower_left_corner, lower_right_corner) describing the bounding box of a point.

            Returns:
                is_intersecting (bool) : True if intersecting, False if NOT intersecting.
        
        """
        x_min_boundary_b = bbox_two[0][0]
        x_max_boundary_b = bbox_two[1][0]
        y_min_boundary_b = bbox_two[3][1]
        y_max_boundary_b = bbox_two[1][1]

        x_min_boundary_a = bbox_one[0][0]
        x_max_boundary_a = bbox_one[1][0]
        y_min_boundary_a = bbox_one[3][1]
        y_max_boundary_a = bbox_one[1][1]

        if x_max_boundary_a > x_min_boundary_b and x_min_boundary_a < x_max_boundary_b:
            if y_min_boundary_a > y_max_boundary_b and y_max_boundary_a < y_min_boundary_b:
                return True
        return False

    ### Start Main Function Here ###
    total_num_shapes = total_num_shapes
    drawn_shapes = []
    index = 0
    max_scale = shape_max_scale
    min_scale = shape_min_scale

    # Scales down drawing area by the optimization depth to reduce collision checks
    optimization_depth = 8
    total_bucket_num = optimization_depth*optimization_depth

    # bucket_size = minX minY maxX maxY
    bucket_max_xy = WINDOW_SIZE[0]/optimization_depth
    bucket_size = (0, 0, bucket_max_xy, bucket_max_xy)

    # Find number of objects per bucket (randomly re-add truncated shapes)
    truncated_num_shapes = int(total_num_shapes/total_bucket_num)
    num_bucket_shapes = []
    for i in range(total_bucket_num):
        num_bucket_shapes.append(truncated_num_shapes)
    while sum(num_bucket_shapes) < total_num_shapes:
        num_bucket_shapes[random.randint(0, total_bucket_num-1)] += 1

    # Draw one bucket at a time
    for num_inside_bucket in num_bucket_shapes:
        current_bucket_shapes = []
        current_num_shapes = num_inside_bucket
        
        # Attempts to create shapes till bucket is empty
        while current_num_shapes != 0:
            random_xy_pos = (random.randint(bucket_size[0], bucket_size[2]), random.randint(bucket_size[1], bucket_size[3]))
            random_scale = random.randint(min_scale, max_scale)
            random_type = random.randint(0, 2)

            # Make sure circle respects width and height rules
            if random_type == 1:
                random_scale = random_scale/2

            # Create new point and calculate its bbox
            new_point = Point(random_xy_pos, random_scale, random_type)
            new_point.calculate_bbox()
        
            is_valid = True

            # Unpack Variables
            upper_left_p = new_point.bbox[0]
            upper_right_p = new_point.bbox[1]
            lower_right_p = new_point.bbox[3]
    
            # Make sure it doesn't go out of the current bucket area - Bucket order minX minY maxX maxY
            if upper_left_p[0] < bucket_size[0] or upper_right_p[0] > bucket_size[2]: # X
                is_valid = False
            elif lower_right_p[1] > bucket_size[3] or upper_right_p[1] < bucket_size[1]: # Y
                is_valid = False

            # Only allow creation if not intersecting
            for shape in current_bucket_shapes:
                if is_bbox_intersecting(new_point.bbox, shape.bbox):
                    is_valid = False

            # Created shape, draw and store to bucket list
            if is_valid:
                new_shape = Shape(index, new_point)
                index += 1
                new_shape.draw()
                drawn_shapes.append(new_shape)
                current_bucket_shapes.append(new_shape)
                current_num_shapes -= 1

        # Move Bucket Position
        if bucket_size[3] + 1 < WINDOW_SIZE[0]:
            bucket_size = (bucket_size[0], bucket_size[1]+bucket_max_xy, bucket_size[2], bucket_size[3]+bucket_max_xy)
        else:
            bucket_size = (bucket_size[0]+bucket_max_xy, 0, bucket_size[2]+bucket_max_xy, bucket_max_xy)
    
    # Print how many shapes were generated
    if print_log:
        print("#" * 80)
        print("Total number of shapes generated: " + str(len(drawn_shapes)))
        print("#" * 80)

    return drawn_shapes

def generate_sample_points(num_points, draw_points=True, print_log=True):
    """
    Generates sample points that are then used to calculate number of objects hit, median hit rate and other statistics.
    The result of these checks is then printed to the console.

            Parameters:
            num_points (int) : Number of sample points to create.
            draw_points (int, optional) : Whether or not to draw the point when using it.
            print_log (bool, optional) : Whether or not to print information extracted from current sample. 
    """
    generated_points = []
    point_scale = 2
    hit_shape_dict = {}

    while num_points != 0:
        random_xy_pos = (random.randint(0, WINDOW_SIZE[0]), random.randint(0, WINDOW_SIZE[1]))
        generated_points.append(Point(random_xy_pos, point_scale))
        if draw_points and screen:
            pygame.draw.circle(screen, (255,255,255), random_xy_pos, point_scale)
        num_points -=1
        
    for shape in drawn_shapes:
        for point in generated_points:
            if shape.is_point_inside_shape(point):
                hit_shape_dict[shape.unique_id] = (hit_shape_dict.get(shape.unique_id) or 0) + 1

    if print_log:
        hit_num = 0
        for hit_shape in hit_shape_dict:
            hit_num += hit_shape_dict.get(hit_shape)
        hit_shape_set = set( val for dic in [hit_shape_dict] for val in dic.values())
        print("#" * 80)
        print("Number of shapes: " + str(len(drawn_shapes)))
        print("Number of points sampled: " + str(len(generated_points)))
        print("Number of objects hit at least once: " + str(len(hit_shape_dict)))
        print("Number of hits: " + str(hit_num))
        print("Median hit rate: " + str(statistics.median(hit_shape_set))) # middle score of a distribution
        print("Average number of hits per object: " + str(round(hit_num/len(hit_shape_dict), 1)))
        print("#" * 80)

### Run program if not importing it ###
if __name__ == "__main__":
    if render_gui:
        drawn_shapes = generate_shapes(1000, 100, 10, print_log=False)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # If spacebar is pressed, generate sample points
                if event.type == KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        generate_sample_points(1000)

            pygame.display.update()
    else:
        drawn_shapes = generate_shapes(1000, 100, 10, print_log=False)
        generate_sample_points(1000)
        pygame.quit()
        sys.exit()