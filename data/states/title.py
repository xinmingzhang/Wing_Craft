import sys
import json
import pygame as pg
from .. import tools
from ..prepare import GFX,FONT1,CTRL,MUSIC,SFX
from ..components.labels import Label,Blinker
from ..components import transition

class Title(tools._State):
    def __init__(self):
        super(Title, self).__init__()
        self.bg = GFX['title_bg']
        self.coins = 0
        self.fade_effect = False
        self.make_labels()
        self.transition = transition.Transition()

    def make_labels(self):
        self.labels = pg.sprite.Group()
        self.text_1 = 'credit {}'.format(self.coins)
        self.text_2 = 'Tab  key  for  control  settings'
        self.text_3 = 'Please     insert     coin'
        self.text_4 = 'Press  1P  or  2P  start  button'

        self.label_1 = Label(self.text_1,
                             {'midbottom': (300, 750)},
                             self.labels,
                             font_path=FONT1,
                             text_color=(255, 255, 255),
                             font_size=25)

        self.label_2 = Label(self.text_2,
                             {'midbottom': (300, 780)},
                             self.labels,
                             font_path=FONT1,
                             text_color=(200, 200, 200),
                             font_size=15)

        self.blinker = Blinker(self.text_3,
                               {'midbottom': (300, 700)},
                               500,
                               self.labels,
                               font_path=FONT1,
                               text_color=(255, 255, 255),
                               font_size=30)

    def get_coin(self):
        SFX['coin'].play()
        self.coins += 1


        
    def startup(self, persist):
        self.done = False
        self.persist = persist
        self.choice = [False, False]
        try:
            self.coins = self.persist['coins']
        except:
            self.coins = 0
        self.frame = 0
        if pg.mixer.music.get_busy():
            pass
        else:
            pg.mixer.music.load(MUSIC['06_-_space_troopers_0'])
            pg.mixer.music.play(-1)
        with open(CTRL, 'r') as f:
            self.controls = json.load(f)
        self.transition = transition.Transition()
        self.fade_effect = False

    def cleanup(self):
        if self.next == 'SELECT':
            pg.mixer.music.fadeout(500)
        persist = {}
        persist['controls'] = self.controls
        persist['choice'] = self.choice
        persist['coins'] = self.coins
        return persist

    def get_event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_TAB:
                    self.fade_effect = True
                    self.next = 'CONTROL'
                if event.key in(self.controls['1p_coin'],self.controls['2p_coin']):
                    self.get_coin()
                if event.key == self.controls['1p_start']:
                    if self.coins >= 1:
                        self.coins -= 1
                        self.choice[0] = True
                        self.fade_effect = True
                        self.next = 'SELECT'

                elif event.key == self.controls['2p_start']:
                    if self.coins >= 1:
                        self.coins -= 1
                        self.choice[1] = True
                        self.fade_effect = True
                        self.next = 'SELECT'

    def update_text(self,dt):
        if self.coins:
            self.blinker.original_text = self.text_4
        else:
            self.blinker.original_text = self.text_3
        self.text_1 = 'credit {}'.format(self.coins)
        self.label_1.set_text(self.text_1)
        self.blinker.update(dt)


    def update(self, dt):
        self.frame += 1
        self.transition.fade_in()
        if self.frame == 300 and self.fade_effect == False and not self.coins:
            self.fade_effect = True
            self.next = 'SCORE'
        if self.fade_effect == True:
            self.done = self.transition.fade_out()
        self.update_text(dt)


    def draw(self, surface):
        surface.blit(self.bg,(0,0))
        self.labels.draw(surface)
        self.transition.draw(surface)



