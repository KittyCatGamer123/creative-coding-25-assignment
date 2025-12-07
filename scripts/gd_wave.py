from scripts.scene_object import SceneObject
import py5

from scripts.vector2d import Vector2D

class GeometricWave(SceneObject):
    def __init__(self, position):
        super().__init__(position)
        
        self.is_holding = False
        self.wave_speed = 5
        self.amp = 0
        self.rot = 0
        
        self.point_history = []
        self.point_history_max = 40
        
    def _process(self, frame_number):
        self.is_holding = (self.amp >= 0.48)
        
        if self.is_holding:
            self.rot = -45 * (py5.PI / 180)
            self.y -= self.wave_speed
        else:
            self.rot = 45 * (py5.PI / 180)
            self.y += self.wave_speed

        bx_local = -12
        by_local = 0

        bx = bx_local * py5.cos(self.rot) - by_local * py5.sin(self.rot)
        by = bx_local * py5.sin(self.rot) + by_local * py5.cos(self.rot)

        trail_x = self.x + bx
        trail_y = self.y + by

        self.point_history.insert(0, (trail_x, trail_y))
        if len(self.point_history) > self.point_history_max:
            self.point_history.pop()
    
    def _draw(self, frame_number):
        py5.push_matrix()
        py5.push_style()
        
        py5.no_fill()
        py5.stroke(255)
        
        py5.begin_shape()
        py5.stroke_weight(15)
        for idx, (px, py) in enumerate(self.point_history):
            py5.vertex(px - ((idx - 1) * self.wave_speed), py)
        py5.end_shape()

        py5.stroke_weight(1)
        py5.fill(0)
        py5.translate(self.x, self.y)
        py5.rotate(self.rot)

        py5.begin_shape()
        py5.vertex(23, 0)
        py5.vertex(-12, -15)
        py5.vertex(1, 0)
        py5.vertex(-12, 15)
        py5.end_shape(py5.CLOSE)

        py5.pop_style()
        py5.pop_matrix()