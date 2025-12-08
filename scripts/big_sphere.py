import py5
from scripts.scene_object import SceneObject

class BigSphere(SceneObject):
    def __init__(self, position):
        super().__init__(position)
        self.rotation = 0
        self.rotation_speed = 0.01
    
    def _draw(self, frame_number):
        sphere_rad = 0
        if frame_number < 1900:
            sphere_rad = py5.remap(frame_number, 0, 1900, 0, 100)
        
        elif frame_number < 2050:
            sphere_rad = 100
        
        elif frame_number < 2100:
            sphere_rad = py5.remap(frame_number, 2050, 2100, 100, 1000)
        
        elif frame_number < 4250:
            sphere_rad = 1000
            
        elif frame_number < 5000:
            sphere_rad = py5.remap(frame_number, 4250, 5000, 1000, 0)
        
        else:
            self.ALIVE = False
            return
        
        py5.push_matrix()
        py5.push_style()
        
        py5.translate(self.x, self.y)
        self.rotation -= self.rotation_speed
        py5.rotate_y(self.rotation)
        py5.no_fill()
        py5.stroke(35)
        py5.sphere(sphere_rad)
        
        py5.pop_style()
        py5.pop_matrix()