from random import randrange
import py5

from scripts.scene_object import SceneObject
from scripts.vector2d import Vector2D

class ScrollingParticle(SceneObject):
    def __init__(self, position: Vector2D, scale: float, rotation: float):
        super().__init__(position)
        self.size = 10
        self.scale = scale
        self.rotation = rotation
        self.colour = randrange(0, 255)
        
        self.wave_phase = randrange(0, 1000)
        self.wave_amp = py5.remap(self.size, 10, 20, 40, 10)
        self.wave_speed = 0.08
        
        self.trail_history = []
        self.trail_history_limit = 10
    
    def _process(self, frame_number):
        self.x += py5.remap(self.size, 10, 20, 5, 2)
        
        self.wave_phase += self.wave_speed
        self.y_offset = py5.sin(self.wave_phase) * self.wave_amp
        
        self.rotation += 0.05
        
        self.trail_history.append((self.x, self.y + self.y_offset))
        if len(self.trail_history) > self.trail_history_limit:
            self.trail_history.pop(0)
        
        if self.x > (py5.width + (self.size * self.trail_history_limit)):
            self.ALIVE = False
    
    def _draw(self, frame_count: int):
        py5.push_style()
        
        py5.color_mode(py5.HSB)
        py5.no_stroke()
        
        # Draw Trail
        for i, (tx, ty) in enumerate(self.trail_history):
            fade = py5.remap(i, 0, len(self.trail_history) - 1, 0, 80) # 0-10 => 0-80 alpha
            scal = self.scale - py5.remap(i, 0, len(self.trail_history) - 1, 1, 0)
            py5.fill(self.colour, 255, 50, fade)
            self.draw_particle(tx - 5, ty, scal)
        
        py5.fill(self.colour, 50, 255)
        self.draw_particle(self.x, self.y + self.y_offset, self.scale)
    
        py5.pop_style()
    
    def draw_particle(self, px: float, py: float, pscal: float):
        py5.push_matrix()
        py5.translate(px, py)
        
        half_size = (self.size * pscal) / 2
        py5.rotate(self.rotation)
        py5.rect(-half_size, -half_size, half_size * 2, half_size * 2)
        
        py5.pop_matrix()