import pygame as pg
from itertools import cycle
from ..prepare import GFX,SFX

class BulletExplsoion(pg.sprite.Sprite):
    def __init__(self, game, level,pos, *group):
        super(BulletExplsoion, self).__init__(*group)
        self.pos = pos
        self.game = game
        self.level = level
        i = self.game.frame % 50 + 1
        image = GFX['fire1_ {}{}'.format(i//10,i % 10)]
        size = image.get_size()
        self.image = pg.transform.scale(image,(int(size[0]/5.0*self.level),int(size[1]/5.0*self.level)))
        self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1] - int(20/5.0*self.level)))
        self.frame = 0

    def update(self):
        self.kill()

class EnemyExplosion(pg.sprite.Sprite):
    def __init__(self, game, enemy, *group):
        super(EnemyExplosion,self).__init__(*group)
        self.game = game
        self.enemy = enemy
        self.pos = self.enemy.pos
        self.frame = 0
        self.image = GFX['explosion_10001']
        self.rect = self.image.get_rect(center = self.pos)

    def update(self):
        self.frame += 1
        if self.frame >= 90:
            self.kill()
        else:
            self.o_image = GFX['explosion_100{}{}'.format(self.frame//10,self.frame%10)]
            w, h = self.o_image.get_size()
            a = self.enemy.image.get_width()
            ratio = a/150.0
            self.image = pg.transform.scale(self.o_image,(int(ratio*w),int(ratio*h)))
            self.rect = self.image.get_rect(center = self.pos)

class PlayerBomb(pg.sprite.Sprite):
    def __init__(self,player,group):
        super(PlayerBomb,self).__init__(group)
        self.player = player
        self.images = cycle((GFX['bm_0'],GFX['bm_{}'.format(self.player.id)]))
        self.image = next(self.images)
        self.rect = self.image.get_rect()
        self.frame = 0
        self.frame_time = 4
        self.bomb_time = 60.0

    def update(self,dt):
        self.frame += 1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.frame >= self.bomb_time:
            self.kill()
            self.player.bomb_on = False

class Exhaust(pg.sprite.Sprite):
    def __init__(self,enemy,delta_d,style,reverse):
        super(Exhaust,self).__init__()
        self.enemy = enemy
        self.delta_d = delta_d
        self.pos = (self.enemy.pos[0] + self.delta_d[0],self.enemy.pos[1] + self.delta_d[1])
        self.style = style
        if self.style == 1:
            if reverse:
                self.images = cycle([pg.transform.flip(GFX['exhaust{}'.format(x+1)],False,True) for x in range(8)])
            elif not reverse:
                self.images = cycle([GFX['exhaust{}'.format(x + 1)] for x in range(8)])
        elif self.style == 2:
            if reverse:
                self.images = cycle([pg.transform.flip(GFX['exhaust2_frame{}'.format(x+1)],False,True) for x in range(4)])
            elif not reverse:
                self.images = cycle([GFX['exhaust2_frame{}'.format(x+1)] for x in range(4)])
        elif self.style == 3:
            if reverse:
                self.images = cycle([pg.transform.flip(GFX['exhaust3_frame{}'.format(x+1)],False,True) for x in range(8)])
            elif not reverse:
                self.images = cycle([GFX['exhaust3_frame{}'.format(x+1)] for x in range(8)])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = self.pos)
        self.frame = 0

    def update(self):
        self.frame +=1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.enemy.groups():
            self.pos = (self.enemy.pos[0] + self.delta_d[0], self.enemy.pos[1] + self.delta_d[1])
            self.rect.center = self.pos
        elif not self.enemy.groups():
            self.kill()

class RotateRing(pg.sprite.Sprite):
    def __init__(self,enemy,size):
        super(RotateRing,self).__init__()
        self.enemy = enemy
        self.size = size
        self.pos = self.enemy.pos
        self.images = cycle([pg.transform.scale(GFX['d_00{}{}'.format(x//10,x%10)],(size,size)) for x in range(1,13)])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = self.pos)
        self.frame = 0

    def update(self):
        self.frame +=1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.enemy.groups():
            self.pos = self.enemy.pos
            self.rect.center = self.pos
        elif not self.enemy.groups():
            self.kill()

class Emerge1(pg.sprite.Sprite):
    def __init__(self,game,pos):
        super(Emerge1,self).__init__()
        self.tag = 'effect'
        self.pos = pos
        self.game = game
        self.images = [GFX['energe1_{}'.format(x)] for x in range(1,9)]
        self.i = 0
        self.image = self.images[self.i]
        self.rect = self.image.get_rect(center = self.pos)
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame % 4 == 1:
            self.i += 1
            if self.i >= 7:
                self.kill()
            else:
                self.image = self.images[self.i]


class Emerge2(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super(Emerge2, self).__init__()
        self.tag = 'effect'
        self.pos = pos
        self.game = game
        self.images = [GFX['energe2_{}'.format(x)] for x in range(1, 10)]
        self.i = 0
        self.image = self.images[self.i]
        self.rect = self.image.get_rect(center=self.pos)
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame % 4 == 1:
            self.i += 1
            if self.i >= 8:
                self.kill()
            else:
                self.image = self.images[self.i]

class WarningSign(pg.sprite.Sprite):
    def __init__(self,game,pos):
        super(WarningSign,self).__init__()
        self.tag = 'effect'
        self.game = game
        self.pos = pos
        self.images = cycle([GFX['warningitem'],GFX['name0']])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = (300,100))
        self.frame = 0
        SFX['alarm'].play()

    def update(self):
        self.frame += 1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.frame >= 120:
            self.kill()

class Cone(pg.sprite.Sprite):
    def __init__(self,game,pos):
        super(Cone,self).__init__(game.explosion_effect)
        self.game = game
        self.pos = pos
        self.images = cycle([pg.transform.flip(GFX['h_st_00{}{}'.format(x//10,x%10)],False,True) for x in range(1,16)])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = self.pos)
        self.frame = 0
        self.game.explosion_effect.add(self)

    def update(self):
        self.frame += 1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.frame >= 100:
            self.kill()

class EndingExplosion(pg.sprite.Sprite):
    def __init__(self,game):
        super(EndingExplosion,self).__init__(game.explosion_effect)
        self.game = game
        self.image = pg.Surface((600,800),pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame >= 254:
            self.game.stage_clear = True
            self.kill()
        self.image.fill((255,255,255,self.frame))

class Radar(Cone):
    def __init__(self,game,pos,reverse = False):
        super(Radar,self).__init__(game,pos)
        self.images = cycle([pg.transform.flip(GFX['{}{}'.format(x//10,x%10)],False,False) for x in range(13)])
        if reverse == True:
            self.images = cycle(
                [pg.transform.flip(GFX['{}{}'.format(x // 10, x % 10)], True,False) for x in range(13)])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = self.pos)
        self.frame = 0
        self.game.explosion_effect.add(self)

    def update(self):
        self.frame += 1
        self.pos = self.game.boss.pos
        self.rect.center = self.pos
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.frame >= 100:
            self.kill()


class Shield(RotateRing):
    def __init__(self,enemy,size):
        super(Shield,self).__init__(enemy,size)
        self.enemy = enemy
        self.size = size
        self.pos = self.enemy.pos
        self.images = cycle([pg.transform.scale(GFX['s{}{}'.format(x//10,x%10)],(size,size)) for x in range(1,12)])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = self.pos)
        self.frame = 0

    def update(self):
        self.pos = self.enemy.pos
        self.rect.center = self.pos
        self.frame +=1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.frame >= 60:
            self.kill()