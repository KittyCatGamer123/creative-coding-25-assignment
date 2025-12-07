import py5
from scripts.scene_object import SceneObject


class GeometricSquare(SceneObject):
    def __init__(self, position, bpm: int = 110):
        super().__init__(position)
        self.frames_per_beat = int(60 * 60 / bpm)
        self.base_y = self.y
        
        self.jump_start_frame = None
        self.jump_duration = 40     # frames to complete jump arc        
        self.jump_height = 120      # peak height
        
        self.rotation = 0
        self.rot_speed = py5.PI
    
    def _process(self, frame_number):
        if frame_number % self.frames_per_beat == 0:
            self.jump_start_frame = frame_number
    
    def get_jump_motion(self, frame_number):
        if self.jump_start_frame is None:
            return 0, 0

        t = frame_number - self.jump_start_frame
        n = min(t / self.jump_duration, 1)  # clamp to 1 instead of aborting

        # Parabolic jump (smooth up AND smooth down)
        y_offset = -4 * self.jump_height * n * (1 - n)

        # Rotation synced across full arc
        rotation = n * self.rot_speed

        return y_offset, rotation
    
    def _draw(self, frame_number):
        y_offset, rot = self.get_jump_motion(frame_number)
        y = self.base_y + y_offset
    
        py5.push_matrix()
        py5.push_style()
        
        py5.translate(self.x, y)
        py5.rotate(rot)
        
        py5.rect_mode(py5.CENTER)
        py5.stroke(255)
        py5.fill(0)
        py5.rect(0, 0, 40, 40)
        
        py5.pop_style()
        py5.pop_matrix()