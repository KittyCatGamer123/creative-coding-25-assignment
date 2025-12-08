from scripts.scene_object import SceneObject
import py5

class MiddleFreqs(SceneObject):
    def __init__(self, position):
        super().__init__(position)
        self.freqs = []
    
    def _draw(self, frame_number):
        py5.push_style()
        py5.no_stroke()
        py5.fill(255, 94, 247, 150)
        py5.rect_mode(py5.CENTER)
        
        for idx, val in enumerate(self.freqs):
            size = py5.remap(val, 0, 0.5, 0, 50)
            py5.rect(self.x, self.y + (idx * 64), size, 55)
        py5.pop_style()