import py5

from scripts.scene_object import SceneObject
from scripts.util import clamp
from scripts.vector2d import Vector2D

class ProgressBar(SceneObject):
    def __init__(self, value: float, min_val: float, max_val: float, position: Vector2D, size: Vector2D):
        super().__init__(position)
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        
        self.w = size.x
        self.h = size.y
    
    def _draw(self, frame_number: int): 
        # Seeker
        seeker_width = 8
        
        seeker_progress = clamp((self.value - self.min_val) / (self.max_val - self.min_val), 0, 1) # Basic percentage calculator
        seeker_base_x = self.x - (seeker_width / 2)
        seeker_x = seeker_base_x + (self.w * seeker_progress)
        
        py5.push_matrix()
        py5.push_style()
        
        py5.color_mode(py5.RGB)
        py5.no_stroke()
        py5.fill(230)
        py5.rect(seeker_x, self.y, (seeker_width / 2), self.h)
        
        # Mid-Line
        line_thickness = 4
        py5.rect(self.x, self.y + (self.h / 2) - (line_thickness / 2), self.w, (line_thickness / 2))
        
        py5.pop_style()
        py5.pop_matrix()