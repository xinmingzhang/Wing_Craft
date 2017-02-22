import sys
import json
import pygame as pg
from .. import tools
from ..prepare import GFX, FONT1, FONT2, SCORE,SFX
from ..components import background
from ..components.labels import Label
from ..components import transition


class Scoreboard(tools._State):
    def __init__(self):
        super(Scoreboard, self).__init__()
        self.background = background.Background(5)
        self.labels = pg.sprite.Group()
        with open(SCORE, 'r') as f:
            self.scoreboard = json.load(f)
        self.images = [GFX['player{}'.format(x + 1)] for x in range(4)]
        self.title = GFX['scoreboard']
        self.title_rect = self.title.get_rect(center = (300,100))
        self.frame = 0
        self.transition = transition.Transition()
        self.next = 'TITLE'
        self.fade_effect = False

        self.make_labels()

    def startup(self, persist):
        self.frame = 0
        self.done = False
        self.transition = transition.Transition()
        self.fade_effect = False
        self.persist = persist
        with open(SCORE, 'r') as f:
            self.scoreboard = json.load(f)
        self.labels = pg.sprite.Group()
        self.make_labels()
        self.controls = self.persist['controls']
        self.coins = self.persist['coins']

    def cleanup(self):
        self.persist['coins'] = self.coins
        return self.persist

    def blit_image(self,surface):
        for i,item in enumerate(self.scoreboard):
            surface.blit(self.images[item[1]-1],(50, 200 + i* 100))


    def make_labels(self):
        rank = ['1st', '2nd', '3rd', '4th', '5th']
        colors = [(234, 199, 135), (233, 233, 216), (186, 110, 64), (118, 119, 120), (118, 119, 120)]
        pos1 = [(150, 250 + x * 100) for x in range(5)]
        pos2 = [(220,250 + x * 100) for x in range(5)]
        pos3 = [(550,250 + x * 100) for x in range(5)]

        for rank, bottomleft, color in zip(rank, pos1, colors):
            Label(rank, {'bottomleft': bottomleft}, self.labels, font_path=FONT2, font_size = 40,text_color = color)

        for item, bottomleft, color in zip(self.scoreboard, pos2, colors):
            Label(item[0], {'bottomleft': bottomleft}, self.labels, font_path=FONT1, font_size = 40, text_color=color)

        for item, bottomright, color in zip(self.scoreboard, pos3, colors):
            Label(str(item[2]), {'bottomright': bottomright}, self.labels, font_path=FONT1, font_size=40, text_color=color)

    def get_coin(self):
        SFX['coin'].play()
        self.coins += 1

    def get_event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key in (self.controls['1p_coin'],self.controls['2p_coin']):
                    self.get_coin()
                    self.fade_effect = True

    def update(self, dt):
        self.frame += 1
        self.transition.fade_in()
        if self.frame >= 120:
            self.fade_effect = True
        if self.fade_effect == True:
            self.done = self.transition.fade_out()
        self.background.update()
        self.labels.update()

    def draw(self, surface):
        self.background.draw(surface)
        self.blit_image(surface)
        surface.blit(self.title,self.title_rect)
        self.labels.draw(surface)
        self.transition.draw(surface)
