import sys
import json
import pygame as pg
from .. import tools
from ..prepare import GFX,FONT1,FONT2,SFX,SCORE
from ..components.labels import Label
from ..components import background,transition

class EnterName(tools._State):
    def __init__(self):
        super(EnterName, self).__init__()
        self.background = background.Background(1)
        self.string = 'abcdefghijklmnopqrstuvwxyz  '
        self.pos = [(90 + x * 70, 350 + y * 100) for y in range(4) for x in range(7)]
        self.title = GFX['entername']
        self.title_rect = self.title.get_rect(center = (300,100))
        self.end = GFX['end']
        self.end_rect = self.end.get_rect(center = self.pos[27])

        self.next = 'TITLE'

        self.ranks = ['1st','2nd','3rd','4th','5th']
        self.rank_color = [(234, 199, 135), (233, 233, 216), (186, 110, 64), (118, 119, 120), (118, 119, 120)]


    def startup(self, persist):
        self.frame = 0
        self.done = False
        self.persist = persist
        self.coins = self.persist['coins']
        self.scoreboard = self.persist['scoreboard']
        self.controls = self.persist['controls']
        self.transition = transition.Transition()
        self.p1_rank = 6
        self.p1_name = ''
        self.p2_rank = 6
        self.p2_name = ''
        self.get_player_rank()
        self.p1_letter_num = 0
        self.p2_letter_num = 1
        self.make_labels()

    def cleanup(self):
        persist = {}
        persist['coins'] = self.persist['coins']
        return persist

    def get_player_rank(self):
        for i in range(5):
            if self.scoreboard[i][0] == 'player_1':
                self.p1_rank = i
            elif self.scoreboard[i][0] == 'player_2':
                self.p2_rank = i

    def make_labels(self):
        self.labels = pg.sprite.Group()

        for letter, center in zip(self.string, self.pos):
            Label(letter, {'center': center}, self.labels, font_path=FONT1, font_size = 40, text_color=(255,255,255))
        if self.p1_rank != 6:
            Label(self.ranks[self.p1_rank],{'center':(150,180)},self.labels,font_path = FONT2,font_size = 40,text_color = self.rank_color[self.p1_rank])
        if self.p2_rank != 6:
            Label(self.ranks[self.p2_rank], {'center': (450, 180)}, self.labels, font_path=FONT2, font_size=40,
              text_color=self.rank_color[self.p2_rank])

        self.p1_name_label = Label(self.p1_name,{'center':(150,260)},self.labels,font_path = FONT1,font_size = 40,text_color = (255,255,255))
        self.p2_name_label = Label(self.p2_name, {'center': (450, 260)}, self.labels, font_path=FONT1, font_size=40,
                                   text_color=(255, 255, 255))

        self.p1_letter = pg.sprite.Sprite()
        self.p1_letter.image = GFX['1p_letter']
        self.p1_letter.rect = self.p1_letter.image.get_rect(center = self.pos[self.p1_letter_num])
        if self.p1_rank !=6:
            self.labels.add(self.p1_letter)

        self.p2_letter = pg.sprite.Sprite()
        self.p2_letter.image = GFX['2p_letter']
        self.p2_letter.rect = self.p2_letter.image.get_rect(center = self.pos[self.p2_letter_num])
        if self.p2_rank != 6:
            self.labels.add(self.p2_letter)

    def get_event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key in (self.controls['1p_coin'], self.controls['2p_coin']):
                    SFX['coin'].play()
                    self.coins += 1
                if event.key == self.controls['1p_up']:
                    self.p1_letter_num -= 7
                    if self.p1_letter_num < 0:
                        self.p1_letter_num += 28
                    if self.p1_letter_num == 26:
                        self.p1_letter_num = 19
                if event.key == self.controls['1p_down']:
                    self.p1_letter_num += 7
                    if self.p1_letter_num > 27:
                        self.p1_letter_num -= 28
                    if self.p1_letter_num == 26:
                        self.p1_letter_num = 5
                if event.key == self.controls['1p_left']:
                    self.p1_letter_num -= 1
                    if self.p1_letter_num < 0:
                        self.p1_letter_num = 27
                    if self.p1_letter_num == 26:
                        self.p1_letter_num = 25
                if event.key == self.controls['1p_right']:
                    self.p1_letter_num += 1
                    if self.p1_letter_num > 27:
                        self.p1_letter_num = 0
                    if self.p1_letter_num == 26:
                        self.p1_letter_num = 27
                if event.key in (self.controls['1p_button_a'],self.controls['1p_button_b']):
                    self.p1_name = self.add_letter(1)
                if event.key == self.controls['2p_up']:
                    self.p2_letter_num -= 7
                    if self.p2_letter_num < 0:
                        self.p2_letter_num += 28
                    if self.p2_letter_num == 26:
                        self.p2_letter_num = 19
                if event.key == self.controls['2p_down']:
                    self.p2_letter_num += 7
                    if self.p2_letter_num > 27:
                        self.p2_letter_num -= 28
                    if self.p2_letter_num == 26:
                        self.p2_letter_num = 5
                if event.key == self.controls['2p_left']:
                    self.p2_letter_num -= 1
                    if self.p2_letter_num < 0:
                        self.p2_letter_num = 27
                    if self.p2_letter_num == 26:
                        self.p2_letter_num = 25
                if event.key == self.controls['2p_right']:
                    self.p2_letter_num += 1
                    if self.p2_letter_num > 27:
                        self.p2_letter_num = 0
                    if self.p2_letter_num == 26:
                        self.p2_letter_num = 27
                if event.key in (self.controls['2p_button_a'],self.controls['2p_button_b']):
                    self.p2_name = self.add_letter(2)

    def add_letter(self,id):
        if id == 1:
            if len(self.p1_name) == 3:
                return self.p1_name
            elif len(self.p1_name) < 3:
                if self.p1_name.endswith('_'):
                    return self.p1_name
                else:
                    self.p1_name += self.string[self.p1_letter_num]
                    return self.p1_name
        if id == 2:
            if len(self.p2_name) == 3:
                return self.p2_name
            elif len(self.p2_name) < 3:
                if self.p2_name.endswith('_'):
                    return self.p2_name
                else:
                    self.p2_name += self.string[self.p2_letter_num]
                    return self.p2_name

    def save_name(self):
        for i in range(5):
            if self.scoreboard[i][0] == 'player_1':
                self.scoreboard[i][0] = ''
            elif self.scoreboard[i][0] == 'player_2':
                self.scoreboard[i][0]=''
        if self.p1_rank != 6:
            self.p1_name.rstrip('_')
            if self.p1_name != '':
                self.scoreboard[self.p1_rank][0] = self.p1_name
        if self.p2_rank != 6:
            self.p2_name.rstrip('_')
            if self.p2_name != '':
                self.scoreboard[self.p2_rank][0] = self.p2_name
        with open(SCORE, 'w') as f:
            json.dump(self.scoreboard,f)


    def update_letters(self):
        self.p1_letter.rect = self.p1_letter.image.get_rect(center=self.pos[self.p1_letter_num])
        self.p2_letter.rect = self.p2_letter.image.get_rect(center=self.pos[self.p2_letter_num])
        self.p1_name_label.set_text(self.p1_name)
        self.p2_name_label.set_text(self.p2_name)



    def update(self, dt):
        self.transition.fade_in()
        self.frame += 1
        if self.frame >= 600:
            self.save_name()
            self.done = self.transition.fade_out()
        self.transition.fade_in()
        self.background.update()
        self.update_letters()
        self.labels.update()

    def draw(self, surface):
        self.background.draw(surface)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.end,self.end_rect)
        self.labels.draw(surface)