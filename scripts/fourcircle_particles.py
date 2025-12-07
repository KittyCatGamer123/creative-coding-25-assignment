from random import randrange
from scripts.scene_object import SceneObject
import py5

class FourCircleParticles(SceneObject):
    def __init__(self, position, lifetime: int):
        super().__init__(position)
        
        self.x = randrange(0, py5.width)
        self.y = randrange(0, py5.height)
        self.size = randrange(1, 10)
        self.rot = 0
        self.rot_speed = randrange(-7, 7) / 100
        self.dist = randrange(20, 80)
        self.frame_count = 0
        self.frame_kill = 60 * lifetime
        self.hue = randrange(150, 230)
    
    def _process(self, frame_number):
        self.frame_count += 1
        
        if self.frame_count >= self.frame_kill:
            self.ALIVE = False
    
    def _draw(self, frame_number):
        py5.push_matrix()
        py5.push_style()
        py5.no_stroke()
        
        alph = py5.remap(self.frame_count, 0, self.frame_kill, 100, 0)
        py5.color_mode(py5.HSB)
        py5.fill(self.hue, 100, 255, alph)
        py5.translate(self.x, self.y)
        
        py5.rotate(self.rot)
        self.rot += self.rot_speed
        
        py5.circle(-self.dist, -self.dist, self.size)
        py5.circle(self.dist, -self.dist, self.size)
        py5.circle(-self.dist, self.dist, self.size)
        py5.circle(self.dist, self.dist, self.size)
        
        py5.pop_style()
        py5.pop_matrix()