import sys
import json
import pygame as pg
from itertools import cycle
from .. import tools
from ..prepare import GFX,FONT1,FONT3,MUSIC,SFX
from ..components import player,background,bullet
from ..components.labels import Label
from ..components import transition

class Select(tools._State):
    def __init__(self):
        super(Select, self).__init__()
        self.background = background.Background(3)
        self.mask = GFX['playerselect']

        self.frame = 0
        self.next = 'LEVEL1'
        self.time = 20
        self.coins = 0

        self.players = pg.sprite.Group()
        self.player_bullets = pg.sprite.Group()
        self.player_1 = pg.sprite.Sprite()
        self.player_2 = pg.sprite.Sprite()
        self.player_1_confirm = False
        self.player_2_confirm = False

        self.transition = transition.Transition()
        self.fade_effect = False

        self.load_images()
        self.make_labels()



    def load_images(self):
        self.player_1_images = cycle([GFX['p1'],GFX['p2']])
        self.player_2_images = cycle([GFX['p3'],GFX['p4']])
        self.player_1_rank_images = cycle([GFX['s4'],GFX['s3']])
        self.player_2_rank_images = cycle([GFX['s2'],GFX['s1']])
        self.player_1_name_images = cycle([GFX['name1'],GFX['name2']])
        self.player_2_name_images = cycle([GFX['name3'],GFX['name4']])
        self.player_1_rects = cycle([pg.Rect(60,460,70,105),pg.Rect(166,460,70,105)])
        self.player_2_rects = cycle([pg.Rect(365,460,70,105),pg.Rect(465,460,70,105)])
        self.player_1_classes = cycle([player.Player(self,(150,400),1),
                                       player.Player(self,(150,400),3)])
        self.player_2_classes = cycle([player.Player(self,(450,400),2),
                                       player.Player(self,(450,400),4)])

        self.player_1_power_image = GFX['s5']
        self.player_1_power_rect = pg.Rect(100,660,97,17)
        self.player_1_speed_image = GFX['s5']
        self.player_1_speed_rect = pg.Rect(100,719,97,17)

        self.player_2_power_image = GFX['s0']
        self.player_2_power_rect = pg.Rect(405,660,97,17)
        self.player_2_speed_image = GFX['s0']
        self.player_2_speed_rect = pg.Rect(405,719,97,17)

        self.player_1_name_image = GFX['name0']
        self.player_1_name_rect = pg.Rect(120,560,70,60)
        self.player_2_name_image = GFX['name0']
        self.player_2_name_rect = pg.Rect(420,560,70,60)

    def make_labels(self):
        self.labels = pg.sprite.Group()
        self.text_1 = 'credit {}'.format(self.coins)

        self.label_0 = Label(str(self.time),
                             {'midbottom': (300, 140)},
                             self.labels,
                             font_path=FONT3,
                             text_color=(255, 255, 255),
                             font_size=50)
        self.label_0.frequency = 490

        self.label_1 = Label(self.text_1,
                             {'midbottom': (300, 780)},
                             self.labels,
                             font_path=FONT1,
                             text_color=(255, 255, 255),
                             font_size=25)

    def get_coin(self):
        SFX['coin'].play()
        self.coins += 1


        
    def startup(self, persist):
        self.persist = persist
        self.choice = self.persist['choice']
        self.players = pg.sprite.Group()
        self.player_1 = pg.sprite.Sprite()
        self.player_2 = pg.sprite.Sprite()
        self.player_1_confirm = False
        self.player_2_confirm = False
        self.player_bullets = pg.sprite.Group()
        if self.choice[0]:
            self.set_player_1()            
        if self.choice[1]:
            self.set_player_2()

        self.coins = self.persist['coins']
        self.controls = self.persist['controls']
        self.transition = transition.Transition()
        self.fade_effect = False
        self.done = False
        self.time = 20

        pg.mixer.music.load(MUSIC['07_-_stars_dont_twinkle_0'])
        pg.mixer.music.play(-1)

        
    def cleanup(self):
        pg.mixer.music.fadeout(500)
        persist = {}
        persist['coins'] = self.coins
        persist['controls'] = self.controls
        persist['choice'] = self.choice
        return persist

    def get_event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key in (self.controls['1p_coin'],self.controls['2p_coin']):
                    self.get_coin()
                if event.key == self.controls['1p_start']:
                    if not self.player_1.groups() and self.coins >= 1:
                        self.coins -= 1
                        self.time = 20
                        self.set_player_1()
                if event.key == self.controls['2p_start']:
                    if not self.player_2.groups() and self.coins >= 1:
                        self.coins -= 1
                        self.time = 20
                        self.set_player_2()                        
                if event.key in (self.controls['1p_up'],self.controls['1p_down'], self.controls['1p_left'], self.controls['1p_right']):
                    if self.player_1.groups() and self.player_1_confirm == False:
                        self.set_player_1()
                        SFX['hint'].play()
                if event.key in (self.controls['2p_up'],self.controls['2p_down'], self.controls['2p_left'], self.controls['2p_right']):
                    if self.player_2.groups() and self.player_2_confirm == False:
                        self.set_player_2()
                        SFX['hint'].play()
                if event.key in (self.controls['1p_button_a'], self.controls['1p_button_b']):
                    if self.player_1.groups() and self.player_1_confirm == False:
                        self.player_1_confirm = True
                        del self.player_1_image
                if event.key in (self.controls['2p_button_a'], self.controls['2p_button_b']):
                    if self.player_2.groups() and self.player_2_confirm == False:
                        self.player_2_confirm = True
                        del self.player_2_image





    def set_player_1(self):
        if self.player_1.groups():
            self.player_1.kill()
        self.player_1 = next(self.player_1_classes)
        self.choice[0] = self.player_1.id
        self.player_1.invincible = False
        self.players.add(self.player_1)
        self.player_1.weapon_level = 5
        self.player_1_image = next(self.player_1_images)
        self.player_1_rect = next(self.player_1_rects)
        self.player_1_power_image = next(self.player_1_rank_images)
        self.player_1_speed_image = next(self.player_1_rank_images)        
        _ = next(self.player_1_rank_images)
        self.player_1_name_image = next(self.player_1_name_images)

    def set_player_2(self):
        if self.player_2.groups():
            self.player_2.kill()
        self.player_2 = next(self.player_2_classes)
        self.choice[1] = self.player_2.id
        self.player_2.invincible = False
        self.players.add(self.player_2)
        self.player_2.weapon_level = 5
        self.player_2_image = next(self.player_2_images)
        self.player_2_rect = next(self.player_2_rects)
        self.player_2_power_image = next(self.player_2_rank_images)
        self.player_2_speed_image = next(self.player_2_rank_images)
        _ = next(self.player_2_rank_images)
        self.player_2_name_image = next(self.player_2_name_images)

    def check_done(self):
        if self.time <= 0:
            return True
        if not self.player_2.groups() and self.player_1_confirm == True:
            return True
        elif not self.player_1.groups() and self.player_2_confirm == True:
            return True
        elif self.player_1.groups() and self.player_1_confirm == True and self.player_2.groups() and self.player_2_confirm == True:
            return True
        else:
            return False

    def update_labels(self,dt):
        self.time -= dt / 1000.0
        text = str(int(self.time))
        self.label_0.original_text = text
        self.label_0.blink(dt)

        self.text_1 = 'credit {}'.format(self.coins)
        self.label_1.set_text(self.text_1)

    def update_bullets(self):
        if self.frame % 120 >= 60:
            if self.player_1.groups():
                bullet.PlayerLaserBullet(self,self.player_1,self.player_bullets)
            if self.player_2.groups():
                bullet.PlayerLaserBullet(self,self.player_2,self.player_bullets)
        else:
            if self.frame % 10 == 1:
                if self.player_1.groups():
                    bullet.PlayerWeapon1(self.player_1,self.player_bullets)
                if self.player_2.groups():
                    bullet.PlayerWeapon1(self.player_2,self.player_bullets)


    def update(self, dt):
        self.transition.fade_in()
        self.fade_effect = self.check_done()
        if self.fade_effect:
            self.done = self.transition.fade_out()
        self.frame += 1
        self.update_labels(dt)
        self.update_bullets()
        self.background.update()
        self.player_bullets.update(dt)
        self.players.update(dt)


    def draw(self, surface):
        self.background.draw(surface)
        
        self.player_bullets.draw(surface)
        self.players.draw(surface)

        surface.blit(self.mask,(0,0))
        if hasattr(self,'player_1_image'):
            surface.blit(self.player_1_image,self.player_1_rect)
        if hasattr(self,'player_2_image'):
            surface.blit(self.player_2_image,self.player_2_rect)
        surface.blit(self.player_1_power_image,self.player_1_power_rect)
        surface.blit(self.player_1_speed_image,self.player_1_speed_rect)
        surface.blit(self.player_1_name_image,self.player_1_name_rect)
        surface.blit(self.player_2_power_image,self.player_2_power_rect)
        surface.blit(self.player_2_speed_image,self.player_2_speed_rect)
        surface.blit(self.player_2_name_image,self.player_2_name_rect)
        self.labels.draw(surface)
        self.transition.draw(surface)



