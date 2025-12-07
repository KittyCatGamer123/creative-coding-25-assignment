from random import randrange
import py5
import py5_tools
import time 

from lyrics import LYRICS
from scripts.big_sphere import BigSphere
from scripts.util import time_format
from scripts.progress_bar import ProgressBar
from scripts.edge_glow import EdgeGlow, GlowPosition
from scripts.gd_cube import GeometricSquare
from scripts.lyrics_typewriter import LyricTypewriter
from scripts.scene_object import SceneObject
from scripts.scrolling_particle import ScrollingParticle
from scripts.song_title import SongTitle
from scripts.star_grid_item import StarGridItem
from scripts.vector2d import Vector2D

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
song_title_obj: SongTitle = None
song_lyric_objs: list[LyricTypewriter] = []
song_gd_cube: GeometricSquare = None
song_big_sphere: BigSphere = None

start_time: int = 0                 # Unix timestamp for when the program starts.
end_time: int = 0                   # Estimated time when the song ends.

####

def settings():
    py5.size(1000, 800, py5.P3D)

def setup():
    global ACTIVE_NODES
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
    FONT = py5.create_font("Terminus.ttf", 20, False)
    py5.text_font(FONT)
    
    global start_time, end_time
    start_time = int(time.time())
    end_time = start_time + 225 # 225 => 3:45 Song Length
    
    # Used to check that start and end time are correct
    # print(time.strftime("%d %H:%M:%S", time.localtime(start_time)))
    # print(time.strftime("%d %H:%M:%S", time.localtime(end_time)))
    
    global song_progress_bar
    song_progress_bar = ProgressBar(start_time, start_time, end_time, Vector2D(30, 760), Vector2D(850, 20))
    ACTIVE_NODES.append(song_progress_bar)
    
    global song_title_obj
    song_title_obj = SongTitle(Vector2D(920, 670), 0.3)
    ACTIVE_NODES.append(song_title_obj)
    
    global song_big_sphere
    song_big_sphere = BigSphere(Vector2D(py5.width / 2, py5.height / 2))
    ACTIVE_NODES.append(song_big_sphere)
    
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
    
    if FRAME in [50, 570, 1100, 1640]:
        eg = EdgeGlow(Vector2D(0, 0), FRAME, FRAME + (60 * 3), GlowPosition.LEFT)
        ACTIVE_NODES.insert(0, eg)
        
        for row in range(1, 8):
            for column in range(1, 10):
                star = StarGridItem(Vector2D(column * 100, row * 100), 5, 1)
                ACTIVE_NODES.insert(1, star)
                
    if FRAME == 45:
        lyrc = LyricTypewriter(Vector2D(50, 740), LYRICS, 30, 5)
        ACTIVE_NODES.append(lyrc)
    
    if FRAME == 1100:
        global song_gd_cube
        song_gd_cube = GeometricSquare(Vector2D(75, py5.height / 2))
        ACTIVE_NODES.append(song_gd_cube)
    
    ACTIVE_NODES = [n for n in ACTIVE_NODES if n.ALIVE]
    for n in ACTIVE_NODES:
        if type(n) == SongTitle:
            n.scale = AMP_VAL
        n.step(FRAME)
    
    intro_particles = [n for n in intro_particles if n.ALIVE]
    for n in intro_particles:
        n.scale = AMP_VAL * 10
    
    global start_time, song_progress_bar
    current_time = time.time()
    song_progress_bar.value = current_time
    
    # Extra UI that classes are not needed for
    py5.push_style()
    py5.fill(230)
    
    py5.text_align(py5.LEFT)
    py5.text(time_format(current_time - start_time), 900, 775)
    
    py5.text_align(py5.RIGHT)
    py5.text(str(FRAME), 970, 30)
    py5.text(str(current_time - start_time), 970, 50)
    
    py5.pop_style()
    
    FRAME += 1    
    
py5.run_sketch()