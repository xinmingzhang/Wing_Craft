from random import randint
import pygame as pg
from ..prepare import GFX


class Star(pg.sprite.Sprite):
    def __init__(self,x,y,speed,*group):
        super(Star,self).__init__(*group)
        self.x = x
        self.y = y
        self.speed = speed
        if self.speed == 1:
            self.image = pg.Surface((1,1),pg.SRCALPHA)
            self.image.fill((255,255,255,175))
        elif self.speed == 2:
            self.image = pg.Surface((2,2),pg.SRCALPHA)
            pg.draw.circle(self.image,(255,255,255,175),(1,1),1)
        elif self.speed == 3:
            self.image = pg.Surface((3,3),pg.SRCALPHA)
            self.image.fill((255,255,255,175))
        elif self.speed == 4:
            self.image = pg.Surface((4,4),pg.SRCALPHA)
            pg.draw.circle(self.image,(255,255,255,200),(2,2),2)
        self.rect = self.image.get_rect(topleft = (self.x,self.y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.kill()


class Background(object):
    def __init__(self,level):
        self.stars = pg.sprite.Group()
        self.star_num = 20
        self.image = GFX['bg{}'.format(level)]
        self.image_h = self.image.get_height()
        self.camera_y = self.image_h - 800
        self.bg_image = pg.Surface((600,800))
        self.bg_image.blit(self.image.subsurface(0,self.camera_y,600,800),(0,0))
        self.bg_move_speed = 5
        for i in range(self.star_num):
            x = randint(0, 599)
            y = randint(0, 799)
            speed = randint(1,4)
            Star(x, y, speed,self.stars)

    def draw(self, surface):
        surface.blit(self.bg_image,(0,0))
        self.stars.draw(surface)

    def update(self):
        self.bg_move_speed -= 1
        if self.bg_move_speed <= 0:
            self.bg_move_speed = 5
            self.camera_y -= 1
            if self.camera_y <0:
                self.camera_y = self.image_h - 800
            self.bg_image.blit(self.image.subsurface(0, self.camera_y, 600, 800), (0, 0))
        self.stars.update()
        if len(self.stars)<self.star_num:
            x = randint(0, 599)
            y = 0
            speed = randint(1,4)
            Star(x, y, speed,self.stars)

