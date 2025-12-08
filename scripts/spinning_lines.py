from scripts.scene_object import SceneObject
import py5

class SpinningLines(SceneObject):
    def __init__(self, position):
        super().__init__(position)
        self.rotation = 0
        self.width = 10
        self.height = 150
    
    def _process(self, frame_number):
        self.rotation += 0.05
        
    def _draw(self, frame_number):
        py5.push_style()
        py5.color_mode(py5.HSB)
        py5.no_stroke()
        py5.fill(160, 102, 255, 90)
        for n in range(0, 20):
            py5.push_matrix()
            py5.translate(self.x + (n * self.width * 2), self.y)
            py5.rotate(-self.rotation)
            py5.rect(-(self.width / 2), 0, self.width, self.height)
            py5.pop_matrix()
        py5.pop_style()
        