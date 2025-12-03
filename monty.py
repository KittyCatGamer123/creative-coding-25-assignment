from random import randrange
import py5
import py5_tools
import time 

from scripts.scene_object import SceneObject
from scripts.scrolling_particle import ScrollingParticle
from scripts.util import time_format
from scripts.vector2d import Vector2D
from scripts.progress_bar import ProgressBar

py5_tools.processing.download_library("Sound")
from processing.sound import SoundFile, Amplitude, FFT

####

ACTIVE_NODES: list[SceneObject] = [] # Keep track of all the existing objects in the program.
FRAME: int = 0                       # Frame step counter allowing for each animation to trigger on-time.
FONT = None

intro_particles: list[ScrollingParticle] = []

audio_player: SoundFile = None       # The audio player for playing the song.
amplutude_entity: Amplitude = None
fft_entity: FFT = None

song_progress_bar: ProgressBar = None

start_time: int = 0                 # Unix timestamp for when the program starts.
end_time: int = 0                   # Estimated time when the song ends.

####

def settings():
    py5.size(1000, 800, py5.P3D)

def setup():
    py5.window_title("CC25 Assignment")
    py5.window_resizable(False)
    
    global audio_player, amplutude_entity, fft_entity
    audio_player = SoundFile(py5.get_current_sketch(), "When You Find Me.mp3")
    audio_player.play()
    
    amplutude_entity = Amplitude(py5.get_current_sketch())
    amplutude_entity.input(audio_player)
    
    fft_entity = FFT(py5.get_current_sketch(), 64)
    fft_entity.input(audio_player)
    
    global FONT
    FONT = py5.create_font("Terminus.ttf", 20)
    py5.text_font(FONT)
    
    global start_time, end_time
    start_time = int(time.time())
    end_time = start_time + 225 # 225 => 3:45 Song Length
    
    # Used to check that start and end time are correct
    # print(time.strftime("%d %H:%M:%S", time.localtime(start_time)))
    # print(time.strftime("%d %H:%M:%S", time.localtime(end_time)))
    
    global song_progress_bar
    song_progress_bar = ProgressBar(start_time, start_time, end_time, Vector2D(30, 760), Vector2D(850, 20))
    
    global ACTIVE_NODES
    ACTIVE_NODES.append(song_progress_bar)
    
def draw():
    global amplutude_entity, fft_entity
    AMP_VAL = amplutude_entity.analyze()
    FFT_VAL = fft_entity.analyze()
    
    py5.background(15)
    
    global FRAME
    global ACTIVE_NODES, intro_particles
    
    if FRAME in range(0, 1200, 110):
        for n in range(0, 5):
            new_particle = ScrollingParticle(Vector2D(randrange(-5, -500, -1), randrange(0, py5.height)), 1, randrange(0, 1))
            intro_particles.append(new_particle)
            ACTIVE_NODES.append(new_particle)
    
    ACTIVE_NODES = [n for n in ACTIVE_NODES if n.ALIVE]
    for n in ACTIVE_NODES:
        n.step(FRAME)
    
    intro_particles = [n for n in intro_particles if n.ALIVE]
    for n in intro_particles:
        n.scale = AMP_VAL * 10
    
    global start_time, song_progress_bar
    current_time = time.time()
    song_progress_bar.value = current_time
    py5.push_style()
    py5.fill(230)
    py5.text(time_format(current_time - start_time), 900, 775)
    py5.pop_style()
    
    FRAME += 1
    
py5.run_sketch()