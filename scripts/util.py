from scripts.vector2d import Vector2D
import py5

# Clamps a number into a certain range
def clamp(n, min_val, max_val):
    return max(min_val, min(n, max_val))

# Formats the argument into XX:XX style
def time_format(seconds: int):
    m = str(int(seconds / 60)).zfill(2)
    s = str(int(seconds % 60)).zfill(2)
    return f"{m}:{s}"

# Draws a star shape
# Use translate to move the star
def star(npoints: int, inner_rad, outer_rad):
    angle = py5.TWO_PI / npoints
    half_angle = angle / 2
    
    py5.begin_shape()
    a = 0
    while a < py5.TWO_PI:
        sx = py5.cos(a) * inner_rad
        sy = py5.sin(a) * inner_rad
        py5.vertex(sx, sy)
        
        sx = py5.cos(a + half_angle) * outer_rad
        sy = py5.sin(a + half_angle) * outer_rad
        py5.vertex(sx, sy)
        
        a += angle
    py5.end_shape()