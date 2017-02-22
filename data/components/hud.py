import pygame as pg
from ..prepare import FONT1,FONT2, FONT3,GFX
from . import labels


class Hud(object):
    def __init__(self, game):
        self.game = game
        self.layer = pg.Surface((600, 800), pg.SRCALPHA)
        self.labels = pg.sprite.Group()
        self.bomb_img = GFX['bomb1']
        self.set_player_image()
        self.bonus_num = 100000


        self.health_bar = GFX['health_bar']
        self.health_bar_size = self.health_bar.get_size()
        self.health_bar_rect = self.health_bar.get_rect(center = (300,55))
        self.health_bar_h = self.health_bar.get_height()
        self.health_bar_w = self.health_bar.get_width()


        label_texts = ['player 1', 'highscore', 'player 2']
        attributes = ['topleft', 'midtop', 'topright']
        label_pos = [(0, 0), (300, 0), (600, 0)]
        label_colors = [(211, 12, 243), (255, 7, 7), (5, 5, 246)]
        for text, attr, pos, color in zip(label_texts, attributes, label_pos, label_colors):
            labels.Label(text, {attr: pos}, self.labels, font_path=FONT1, text_color=color, font_size=25)

        self.coin_label = labels.Label('credit {}'.format(self.game.coins), {'midbottom': (300, 800)}, self.labels,
                                       font_path=FONT1, text_color=(255, 255, 255), font_size=25)
        self.player_1_label = labels.Label('please wait', {'topleft': (0, 25)}, self.labels, font_path=FONT1,
                                           text_color=(255, 255, 255), font_size=25)

        self.player_2_label = labels.Label('please wait', {'topright': (600, 25)}, self.labels, font_path=FONT1,
                                           text_color=(255, 255, 255), font_size=25)

        self.continue_label_up = labels.Label('',{'midbottom': (300, 300)},self.labels, font_path=FONT1,
                                           text_color=(255, 255, 255), font_size=55)
        self.continue_label_down = labels.Label('',{'midtop': (300, 300)},self.labels, font_path=FONT1,
                                           text_color=(255, 255, 255), font_size=55)
        self.update_player_labels()

    def update_player_labels(self):
        if self.game.player_1.groups():
            player_1_text = '{}'.format(self.game.player_1.score)
        elif not self.game.player_1.groups():
            if self.game.coins >= 1:
                player_1_text = 'push 1p start'
            elif self.game.coins == 0:
                player_1_text = 'insert coin'
        if hasattr(self.game, 'player_1_choose') and self.game.player_1_choose == True:
            if self.game.choice[0] == 1:
                text = 'cricket'
            elif self.game.choice[0] == 3:
                text = 'locust'
            player_1_text = '{}  ??{}??'.format(self.game.choose_player_1_time, text)

        self.player_1_label.set_text(player_1_text)

        if self.game.player_2.groups():
            player_2_text = '{}'.format(self.game.player_2.score)
        elif not self.game.player_2.groups():
            if self.game.coins >= 1:
                player_2_text = 'push 2p start'
            elif self.game.coins == 0:
                player_2_text = 'insert coin'

        if hasattr(self.game, 'player_2_choose') and self.game.player_2_choose == True:
            if self.game.choice[1] == 2:
                text = 'cricket'
            elif self.game.choice[1] == 4:
                text = 'locust'
            player_2_text = '??{}?? {}'.format(text, self.game.choose_player_2_time)
        self.player_2_label.set_text(player_2_text)
        if self.game.show_continue == True:
            self.continue_label_up.set_text('continue')
            self.continue_label_down.set_text('{}'.format(int(self.game.c_time)))

        elif self.game.show_continue == False:
            self.continue_label_up.set_text('')
            self.continue_label_down.set_text('')

    def set_player_image(self):
        if self.game.player_1.groups():
            if self.game.player_1.id == 1:
                self.player_1_image = pg.transform.scale(GFX['player1'],(20,30))

            elif self.game.player_1.id == 3:
                self.player_1_image = pg.transform.scale(GFX['player3'],(20,30))
        if self.game.player_2.groups():
            if self.game.player_2.id == 2:
                self.player_2_image = pg.transform.scale(GFX['player2'],(20,30))

            elif self.game.player_2.id == 4:
                self.player_2_image = pg.transform.scale(GFX['player4'],(20,30))

    def blit_player_num(self):
        if self.game.player_1.groups():
            for i in range(self.game.player_1.lives - 1):
                self.layer.blit(self.player_1_image, (0 + i * 30, 70))
        if self.game.player_2.groups():
            for i in range(self.game.player_2.lives -1 ):
                self.layer.blit(self.player_2_image, (600 - (i + 1) * 30, 70))

    def blit_bomb_num(self):
        if self.game.player_1.groups():
            for i in range(self.game.player_1.bomb_num):
                self.layer.blit(self.bomb_img, (0 + i * 30, 770))
        if self.game.player_2.groups():
            for i in range(self.game.player_2.bomb_num):
                self.layer.blit(self.bomb_img, (600 - (i + 1) * 30, 770))

    def blit_health_bar(self):
        if self.game.boss.groups():
            health_bar_layer = pg.Surface(self.health_bar_size,pg.SRCALPHA)
            ratio = self.game.boss.health/1.0/self.game.boss.o_health
            blood_length =  ratio * self.health_bar_w
            if ratio >=0.2:
                pg.draw.rect(health_bar_layer,(250,211,42),(2,2,blood_length-2,self.health_bar_h-3))
            else:
                pg.draw.rect(health_bar_layer, (255, 0, 0), (2, 2, blood_length - 2, self.health_bar_h - 3))
            health_bar_layer.blit(self.health_bar,(0,0))
            self.layer.blit(health_bar_layer,self.health_bar_rect)


    def blit_bonus(self):
        if self.game.stage_clear:
            self.layer.blit(GFX['stageclear'], (220, 100))


            if self.game.player_1.groups():
                layer = pg.Surface((200,400),pg.SRCALPHA)
                board = GFX['frame1']
                p1_bonus_label = pg.sprite.Group()
                labels.Label('Player 1', {'center': (100, 50)},p1_bonus_label, font_path=FONT1,
                                           text_color=(211, 12, 243), font_size=35)
                labels.Label('x {}'.format(self.game.player_1.lives), {'topright': (160, 100)}, p1_bonus_label, font_path=FONT1,
                             text_color=(211, 12, 243), font_size=35)
                labels.Label('{}'.format(self.bonus_num * self.game.player_1.lives), {'topright': (180, 150)}, p1_bonus_label, font_path=FONT3,
                             text_color=(211, 12, 243), font_size=35)
                labels.Label('x {}'.format(self.game.player_1.bomb_num), {'topright': (160, 200)}, p1_bonus_label, font_path=FONT1,
                             text_color=(211, 12, 243), font_size=35)
                labels.Label('{}'.format(self.bonus_num * self.game.player_1.bomb_num), {'topright': (180, 250)}, p1_bonus_label, font_path=FONT3,
                             text_color=(211, 12, 243), font_size=35)
                labels.Label('BONUS', {'center': (100, 310)}, p1_bonus_label, font_path=FONT1,
                             text_color=(211, 12, 243), font_size=35)
                labels.Label('{}'.format(self.bonus_num * (self.game.player_1.lives + self.game.player_1.bomb_num)), {'center': (100, 350)}, p1_bonus_label, font_path=FONT3,
                             text_color=(211, 12, 243), font_size=40)
                bonus = self.bonus_num * (self.game.player_1.lives + self.game.player_1.bomb_num)
                if self.game.player_1.score < self.game.p1_score + bonus:
                    self.game.player_1.score += int(bonus / self.game.show_label_time)
                layer.blit(board,(0,0))
                p1_bonus_label.draw(layer)
                layer.blit(self.player_1_image,(50,105))
                layer.blit(self.bomb_img,(48,205))
                self.layer.blit(layer,(50,200))

            if self.game.player_2.groups():
                layer = pg.Surface((200,400),pg.SRCALPHA)
                board = GFX['frame2']
                p2_bonus_label = pg.sprite.Group()
                labels.Label('Player 2', {'center': (100, 50)},p2_bonus_label, font_path=FONT1,
                                           text_color=(5, 5, 246), font_size=35)
                labels.Label('x {}'.format(self.game.player_2.lives), {'topright': (160, 100)}, p2_bonus_label, font_path=FONT1,
                             text_color=(5, 5, 246), font_size=35)
                labels.Label('{}'.format(self.bonus_num * self.game.player_2.lives), {'topright': (180, 150)}, p2_bonus_label, font_path=FONT3,
                             text_color=(5, 5, 246), font_size=35)
                labels.Label('x {}'.format(self.game.player_2.bomb_num), {'topright': (160, 200)}, p2_bonus_label, font_path=FONT1,
                             text_color=(5, 5, 246), font_size=35)
                labels.Label('{}'.format(self.bonus_num * self.game.player_2.bomb_num), {'topright': (180, 250)}, p2_bonus_label, font_path=FONT3,
                             text_color=(5, 5, 246), font_size=35)
                labels.Label('BONUS', {'center': (100, 310)}, p2_bonus_label, font_path=FONT1,
                             text_color=(5, 5, 246), font_size=35)
                labels.Label('{}'.format(self.bonus_num * (self.game.player_2.lives + self.game.player_2.bomb_num)), {'center': (100, 350)}, p2_bonus_label, font_path=FONT3,
                             text_color=(5, 5, 246), font_size=40)

                bonus = self.bonus_num * (self.game.player_2.lives + self.game.player_2.bomb_num)
                if self.game.player_2.score < self.game.p2_score + bonus:
                    self.game.player_2.score += int(bonus / self.game.show_label_time)
                layer.blit(board,(0,0))
                p2_bonus_label.draw(layer)
                layer.blit(self.player_2_image,(50,105))
                layer.blit(self.bomb_img,(48,205))
                self.layer.blit(layer,(350,200))


    def update(self):
        self.set_player_image()
        self.update_player_labels()
        self.coin_label.set_text('credit {}'.format(self.game.coins))


    def draw(self, surface):
        self.layer.fill((0, 0, 0, 0))
        self.labels.draw(self.layer)
        self.blit_bomb_num()
        self.blit_health_bar()
        self.blit_player_num()
        self.blit_bonus()
        surface.blit(self.layer, (0, 0))
