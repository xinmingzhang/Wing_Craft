import random
import pygame as pg
from ..prepare import GFX

class Transition(object):
    def __init__(self):
        self.mask = pg.Surface((600,800),pg.SRCALPHA)
        self.alpha_pixel_value_1 = 0
        self.alpha_pixel_value_2 = 255
        self.frame = 0

    def draw(self,surface):
        surface.blit(self.mask,(0,0))

    def fade_in(self):
        self.frame += 1
        if self.frame <= 51:
            self.mask.fill((0,0,0,self.alpha_pixel_value_2-self.frame*5))

    def fade_out(self):
        self.alpha_pixel_value_1 += 5
        self.mask.fill((0, 0, 0, self.alpha_pixel_value_1))
        if self.alpha_pixel_value_1 == self.alpha_pixel_value_2:
            return True





class Particle(pg.sprite.Sprite):
    def __init__(self, pos, *group):
        super(Particle, self).__init__(*group)
        self.image = GFX['particle']
        self.speed = [random.randint(1,10) * random.choice([-1,1]),random.randint(1,10)* random.choice([-1,1])]
        self.pos = list(pos)
        self.start = [self.pos[0] - self.speed[0] * 120,self.pos[1] - self.speed[1] * 120 ]
        self.rect = self.image.get_rect(center=self.start)
        self.frame = 0


    def update(self):
        self.frame += 1
        if self.frame <= 120:
            self.pos = [self.start[0] + self.frame * self.speed[0],self.start[1] + self.frame * self.speed[1]]
            self.rect.center = self.pos
        elif self.frame > 160:
            self.pos = [self.pos[0] - self.speed[0],self.pos[1] - self.speed[1]]
            self.rect.center = self.pos

class StageTransition(object):
    def __init__(self,level):
        self.level = level
        self.style = GFX['stage{}'.format(self.level)]
        self.pattern = pg.sprite.Group()
        for y in range(0, self.style.get_height(), 2):
            for x in range(0, self.style.get_width(), 2):
                if self.style.get_at((x, y))[3] != 0:
                    Particle((x + 220, y + 210), self.pattern)

        self.frame = 0
        self.bg = pg.Surface((600,800),pg.SRCALPHA)
        self.mask = pg.Surface((600,800),pg.SRCALPHA)


        self.alpha_pixel_value_1 = 0
        self.alpha_pixel_value_2 = 255
        self.frame = 0


    def draw(self,surface):
        self.bg.fill((0,0,0,255))
        self.pattern.draw(self.bg)
        self.bg.blit(self.mask,(0,0),special_flags = pg.BLEND_RGBA_SUB)
        surface.blit(self.bg,(0,0))

    def fade_in(self):
        self.frame += 1
        self.pattern.update()
        if  150 < self.frame <= 201:
            self.mask.fill((0,0,0,(self.frame - 150)*5))

    def fade_out(self):
        self.alpha_pixel_value_1 += 5
        self.bg.fill((0, 0, 0, self.alpha_pixel_value_1))
        if self.alpha_pixel_value_1 == self.alpha_pixel_value_2:
            return True