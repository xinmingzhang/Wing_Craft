from itertools import cycle
import pygame as pg
from ..prepare import GFX,SCREENRECT,SFX
from ..tools import strip_from_sheet
from .explosion import PlayerBomb
from .items import BulletCoin,Powerup



class Player(pg.sprite.Sprite):
    def __init__(self, game, pos, id, *group):
        super(Player, self).__init__(*group)
        self.game = game
        self.pos = pos
        self.id = id
        self.direction = [0, 0]
        self.lives = 3
        self.score = 0
        self.bomb_num = 3
        self.invincible = True
        self.invincible_time = 60
        self.weapon_level = 1
        self.set_image()
        self.set_speed()
        self.set_hitbox()

        self.frame_time = 4
        self.weapon_time = 10000000000
        self.weapon_1 = False
        self.weapon_2 = False
        self.bomb_on = False
        self.weapon_toggle_time = 300


        self.explosion = False
        self.explosion_time = 60
        self.explosion_frame = 0

        self.bullet_damage = self.weapon_level



    def set_image(self):
        pf = pg.transform.flip
        if self.id == 1:
            self.image_dict = {
                'default': cycle([GFX['cricket10'], GFX['cricket11'], GFX['cricket12'], GFX['cricket11']]),
                'left': cycle([GFX['cricket13'], GFX['cricket14'], GFX['cricket15'], GFX['cricket14']]),
                'right': cycle(
                    [pf(GFX['cricket13'], True, False), pf(GFX['cricket14'], True, False), pf(GFX['cricket15'], True, False),
                     pf(GFX['cricket14'], True, False)])}
            self.explosion_images = strip_from_sheet(GFX['player_explosion_1'], (0, 0), (90, 90), 10)
        elif self.id == 2:
            self.image_dict = {
                'default': cycle([GFX['cricket20'], GFX['cricket21'], GFX['cricket22'], GFX['cricket21']]),
                'left': cycle([GFX['cricket23'], GFX['cricket24'], GFX['cricket25'], GFX['cricket24']]),
                'right': cycle(
                    [pf(GFX['cricket23'], True, False), pf(GFX['cricket24'], True, False), pf(GFX['cricket25'], True, False),
                     pf(GFX['cricket24'], True, False)])}

            self.explosion_images = strip_from_sheet(GFX['player_explosion_1'], (0, 0), (90, 90), 10)

        elif self.id == 3:
            self.image_dict = {
                'default': cycle([GFX['locust10'], GFX['locust11'], GFX['locust12'], GFX['locust11']]),
                'left': cycle([GFX['locust13'], GFX['locust14'], GFX['locust15'], GFX['locust14']]),
                'right': cycle(
                    [pf(GFX['locust13'], True, False), pf(GFX['locust14'], True, False),
                     pf(GFX['locust15'], True, False),
                     pf(GFX['locust14'], True, False)])}
            self.explosion_images = strip_from_sheet(GFX['player_explosion_2'], (0, 0), (90, 90), 10)
        elif self.id == 4:
            self.image_dict = {
                'default': cycle([GFX['locust20'], GFX['locust21'], GFX['locust22'], GFX['locust21']]),
                'left': cycle([GFX['locust23'], GFX['locust24'], GFX['locust25'], GFX['locust24']]),
                'right': cycle(
                    [pf(GFX['locust23'], True, False), pf(GFX['locust24'], True, False),
                     pf(GFX['locust25'], True, False),
                     pf(GFX['locust24'], True, False)])}
            self.explosion_images = strip_from_sheet(GFX['player_explosion_2'], (0, 0), (90, 90), 10)
        self.images = self.image_dict['default']
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = self.pos)

    def set_speed(self):
        if self.id in (1,2):
            self.speed = 5
        elif self.id in (3,4):
            self.speed = 6

    def set_hitbox(self):
        self.hitbox = pg.sprite.Sprite()
        self.hitbox.image = pg.Surface((8,8))
        self.radius = 4
        if self.id in (1,2):
            self.hitbox.rect = self.hitbox.image.get_rect(center = (self.pos[0], self.pos[1]+5))
        elif self.id in (3,4):
            self.hitbox.rect = self.hitbox.image.get_rect(center=(self.pos[0], self.pos[1] - 15))



    def hit_box_pos_update(self):
        if self.id in (1,2):
            if 1 >= self.direction[0] > 0:
                self.hitbox.rect.center = (self.pos[0] + 4, self.pos[1] + 5)
            elif 0 > self.direction[0] >= -1:
                self.hitbox.rect.center = (self.pos[0] - 4, self.pos[1] + 5)
            else:
                self.hitbox.rect.center = (self.pos[0], self.pos[1] + 5)
        elif self.id in (3,4):
            if 1 >= self.direction[0] > 0:
                self.hitbox.rect.center = (self.pos[0] + 4, self.pos[1] - 15)
            elif 0 > self.direction[0] >= -1:
                self.hitbox.rect.center = (self.pos[0] - 4, self.pos[1] - 15)
            else:
                self.hitbox.rect.center = (self.pos[0], self.pos[1] - 15)

    def check_invicible(self):
        if self.invincible == True:
            self.invincible_time -= 1
            if self.invincible_time <= 0:
                self.invincible = False
                self.invincible_time = 60
            if self.id in (1,2):
                self.image = GFX['cricket']
            elif self.id in (3,4):
                self.image = GFX['locust']

    def get_killed(self):
        self.explosion_frame += 1
        if self.explosion_frame < 20:
            self.image = self.explosion_images[self.explosion_frame//2]
            self.rect = self.image.get_rect(center = self.pos)
        elif 20 <= self.explosion_frame < self.explosion_time:
            self.image = GFX['name0']
        elif self.explosion_frame > self.explosion_time:
            self.explosion_frame = 0
            self.lives -= 1
            self.weapon_level = 1
            Powerup(self.game,(self.pos[0],30))
            if self.lives > 0:
                self.invincible = True
                self.explosion = False
                if self.id in (1,3):
                    self.pos = (150, 700)
                elif self.id in (2,4):
                    self.pos = (450, 700)
                self.bomb_num = 3
            elif self.lives <= 0:
                self.kill()


    def item_collide(self,item):
        if item.name == 'coin':
            self.score += item.value
        elif item.name == 'powerup':
            SFX['powerup'].play()
            if self.weapon_level < 5:
                self.weapon_level += 1
            else:
                self.score += 50000
        elif item.name == 'bomb':
            SFX['bomb'].play()
            self.bomb_num += 1
        elif item.name == 'life':
            SFX['life'].play()
            self.lives += 1
        elif item.name == 'poison':
            SFX['poison'].play()
            self.weapon_level = 1
            try:
                self.game.boss.health = self.game.boss.o_health
            except:
                pass

    def get_bullet_score(self):
        self.score += 10
        self.score += self.weapon_level


    def check_bomb(self):
        if self.bomb_on == False and not self.explosion and self.bomb_num >= 1:
            self.invincible = True
            self.bomb_num -= 1
            self.bomb_on = True
            PlayerBomb(self,self.groups())
        else:
            pass


    def weapon_effect(self):
        if self.weapon_2 == True:
            if self.id in (1, 2):
                self.speed = 4
                self.bullet_damage = 2 * (1.0 + self.weapon_level / 10.0)
            elif self.id in (3, 4):
                self.speed = 5
                self.bullet_damage = 2 * (0.8 + self.weapon_level / 10.0)
        else:
            if self.id in (1, 2):
                self.speed = 5
                self.bullet_damage = 1.0 + self.weapon_level / 10.0
            elif self.id in (3, 4):
                self.speed = 6
                self.bullet_damage = 0.8 + self.weapon_level / 10.0

    def bomb_effect(self):
        for enemy in self.game.enemies:
            enemy.get_bomb_damage()
        for bullet in self.game.enemy_bullets:
            BulletCoin(self.game, bullet.pos, self)
            bullet.kill()




    def move(self):

        if 1 >= self.direction[0] > 0:
            self.images = self.image_dict['right']
        elif 0 > self.direction[0] >= -1:
            self.images = self.image_dict['left']
        else:
            self.images = self.image_dict['default']
        self.frame_time -= 1
        if self.frame_time <= 0:
            self.frame_time = 4
            self.image = next(self.images)

        self.check_invicible()
        if self.direction[0] * self.direction[1] in (1, -1):
            self.direction = [self.direction[0] * 0.7071, self.direction[1] * 0.7071]
        self.pos = (self.direction[0] * self.speed + self.pos[0], self.direction[1] * self.speed + self.pos[1])
        self.rect = self.image.get_rect(center = self.pos)
        self.rect.center = self.pos
        r = self.rect.clamp(SCREENRECT)
        if r != self.rect:
            self.direction[0] = 0
            self.rect = r
            self.pos = self.rect.center


    def update(self, dt):
        if not self.explosion:
            self.weapon_effect()
            self.move()
            self.hit_box_pos_update()
        elif self.explosion:
            self.get_killed()





