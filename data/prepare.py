import os
import pygame as pg
from . import tools

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
pg.mixer.pre_init(44100, -16, 1, 512)
pg.display.set_mode((600,800))

ORIGINAL_CAPTION = "xmzhang"
pg.display.set_caption(ORIGINAL_CAPTION)

GFX = tools.load_all_gfx(os.path.join("resources", "graphics"))
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
SFX = tools.load_all_sfx(os.path.join("resources", "sound"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
MAP = tools.load_all_json_maps(os.path.join('resources','maps'))

CTRL = os.path.join('resources','controls.json')
SCORE = os.path.join('resources','scoreboard.json')


MAP1 = MAP['map1']
MAP2 = MAP['map2']
MAP3 = MAP['map3']
MAP4 = MAP['map4']
MAP5 = MAP['map5']


FONT1 = FONTS['ARCADECLASSIC']
FONT2 = FONTS['Ancient Medium']
FONT3 = FONTS['Gamer']


WIDTH = 600
HEIGHT = 800
SCREENRECT = pg.Rect(0,0,WIDTH,HEIGHT)











