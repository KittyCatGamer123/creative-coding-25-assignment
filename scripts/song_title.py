import py5

from scripts.scene_object import SceneObject
from scripts.util import clamp
from scripts.vector2d import Vector2D

class SongTitle(SceneObject):
    def __init__(self, position: Vector2D, scale: float):
        super().__init__(position)
        self.scale = scale
        self.img = py5.load_image("img/chord.png")
    
    def _draw(self, frame_number: int):
        py5.push_style()
        
        alph = 255
        if frame_number <= 80: # Fade in effect
            alph = py5.remap(frame_number, 0, 80, 0, 255)
        elif frame_number >= 255:
            if frame_number > 335: 
                self.ALIVE = False
                return
            alph = py5.remap(frame_number, 255, 335, 255, 0)
        
        py5.tint(255, alph)
        
        img_copy = self.img.copy()
        img_size = clamp(int(160 * self.scale), 1, 100)
        img_copy.resize(img_size, img_size, py5.NEAREST_NEIGHBOR)
        py5.image_mode(py5.CENTER)
        py5.image(img_copy, self.x, self.y)
        
        py5.color_mode(py5.RGB)
        py5.fill(255, 255, 255, alph)
        
        py5.text_size(40)
        py5.text("When You Find Me", self.x - 365, self.y)
        
        py5.text_size(30)
        py5.fill(196, 235, 255, alph)
        py5.text("by Plenka", self.x - 173, self.y + 30)
        
        py5.tint(255, 255)
        py5.pop_style()