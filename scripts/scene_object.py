from scripts.vector2d import Vector2D

class SceneObject:
    def __init__(self, position: Vector2D):
        self.ALIVE = True
        self.x = position.x
        self.y = position.y
    
    def step(self, frame_number: int):
        if self.ALIVE:
            self._process(frame_number)
            self._draw(frame_number)
    
    def _process(self, frame_number: int):
        pass
    
    def _draw(self, frame_number: int):
        pass