import py5
from sympy import ring
from scripts.scene_object import SceneObject

class Planets(SceneObject):
    def __init__(self, position):
        super().__init__(position)
        self.col = 0
        
        # radius, angular speed
        self.rings = [
            (550,  0.01),
            (490, -0.02),
            (380, 0.03),
        ]
    
    def _process(self, frame_number):
        self.col += 1
        if self.col > 255:
            self.col = 0
    
    def _draw(self, frame_number):
        py5.push_matrix()
        py5.push_style()

        cx = py5.width / 2
        cy = py5.height / 2
        py5.translate(cx, cy)

        py5.rect_mode(py5.CENTER)
        py5.fill(0)
        py5.color_mode(py5.HSB)
        py5.stroke_weight(4)

        count = 36
        step = py5.TWO_PI / count

        offset_pattern = [0, 12, -8]

        size = 80

        for ring_index, (radius, speed) in enumerate(self.rings):
            hue = self.col + (50 * ring_index)
            if hue > 255: hue -= 255
            ring_rotation = frame_number * speed

            for i in range(count):
                angle = i * step + ring_rotation
                radial_offset = offset_pattern[i % len(offset_pattern)]
                
                if frame_number > 4100:
                    bonus_offset = py5.remap(frame_number, 4100, 5000, 0, 400)
                    radial_offset += bonus_offset
                    if bonus_offset > 390:
                        self.ALIVE = False
                        py5.pop_style()
                        return
                

                r = radius + radial_offset

                px = py5.cos(angle) * r
                py = py5.sin(angle) * r
                
                py5.push_matrix()
                py5.translate(px, py)
                py5.stroke(hue, 125, 255)
                py5.rotate(angle + py5.PI / 4)
                py5.rect(0, 0, size, size)
                py5.pop_matrix()

        py5.pop_style()
        py5.pop_matrix()
