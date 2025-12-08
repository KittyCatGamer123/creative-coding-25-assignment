#####################
# Please see assignment attachment for full student name and ID.
#
# Creative Coding Assignment 2025 by Katrinaaster
#   This project is a visualisation on an excerpt from the song "When You Find Me" by Plenka,
#   and also heavily inspired by the Geometry Dash level "Defeated Circles", which uses this song.
#
#   The project uses a wide variety of randonmess alongside pulsating shapes so that the canvas feels "alive" with the song.
#   It uses a basic form of Object-Oriented programming to manage object creation and deletion and utilises the frame number to instruct events to occur.
#
# Interaction Instructions:
#   Move your mouse around to watch a small circle follow it, along with a trail, so you can copy the trailing squares!
#   Use your mouse wheel to increase or decrease the volume.
#
# What I'm most proud of:
#   The wave/triangle that appears during the drop of the song,
#   and the bouncing square at appears at the start and end.
#   as I felt it was a solid reference to the Geometry Dash wave, a game I took heavy inspiration from in visualisng this.
#   Also, the square was very difficult to program, consisting of parabola mathematics, so I'm happy it turned out ok.
#####################

from random import randrange
import py5
import py5_tools
import time 
from enum import IntEnum

from lyrics import LYRICS
from scripts.big_sphere import BigSphere
from scripts.fourcircle_particles import FourCircleParticles
from scripts.gd_wave import GeometricWave
from scripts.middle_freqs import MiddleFreqs
from scripts.mouse_follower import MouseFollower
from scripts.planets import Planets
from scripts.spinning_lines import SpinningLines
from scripts.util import clamp, time_format
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
VOLUME: float = 0.2                  # Volume for the music
FRAME: int = 0                       # Frame step counter allowing for each animation to trigger on-time.
FONT = None

intro_particles: list[ScrollingParticle] = []

audio_player: SoundFile = None       # The audio player for playing the song.
amplutude_entity: Amplitude = None   # Analyser for amplitude
fft_entity: FFT = None               # Analyser for frequency

mouse_effect: MouseFollower = None
song_progress_bar: ProgressBar = None
song_title_obj: SongTitle = None
song_lyric_objs: list[LyricTypewriter] = []
song_gd_cube: GeometricSquare = None
song_big_sphere: BigSphere = None
song_gd_wave: GeometricWave = None
song_middle_freqs: MiddleFreqs = None

start_time: int = 0                 # Unix timestamp for when the program starts.
end_time: int = 0                   # Estimated time when the song ends.

# Determinded and dev-friendly list of frames for what events occur during the draw function.
class EVENTS_HANDLER(IntEnum):
    CREATE_TYPEWRITER = 45
    SPIN_PARTICLES = 1600
    CREATE_CUBE = 1050
    DROP_SETUP = 2130
    DROP_SPIN_PARTICLES = 2650
    SPINNING_SQUARES = 3200
    SPINNING_SQUARES_SINCUBES = 3700
    CREATE_CUBE_ENDING = 4250
    KILL_SPINNING_LINES = 5150
    KILL_TYPEWRITER = 5600

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
    audio_player.amp(VOLUME)
    
    amplutude_entity = Amplitude(py5.get_current_sketch())
    amplutude_entity.input(audio_player)
    
    fft_entity = FFT(py5.get_current_sketch(), 64)
    fft_entity.input(audio_player)
    
    global FONT
    FONT = py5.create_font("Terminus.ttf", 20, False)
    py5.text_font(FONT)
    
    global start_time, end_time
    start_time = int(time.time())
    end_time = start_time + 122 # 122 => 2:02 Song Length
    
    # Used to check that start and end time are correct
    # print(time.strftime("%d %H:%M:%S", time.localtime(start_time)))
    # print(time.strftime("%d %H:%M:%S", time.localtime(end_time)))
    
    # Initialise some classes
    global song_progress_bar
    song_progress_bar = ProgressBar(start_time, start_time, end_time, Vector2D(30, 760), Vector2D(850, 20))
    ACTIVE_NODES.append(song_progress_bar)
    
    global song_title_obj
    song_title_obj = SongTitle(Vector2D(920, 670), 0.3)
    ACTIVE_NODES.append(song_title_obj)
    
    global song_big_sphere
    song_big_sphere = BigSphere(Vector2D(py5.width / 2, py5.height / 2))
    ACTIVE_NODES.append(song_big_sphere)
    
    global mouse_effect
    mouse_effect = MouseFollower(Vector2D(0,0))
   
# Allow the user to adjust the volume of the audio without making all the other objects smaller
def remap_volume(value):
    global VOLUME
    if VOLUME <= 0:
        return value
    return value / VOLUME
 
