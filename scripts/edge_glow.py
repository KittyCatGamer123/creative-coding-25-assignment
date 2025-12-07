import py5
from enum import Enum
from scripts.scene_object import SceneObject
from scripts.vector2d import Vector2D

class GlowPosition(Enum):
    LEFT = 0,
    RIGHT = 1,
    UP = 2,
    DOWN = 3

class EdgeGlow(SceneObject):
    def __init__(self, position: Vector2D, spawn_frame: int, kill_frame: int, side: GlowPosition):
        self.rotation = 0
        
        match side:
            case GlowPosition.LEFT:
                self.position = Vector2D(95, 0)
                self.rotation = 90 * (py5.PI / 180)
        
        self.img = py5.load_image("img/glow.png")
        self.spawn_frame = spawn_frame
        self.kill_frame = kill_frame
        
        super().__init__(position)
        
    def _draw(self, frame_number):
        if frame_number > self.kill_frame:
            self.ALIVE = False
            return
        
        img_copy = self.img.copy()
        img_copy.resize(800, 100, py5.NEAREST_NEIGHBOR)
        alph = py5.remap(frame_number, self.spawn_frame, self.kill_frame, 255, 0)
        
        py5.push_matrix()
        py5.tint(100, alph)
        py5.translate(self.position.x, self.position.y)
        py5.rotate(self.rotation)
        py5.image(img_copy, 0, 0)
        py5.tint(255, 255)
        py5.pop_matrix()