import py5

from scripts.scene_object import SceneObject
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
            alph = py5.remap(frame_number, 255, 335, 255, 0)
        elif frame_number > 335:
            self.ALIVE = False
        
        py5.tint(255, alph)
        self.img.resize(int(160 * self.scale), int(168 * self.scale))
        py5.image(self.img, self.x, self.y)
        
        py5.color_mode(py5.RGB)
        py5.fill(255, 255, 255, alph)
        
        py5.text_size(40)
        py5.text("When You Find Me", self.x - 342, self.y + 25)
        
        py5.text_size(30)
        py5.fill(196, 235, 255, alph)
        py5.text("by Plenka", self.x - 160, self.y + 50)
        
        py5.tint(255, 255)
        py5.pop_style()