import random
from itertools import cycle
import pygame as pg
from ..prepare import GFX,WIDTH,HEIGHT,SCREENRECT
from ..components import angles

class Coin(pg.sprite.Sprite):
    name = 'coin'
    def __init__(self,game,pos,target = None):
        super(Coin,self).__init__(game.items)
        self.game = game
        self.pos = pos
        self.target = target
        self.luck = random.choice([20,22,25,27,30])
        acc_speed = random.randint(1,2)
        self.speed = self.luck / 4.0 + acc_speed
        self.value = self.luck * 100
        self.image = pg.transform.scale(GFX['coin'],(self.luck,self.luck))
        self.rect = self.image.get_rect(center = self.pos)
        self.direction = [0,1]
        self.frame = 0

    def check_kill(self):
        if self.rect.top > HEIGHT:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()

    def move(self):
        if self.target is not None:
            angle = angles.get_angle(self.pos,self.target.pos)
            self.direction =angles.project((0,0),angle,1)
            self.speed = 20
        self.pos = (self.direction[0] * self.speed + self.pos[0], self.direction[1] * self.speed + self.pos[1])
        self.rect.center = self.pos


    def update(self):
        self.frame += 1
        self.check_kill()
        self.move()

class BulletCoin(Coin):
    def __init__(self,game,pos,target):
        super(BulletCoin,self).__init__(game,pos,target)
        self.value = self.luck * 10
        self.image = pg.transform.scale(GFX['coin'], (self.luck, self.luck))

class Powerup(pg.sprite.Sprite):
    name = 'powerup'
    def __init__(self, game, pos):

        super(Powerup,self).__init__(game.items)

        self.game = game
        if self.game.frame % 4 == 0:
            self.direction = [1,1]
        elif self.game.frame % 4 == 1:
            self.direction = [1, -1]
        elif self.game.frame % 4 == 2:
            self.direction = [-1, -1]
        elif self.game.frame % 4 == 3:
            self.direction = [-1, 1]
        self.pos = pos

        self.images = cycle([GFX['power{}'.format(x)] for x in range(1,7)])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = self.pos)

        self.speed = 2
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame % 4 == 1:
            self.image = next(self.images)

        self.pos = (self.direction[0] * self.speed + self.pos[0],self.direction[1] * self.speed + self.pos[1])
        self.rect.center = self.pos

        if self.frame >= 3600:
            if self.rect.bottom > HEIGHT:
                self.kill()
            elif self.rect.top < 0:
                self.kill()
            elif self.rect.right > WIDTH:
                self.kill()
            elif self.rect.left < 0:
                self.kill()

        elif self.frame < 3600:

            if self.rect.top >= HEIGHT:
                self.direction[1] = - self.direction[1]
            elif self.rect.bottom <= 0:
                self.direction[1] = - self.direction[1]
            elif self.rect.left >= WIDTH:
                self.direction[0] = - self.direction[0]
            elif self.rect.right <= 0:
                self.direction[0] = - self.direction[0]


class Bomb(Powerup):
    name = 'bomb'
    def __init__(self, game, pos):
        super(Bomb,self).__init__(game,pos)
        self.images = cycle([GFX['bomb{}'.format(x)] for x in range(1,7)])


class Poison(Powerup):
    name = 'poison'
    def __init__(self, game, pos):
        super(Poison,self).__init__(game,pos)
        self.images = cycle([GFX['poison{}'.format(x)] for x in range(1,7)])

class Life(Powerup):
    name = 'life'
    def __init__(self, game, pos):
        super(Life,self).__init__(game,pos)
        self.images = cycle([GFX['life{}'.format(x)] for x in range(1,7)])