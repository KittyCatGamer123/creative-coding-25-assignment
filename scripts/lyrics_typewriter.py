import py5
from scripts.scene_object import SceneObject


class LyricTypewriter(SceneObject):
    def __init__(self, position, lyrics_list: list, line_height: int, char_delay: int):
        super().__init__(position)
        self.frame_counter = 0
        self.line_height = line_height
        self.char_delay = char_delay
        
        self.lyrics_list = lyrics_list
        self.lines_completed = []
        self.visible_char = 0
        self.current_txt = ""
        
        self.waiting_next_line = False
        self.line_wait = char_delay * 10
    
    def _process(self, frame_number):
        if len(self.lines_completed) >= len(self.lyrics_list):
            self.current_txt = ""
            return
        
        if self.waiting_next_line:
            self.frame_counter += 1
            self.current_txt = ""
            if self.frame_counter >= self.line_wait:
                self.waiting_next_line = False
            return
        
        current_ln = self.lyrics_list[len(self.lines_completed)]
        
        if self.frame_counter >= self.char_delay:
            self.visible_char += 1
            self.frame_counter = 0
        
        self.current_txt = current_ln[0:self.visible_char]
        
        if self.visible_char >= len(current_ln):
            self.lines_completed.append(current_ln)
            self.waiting_next_line = True
            self.visible_char = 0
        
        self.frame_counter += 1
    
    def _draw(self, frame_number):
        py5.push_style()
        
        py5.fill(130)
        for i in range(-len(self.lines_completed), 0, 1):
            py5.text(self.lines_completed[i], self.x, self.y + (self.line_height * i))
            
        py5.fill(255)
        py5.text(self.current_txt + "_", self.x, self.y)
        py5.pop_style()