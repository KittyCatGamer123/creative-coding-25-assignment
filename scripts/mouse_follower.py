from scripts.scene_object import SceneObject
import py5

class MouseFollower(SceneObject):
    def __init__(self, position):
        super().__init__(position)
        py5.no_cursor()
        self.colour = 0
        self.amp = 1
        
        self.trail_history = []
        self.trail_history_limit = 10
    
    def _process(self, frame_number):
        self.x = py5.mouse_x
        self.y = py5.mouse_y
        self.colour += 1
        if self.colour > 255:
            self.colour = 0
        
        self.trail_history.append((self.x, self.y))
        if len(self.trail_history) > self.trail_history_limit:
            self.trail_history.pop(0)
        
    def _draw(self, frame_number):
        py5.push_matrix()
        py5.push_style()
        
        py5.color_mode(py5.HSB)
        py5.fill(self.colour, 100, 255)
        py5.no_stroke()
        
        size = py5.remap(self.amp, 0, 0.9, 15, 45)
        
        # Draw Trail
        for i, (tx, ty) in enumerate(self.trail_history):
            fade = py5.remap(i, 0, len(self.trail_history) - 1, 0, 80) # 0-10 => 0-80 alpha
            py5.fill(self.colour, 100, 255, fade)
            py5.circle(tx, ty, size)
        
        py5.circle(self.x, self.y, size)
        
        py5.pop_style()
        py5.pop_matrix()