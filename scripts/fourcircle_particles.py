from random import randrange
from scripts.scene_object import SceneObject
import py5

class FourCircleParticles(SceneObject):
    def __init__(self, position):
        super().__init__(position)
        
        self.x = randrange(0, py5.width)
        self.y = randrange(0, py5.height)
        self.size = randrange(1, 10)
        self.rot = 0
        self.rot_speed = randrange(-7, 7) / 100
        self.dist = randrange(20, 80)
    
    def _draw(self, frame_number):
        py5.push_matrix()
        py5.push_style()
        py5.no_stroke()
        py5.fill(190, 189, 255, 100)
        py5.translate(self.x, self.y)
        
        py5.rotate(self.rot)
        self.rot += self.rot_speed
        
        py5.circle(-self.dist, -self.dist, self.size)
        py5.circle(self.dist, -self.dist, self.size)
        py5.circle(-self.dist, self.dist, self.size)
        py5.circle(self.dist, self.dist, self.size)
        
        py5.pop_style()
        py5.pop_matrix()