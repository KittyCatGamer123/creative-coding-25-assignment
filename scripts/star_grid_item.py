import random
import py5
from scripts.scene_object import SceneObject
from scripts.util import star

class StarGridItem(SceneObject):
    def __init__(self, position, lifetime: int, points = 3):
        super().__init__(position)
        self.rot = 0
        self.rot_spd = random.randrange(-10, 10) / 100
        self.frame_counter = 0
        self.lifetime = (lifetime * 60)
    
    def _process(self, frame_number):
        self.rot += self.rot_spd
        self.frame_counter += 1
        
        if self.frame_counter >= self.lifetime:
            self.ALIVE = False
        
    def _draw(self, frame_number):
        py5.push_style()
        
        alph = py5.remap(self.frame_counter, 0, self.lifetime, 190, 0)
        py5.no_stroke()
        py5.fill(35, alph)
        
        py5.push_matrix()
        py5.translate(self.x, self.y)
        py5.rotate(self.rot)
        star(3, 10, 50)
        
        py5.pop_matrix()
        py5.pop_style()