def draw():
    global amplutude_entity, fft_entity
    AMP_VAL = remap_volume(amplutude_entity.analyze())
    FFT_VAL = map(remap_volume, fft_entity.analyze())
    
    py5.background(15)
    
    global FRAME
    global ACTIVE_NODES, intro_particles
    
    if FRAME in range(0, 1200, 110):
        for n in range(0, 5):
            new_particle = ScrollingParticle(Vector2D(randrange(-5, -500, -1), randrange(0, py5.height)), 1, randrange(0, 1))
            intro_particles.append(new_particle)
            ACTIVE_NODES.append(new_particle)
    
    if FRAME in [50, 570, 1100, 1600]:
        eg = EdgeGlow(Vector2D(0, 0), FRAME, FRAME + (60 * 3), GlowPosition.LEFT)
        ACTIVE_NODES.insert(0, eg)
        
        for row in range(1, 8):
            for column in range(1, 10):
                star = StarGridItem(Vector2D(column * 100, row * 100), 5, 1)
                ACTIVE_NODES.insert(1, star)
        
        if FRAME == int(EVENTS_HANDLER.SPIN_PARTICLES):
            for n in range(200):
                part = FourCircleParticles(Vector2D(0,0), 7)
                ACTIVE_NODES.append(part)
                
    if FRAME == int(EVENTS_HANDLER.CREATE_TYPEWRITER):
        lyrc = LyricTypewriter(Vector2D(50, 740), LYRICS, 30, 5)
        ACTIVE_NODES.append(lyrc)
    
    global song_gd_cube
    global song_gd_wave
    global song_middle_freqs
    
    if FRAME == int(EVENTS_HANDLER.CREATE_CUBE):
        song_gd_cube = GeometricSquare(Vector2D(175, py5.height / 2))
        ACTIVE_NODES.append(song_gd_cube)
        
    elif FRAME == int(EVENTS_HANDLER.DROP_SETUP):
        song_gd_wave = GeometricWave(Vector2D(song_gd_cube.x, song_gd_cube.y))
        ACTIVE_NODES.append(song_gd_wave)
        
        song_middle_freqs = MiddleFreqs(Vector2D(py5.width / 2, 0))
        ACTIVE_NODES.append(song_middle_freqs)
        
        spinny_top = SpinningLines(Vector2D(100, 0))
        spinny_bottom = SpinningLines(Vector2D(600, 800))
        ACTIVE_NODES.append(spinny_top)
        ACTIVE_NODES.append(spinny_bottom)
        
        for n in range(0, 45):
            new_particle = ScrollingParticle(Vector2D(randrange(-5, -1700, -1), randrange(0, py5.height)), 1, randrange(0, 1))
            intro_particles.append(new_particle)
            ACTIVE_NODES.append(new_particle)
        
        song_gd_cube.ALIVE = False
        
    elif FRAME == int(EVENTS_HANDLER.DROP_SPIN_PARTICLES):
        for n in range(200):
            part = FourCircleParticles(Vector2D(0,0), 8)
            ACTIVE_NODES.append(part)
    
    elif FRAME == int(EVENTS_HANDLER.SPINNING_SQUARES):
        planets = Planets(Vector2D(0, 0))
        ACTIVE_NODES.append(planets)
    
    elif FRAME == int(EVENTS_HANDLER.SPINNING_SQUARES_SINCUBES):
        for n in range(0, 45):
            new_particle = ScrollingParticle(Vector2D(randrange(-5, -1700, -1), randrange(0, py5.height)), 1, randrange(0, 1))
            intro_particles.append(new_particle)
            ACTIVE_NODES.append(new_particle)
    
    elif FRAME == int(EVENTS_HANDLER.CREATE_CUBE_ENDING):
        song_gd_cube = GeometricSquare(Vector2D(175, py5.height / 2))
        ACTIVE_NODES.append(song_gd_cube)
        
        song_gd_wave.ALIVE = False
    
    elif FRAME == int(EVENTS_HANDLER.KILL_SPINNING_LINES):
        song_middle_freqs.ALIVE = False
        for n in ACTIVE_NODES:
          if type(n) == SpinningLines:
              n.ALIVE = False  
    
    elif FRAME == int(EVENTS_HANDLER.KILL_TYPEWRITER):
        for n in ACTIVE_NODES:
          if type(n) == LyricTypewriter:
              n.slow_death()
    
    # Call the private "step" function on all the SceneObject classes
    # Filter out all the classes that have "ALIVE" set to false
    # When classes aren't referenced anymore, Python's garbage collector destroys them!    
    ACTIVE_NODES = [n for n in ACTIVE_NODES if n.ALIVE]
    for n in ACTIVE_NODES:
        if type(n) == SongTitle:       n.scale = AMP_VAL
        elif type(n) == GeometricWave: song_gd_wave.amp = AMP_VAL
        elif type(n) == MiddleFreqs:   song_middle_freqs.freqs = FFT_VAL
        
        n.step(FRAME)
    
    # Give all the particles the AMP value to pulse
    intro_particles = [n for n in intro_particles if n.ALIVE]
    for n in intro_particles:
        n.scale = AMP_VAL * 10
        
    # The mouse follower. Seperate from other classes so that it draws on top of everything
    mouse_effect.amp = AMP_VAL
    mouse_effect.step(FRAME)
    
    # Get the current time from when we started
    global start_time, song_progress_bar
    current_time = time.time()
    song_progress_bar.value = current_time
    
    # Extra UI that classes are not needed for
    # XX:XX Timer, Frame counter and framerate
    py5.push_style()
    py5.fill(230)
    
    py5.text_align(py5.LEFT)
    py5.text(time_format(current_time - start_time), 900, 775)
    
    py5.text_align(py5.RIGHT)
    py5.text(f"{int(py5.get_frame_rate())} FPS", 970, 30)
    py5.text(f"VOLUME {int(VOLUME * 100)}%", 970, 50)
    py5.text(f"FRAME {FRAME}", 970, 70)
    
    py5.pop_style()
    
    FRAME += 1    
    
def mouse_wheel(event):
    # event is a mouse event
    # .get_count() gets direction/delta of the scroll
    global VOLUME, audio_player
    print(VOLUME, event.get_count() / 10)
    VOLUME -= (event.get_count() / 10)
    VOLUME = clamp(VOLUME, 0, 1)
    audio_player.amp(VOLUME)
    
py5.run_sketch()