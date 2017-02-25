import math
import random
from itertools import cycle
import pygame as pg
from ..prepare import GFX,WIDTH,HEIGHT
from . import angles

class Bullet(pg.sprite.Sprite):
    def __init__(self, *group):
        super(Bullet,self).__init__(*group)

    def check_kill(self):
        if self.rect.top > HEIGHT:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()
        

    def update(self):
        pass


class PlayerLaserBullet(Bullet):
    speed = 10

    def __init__(self, game, player, *group):
        super(PlayerLaserBullet, self).__init__(*group)
        self.game = game
        self.player = player

        if self.player.id in (1, 2):
            self.pos = (self.player.pos[0], self.player.pos[1])
        if self.player.id in (3, 4):
            self.pos = (self.player.pos[0], self.player.pos[1] - 10)
        self.level = self.player.weapon_level

        assert 1 <= self.level <= 5

        self.image_choice()
        if self.game.frame % 8 <= 3:
            self.image = self.image_0
        elif self.game.frame % 8 >= 4:
            self.image = self.image_1

        self.rect = self.image.get_rect(center=self.pos)

    def image_choice(self):
        self.level = self.player.weapon_level
        if self.player.id == 1:
            self.image_0 = pg.transform.scale(GFX['1'], (self.level * 10, 30))
            self.image_1 = pg.transform.scale(GFX['2'], (self.level * 10, 30))
        elif self.player.id == 2:
            self.image_0 = pg.transform.scale(GFX['3'], (self.level * 10, 30))
            self.image_1 = pg.transform.scale(GFX['4'], (self.level * 10, 30))
        elif self.player.id == 3:
            self.image_0 = pg.transform.scale(GFX['5'], (self.level * 10, 30))
            self.image_1 = pg.transform.scale(GFX['6'], (self.level * 10, 30))
        elif self.player.id == 4:
            self.image_0 = pg.transform.scale(GFX['7'], (self.level * 10, 30))
            self.image_1 = pg.transform.scale(GFX['8'], (self.level * 10, 30))

    def update(self, dt):

        if self.player.weapon_2 == False:
            self.kill()
        self.image_choice()
        if self.game.frame % 8 <= 3:
            self.image = self.image_0
        elif self.game.frame % 8 >= 4:
            self.image = self.image_1

        self.rect = self.image.get_rect(center=self.pos)
        self.pos = (self.player.hitbox.rect.center[0], self.pos[1] - self.speed)
        self.rect.center = self.pos

        self.check_kill()


class PlayerBullet(Bullet):
    rot = 0
    speed = 50

    def __init__(self, player, angle, *group):
        super(PlayerBullet, self).__init__(*group)

        self.player = player
        self.level = self.player.weapon_level

        if self.player.id in (1, 2):
            self.pos = (self.player.pos[0], self.player.pos[1])
            PlayerBullet.rot = 0
        if self.player.id in (3, 4):
            self.pos = (self.player.pos[0], self.player.pos[1] - 10)
            if self.player.direction[0] == 0:
                PlayerBullet.rot = 0
            else:
                PlayerBullet.rot -= self.player.direction[0]

        self.angle = angle + self.rot
        self.direction = angles.project((0, 0), self.angle / 180.0 * math.pi , 1)
        self.transform_image()

    def transform_image(self):

        if self.player.id == 1:
            if self.level <= 3:
                self.image = GFX['bt11']
            elif self.level <= 5:
                self.image = GFX['bt12']

        elif self.player.id == 2:
            if self.level <= 3:
                self.image = GFX['bt8']
            elif self.level <= 5:
                self.image = GFX['bt9']

        elif self.player.id == 3:
            if self.level <= 3:
                self.image = GFX['bt5']
            elif self.level <= 5:
                self.image = GFX['bt6']

        elif self.player.id == 4:
            if self.level <= 3:
                self.image = GFX['bt2']
            elif self.level <= 5:
                self.image = GFX['bt3']

        rot_angle = self.angle - 90
        self.image = pg.transform.rotate(self.image, rot_angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.inflate_ip(-5, -5)

    def update(self, dt):
        self.pos = (self.direction[0] * self.speed + self.pos[0], self.direction[1] * self.speed + self.pos[1])
        self.rect.center = self.pos
        self.check_kill()


class PlayerWeapon1(object):
    def __init__(self, player, *group):
        self.player = player
        self.level = self.player.weapon_level
        if self.level == 1:
            PlayerBullet(player, 90, *group)
            PlayerBullet(player, 75, *group)
            PlayerBullet(player, 105, *group)
        elif self.level == 2:
            PlayerBullet(player, 90, *group)
            PlayerBullet(player, 75, *group)
            PlayerBullet(player, 105, *group)
            PlayerBullet(player, 60, *group)
            PlayerBullet(player, 120, *group)
        elif self.level == 3:
            PlayerBullet(player, 90, *group)
            PlayerBullet(player, 100, *group)
            PlayerBullet(player, 110, *group)
            PlayerBullet(player, 80, *group)
            PlayerBullet(player, 120, *group)
            PlayerBullet(player, 70, *group)
            PlayerBullet(player, 60, *group)
        elif self.level == 4:
            PlayerBullet(player, 90, *group)
            PlayerBullet(player, 75, *group)
            PlayerBullet(player, 105, *group)
            PlayerBullet(player, 60, *group)
            PlayerBullet(player, 120, *group)
        elif self.level == 5:
            PlayerBullet(player, 90, *group)
            PlayerBullet(player, 75, *group)
            PlayerBullet(player, 105, *group)
            PlayerBullet(player, 60, *group)
            PlayerBullet(player, 120, *group)
            PlayerBullet(player, 45, *group)
            PlayerBullet(player, 135, *group)


class PlayerWeapon2(object):
    def __init__(self, pos, *group):
        pass


class EnemyBullet(Bullet):
    def __init__(self, pos, angle, target, size, speed, group):
        super(EnemyBullet, self).__init__(group)
        self.pos = pos
        self.angle = angle / 180.0 * 3.14
        self.target = target
        self.size = size
        self.radius = self.size / 2.0
        self.speed = speed
        if self.target is None:
            self.delta_move = angles.project((0, 0), self.angle, self.speed)
        else:
            self.angle = angles.get_angle(self.pos, self.target)
            self.delta_move = angles.project((0, 0), self.angle, self.speed)
        self.image = pg.transform.scale(GFX['ebt3'], (self.size, self.size))
        self.rect = self.image.get_rect(center=self.pos)
        self.frame = 0

    def customize(self):
        pass

    def update_pos(self):
        self.pos = (self.pos[0] + self.delta_move[0], self.pos[1] + self.delta_move[1])
        self.rect.center = self.pos

    def update(self):
        self.frame += 1
        self.check_kill()
        self.update_pos()
        self.customize()

class PrivateBullet(EnemyBullet):
    def __init__(self,pos,target,group):
        super(PrivateBullet,self).__init__(pos, 0, target, 20, 6, group)
        # self.pos = pos
        # self.target = target
        # angle = angles.get_angle(self.pos,self.target)
        # self.delta_move = angles.project((0,0),angle,self.speed)
        # self.images = cycle([GFX['e_bt1'],GFX['e_bt2']])
        # self.image = next(self.images)
        # self.radius =self.image.get_width() / 2.0
        # self.rect = self.image.get_rect(center = self.pos)
        # self.frame = 0
    #
    # def update(self):
    #     self.frame += 1
    #     self.check_kill()
    #     if self.frame % 4 == 1:
    #         self.image = next(self.images)
    #     self.pos = (self.pos[0]+ self.delta_move[0], self.pos[1]+self.delta_move[1])
    #     self.rect.center = self.pos


class SergeantBullet(Bullet):
    speed = 5
    def __init__(self,pos,target,angle,*group):
        super(SergeantBullet,self).__init__(*group)
        self.pos = pos
        self.target = target
        self.angle = angle
        angle = angles.get_angle(self.pos,self.target)
        rot_angle = angle+self.angle/180.0*math.pi
        self.delta_move = angles.project((0,0),rot_angle , self.speed)

        self.image = pg.transform.rotate(GFX['e_bt101'], rot_angle/math.pi*180 + 90)
        self.rect = self.image.get_rect(center=self.pos)

        self.radius = self.image.get_width()/2.0
        self.frame = 0

    def update(self):
        self.frame += 1
        self.check_kill()
        self.pos = (self.pos[0] + self.delta_move[0], self.pos[1] + self.delta_move[1])
        self.rect.center = self.pos

class SergeantWeapon1(object):
    def __init__(self,pos,target,group):
        SergeantBullet(pos,target,0,group)
        SergeantBullet(pos,target,30,group)
        SergeantBullet(pos, target,-30, group)
        SergeantBullet(pos,target,60,group)
        SergeantBullet(pos, target,-60, group)

class SergeantWeapon2(object):
    def __init__(self,pos,target,group):
        SergeantBullet(pos, target, 20,group)
        SergeantBullet(pos, target, 40,group)
        SergeantBullet(pos, target, -20,group)
        SergeantBullet(pos, target,-40, group)
        SergeantBullet(pos, target, 60,group)
        SergeantBullet(pos, target,-60, group)
    
class CaptainBullet0(Bullet):
    speed = 4
    def __init__(self,pos,angle,*group):
        super(CaptainBullet0,self).__init__(*group)
        self.pos = pos
        self.angle = angle
        self.images = cycle([GFX['e_bt3'],GFX['e_bt4']])
        self.image = next(self.images)
        self.radius = self.image.get_width() / 2.0
        self.rect = self.image.get_rect(center = self.pos)
        self.delta_move = angles.project((0, 0), self.angle, self.speed)
        self.frame = 0



    def update(self):
        self.frame += 1
        self.check_kill()
        if self.frame % 4 == 1:
            self.image = next(self.images)
        self.pos = (self.pos[0] + self.delta_move[0], self.pos[1] + self.delta_move[1])
        self.rect.center = self.pos


class CaptainBullet1(Bullet):
    speed = 4
    def __init__(self,pos,angle,*group):
        super(CaptainBullet1,self).__init__(*group)
        self.pos = pos
        self.angle = angle
        self.size = 10
        self.image = pg.transform.scale(GFX['ebt3'],(self.size,self.size))
        self.radius = self.image.get_width() / 2.0
        self.rect = self.image.get_rect(center = self.pos)
        self.delta_move = angles.project((0, 0), self.angle, self.speed)
        self.frame = 0


    def update(self):
        self.frame += 1
        self.check_kill()
        if self.frame % 4 == 1:
            self.size += 1
        self.image = pg.transform.scale(GFX['ebt3'],(self.size,self.size))
        self.radius = self.image.get_width() / 2.0
        self.rect = self.image.get_rect(center=self.pos)
        self.pos = (self.pos[0] + self.delta_move[0], self.pos[1] + self.delta_move[1])
        self.rect.center = self.pos


class CorporalBullet(Bullet):
    speed = 5
    def __init__(self,p_center,p_radius,p_angle,target,*group):
        super(CorporalBullet,self).__init__(*group)
        self.p_center = p_center
        self.p_radius = p_radius
        self.p_angle = p_angle
        self.target = target
        angle = angles.get_angle(self.p_center,self.target)
        self.delta_move = angles.project((0,0),angle,self.speed)
        self.p_angle_rad = self.p_angle * 3.14/180
        self.pos = angles.project(self.p_center,self.p_angle_rad,self.p_radius)
        self.images = cycle([GFX['e_bt5'],GFX['e_bt6']])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center = self.pos)
        self.radius = self.image.get_width()/2.0
        self.frame = 0

    def update(self):
        self.frame += 1
        self.p_radius += 1
        self.check_kill()
        if self.frame % 4 == 1:
            self.image = next(self.images)
        self.p_center = (self.p_center[0] + self.delta_move[0], self.p_center[1] + self.delta_move[1])
        self.pos = angles.project(self.p_center, self.p_angle_rad, self.p_radius)
        self.rect.center = self.pos


class ColonelWeapon1(object):
    def __init__(self,pos,num,group):
        if num == 1:
            EnemyBullet(pos,-90,None,30,5,group)
        elif num == 2:
            EnemyBullet(pos,-85,None,28,5,group)
            EnemyBullet(pos,-95,None,28,5,group)
        elif num == 3:
            EnemyBullet(pos, -90, None, 26, 5, group)
            EnemyBullet(pos, -80, None, 26, 5, group)
            EnemyBullet(pos, -100, None, 26, 5, group)
        elif num == 4:
            EnemyBullet(pos,-85,None,24,5,group)
            EnemyBullet(pos,-95,None,24,5,group)
            EnemyBullet(pos,-75,None,24,5,group)
            EnemyBullet(pos,-105,None,24,5,group)
        elif num == 5:
            EnemyBullet(pos, -90, None, 22, 5, group)
            EnemyBullet(pos, -80, None, 22, 5, group)
            EnemyBullet(pos, -100, None, 22, 5, group)
            EnemyBullet(pos, -70, None, 22, 5, group)
            EnemyBullet(pos, -110, None, 22, 5, group)
        elif num == 6:
            EnemyBullet(pos,-85,None,20,5,group)
            EnemyBullet(pos,-95,None,20,5,group)
            EnemyBullet(pos,-75,None,20,5,group)
            EnemyBullet(pos,-105,None,20,5,group)
            EnemyBullet(pos,-65,None,20,5,group)
            EnemyBullet(pos,-115,None,20,5,group)
        elif num == 7:
            EnemyBullet(pos, -90, None, 18, 5, group)
            EnemyBullet(pos, -80, None, 18, 5, group)
            EnemyBullet(pos, -100, None, 18, 5, group)
            EnemyBullet(pos, -70, None, 18, 5, group)
            EnemyBullet(pos, -110, None, 18, 5, group)
            EnemyBullet(pos, -60, None, 18, 5, group)
            EnemyBullet(pos, -120, None, 18, 5, group)

class ColonelWeapon2(object):
    def __init__(self,pos,num,group):
        if num == 1:
            EnemyBullet(pos,-90,None,30,5,group)
        elif num == 2:
            EnemyBullet(pos,-85,None,28,5/math.cos(5/180.0*3.14),group)
            EnemyBullet(pos,-95,None,28,5/math.cos(5/180.0*3.14),group)
        elif num == 3:
            EnemyBullet(pos, -90, None, 26, 5, group)
            EnemyBullet(pos, -80, None, 26, 5/math.cos(10/180.0*3.14), group)
            EnemyBullet(pos, -100, None, 26, 5/math.cos(10/180.0*3.14), group)
        elif num == 4:
            EnemyBullet(pos,-85,None,24,5/math.cos(5/180.0*3.14),group)
            EnemyBullet(pos,-95,None,24,5/math.cos(5/180.0*3.14),group)
            EnemyBullet(pos,-75,None,24,5/math.cos(15/180.0*3.14),group)
            EnemyBullet(pos,-105,None,24,5/math.cos(15/180.0*3.14),group)
        elif num == 5:
            EnemyBullet(pos, -90, None, 22, 5, group)
            EnemyBullet(pos, -80, None, 22, 5/math.cos(10/180.0*3.14), group)
            EnemyBullet(pos, -100, None, 22, 5/math.cos(10/180.0*3.14), group)
            EnemyBullet(pos, -70, None, 22, 5/math.cos(20/180.0*3.14), group)
            EnemyBullet(pos, -110, None, 22, 5/math.cos(20/180.0*3.14), group)
        elif num == 6:
            EnemyBullet(pos,-85,None,20,5/math.cos(5/180.0*3.14),group)
            EnemyBullet(pos,-95,None,20,5/math.cos(5/180.0*3.14),group)
            EnemyBullet(pos,-75,None,20,5/math.cos(15/180.0*3.14),group)
            EnemyBullet(pos,-105,None,20,5/math.cos(15/180.0*3.14),group)
            EnemyBullet(pos,-65,None,20,5/math.cos(25/180.0*3.14),group)
            EnemyBullet(pos,-115,None,20,5/math.cos(25/180.0*3.14),group)
        elif num == 7:
            EnemyBullet(pos, -90, None, 18, 5, group)
            EnemyBullet(pos, -80, None, 18, 5/math.cos(10/180.0*3.14), group)
            EnemyBullet(pos, -100, None, 18, 5/math.cos(10/180.0*3.14), group)
            EnemyBullet(pos, -70, None, 18, 5/math.cos(20/180.0*3.14), group)
            EnemyBullet(pos, -110, None, 18, 5/math.cos(20/180.0*3.14), group)
            EnemyBullet(pos, -60, None, 18, 5/math.cos(30/180.0*3.14), group)
            EnemyBullet(pos, -120, None, 18, 5/math.cos(30/180.0*3.14), group)





class FLBulletA(Bullet):
    speed = 5
    def __init__(self,p_center,p_radius,p_angle,target,size,*group):
        super(FLBulletA,self).__init__(*group)
        self.p_center = p_center
        self.p_radius = p_radius
        self.p_angle = p_angle
        self.target = target
        self.size = size
        enemy_angle = angles.get_angle(self.p_center,self.target)
        self.delta_move = angles.project((0,0),enemy_angle,self.speed)
        self.p_angle_rad = self.p_angle * 3.14/180
        self.pos = angles.project(self.p_center,self.p_angle_rad,self.p_radius)
        self.image = pg.transform.scale(GFX['ebt3'],(self.size,self.size))
        self.rect = self.image.get_rect(center = self.pos)
        self.radius = self.image.get_width()/2.0
        self.frame = 0

    def update(self):
        self.frame += 1
        self.p_angle += 10
        self.p_radius += 0.5
        self.check_kill()
        self.p_center = (self.p_center[0] + self.delta_move[0], self.p_center[1] + self.delta_move[1])
        self.p_angle_rad = self.p_angle * 3.14/180
        self.pos = angles.project(self.p_center,self.p_angle_rad,self.p_radius)
        self.rect.center = self.pos

class FLBulletB(FLBulletA):
    speed = 5
    def __init__(self,p_center,p_radius,p_angle,target,size,*group):
        super(FLBulletB, self).__init__(p_center,p_radius,p_angle,target,size,*group)

    def update(self):
        self.frame += 1
        self.p_angle += 5
        self.p_radius -= 0.5
        self.check_kill()
        self.p_center = (self.p_center[0] + self.delta_move[0], self.p_center[1] + self.delta_move[1])
        self.p_angle_rad = self.p_angle * 3.14/180
        self.pos = angles.project(self.p_center,self.p_angle_rad,self.p_radius)
        self.rect.center = self.pos







class MajorBullet1(EnemyBullet):
    def __init__(self, pos, group):
        super(MajorBullet1, self).__init__(pos, -90, None,40,5,group)
        self.group = group
        self.frame = 0

    def customize(self):
        if self.frame == 60:
            self.kill()
            a = random.choice([3,5])
            if a == 3:
                for i in range(0,360):
                    if i % 60 != 0:
                        EnemyBullet(self.pos, i,None,10,10 * math.sin(3.0 * i / 180 * math.pi),self.group)
            elif a == 5:
                for i in range(0,360):
                    if i % 36 != 0:
                        EnemyBullet(self.pos, i,None,10,10 * math.sin(5.0 * i / 180 * math.pi),self.group)


class MajorBullet2(EnemyBullet):
    def __init__(self, pos, group):
        super(MajorBullet2, self).__init__(pos, -90, None,40,5,group)
        self.group = group
        self.frame = 0

    def customize(self):
        if self.frame == 60:
            self.kill()
            a = random.choice([4,2])
            if a == 4:
                for i in range(0,360):
                    if i % 45 != 0:
                        EnemyBullet(self.pos, i,None,10,10 * math.sin(4.0 * i / 180 * math.pi),self.group)
            elif a == 2:
                for i in range(0,360):
                    if i % 90 != 0:
                        EnemyBullet(self.pos, i,None,10,10 * math.sin(2.0 * i / 180 * math.pi),self.group)


class Boss1Pattern1(object):
    def __init__(self,pos,group):
        for i in range(0,360,20):
            EnemyBullet(pos,i,None,30,5,group)


class Boss1Pattern2(object):
    def __init__(self,pos,frame,group):
        CaptainBullet0(pos, -frame * 8, group)
        CaptainBullet0(pos, frame * 8, group)

class Boss2Bullet(pg.sprite.Sprite):
    def __init__(self,pos,enemy,reverse,group):
        super(Boss2Bullet,self).__init__(group)
        self.pos = pos
        self.enemy = enemy
        self.center = self.enemy.pos
        self.reverse = reverse
        self.d = angles.get_distance(self.center,self.pos)
        self.a = angles.get_angle(self.center,self.pos)
        self.image = pg.transform.scale(GFX['ebt1'],(30,30))
        self.rect = self.image.get_rect(center = self.pos)
        self.frame = 0


    def update(self):
        self.frame += 1
        if self.reverse:
            self.a -= 2.0 / 180 * 3.14
        else:
            self.a += 2.0 /180
        self.pos = angles.project(self.enemy.pos,self.a,self.d)
        self.rect.center = self.pos
        if self.frame >=200:
            self.kill()


class Boss2Weapon1(object):
    def __init__(self,enemy,group,reverse,num):
        if num == 1:
            for i in range(0,700,100):
                Boss2Bullet((i,0),enemy,reverse,group)
                Boss2Bullet((i,600),enemy,reverse,group)
            for j in range(100,600,100):
                Boss2Bullet((0,j),enemy,reverse,group)
                Boss2Bullet((600,j),enemy,reverse,group)
        if num == 2:
            for i in range(0,700,100):
                Boss2Bullet((i,600),enemy,reverse,group)
            for i in range(100,700,100):
                pos1 = angles.project((0,600),60*3.14/180,i)
                Boss2Bullet(pos1,enemy,reverse,group)
            for i in range(100,600,100):
                pos2 = angles.project((600,600),120*3.14/180,i)
                Boss2Bullet(pos2,enemy,reverse,group)

class Boss2B(pg.sprite.Sprite):
    def __init__(self, pos, angle,speed,reverse,group):
        super(Boss2B, self).__init__(group)
        self.pos = pos
        self.angle = angle / 180.0 * 3.14
        self.rot_angle = 0
        self.image = GFX['b2b0']
        self.o_image = GFX['b2b0']
        self.rect = self.image.get_rect(center = self.pos)
        self.radius = self.image.get_width() / 2.0
        self.speed = speed
        self.reverse = reverse
        self.direction = angles.project((0, 0), self.angle, 1)
        self.acc = -0.1
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.reverse:
            self.rot_angle -= 1
        else:
            self.rot_angle += 1
        rot_image = self.o_image.copy()
        self.image = pg.transform.rotate(rot_image,self.rot_angle)
        self.speed += self.acc
        self.pos = (self.pos[0]+ self.direction[0] *self.speed, self.pos[1] + self.direction[1]*self.speed)
        self.rect.center = self.pos
        if self.rect.top > HEIGHT:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()

class Boss2B1(Boss2B):
    def __init__(self, pos, angle,speed,reverse,group):
        super(Boss2B1, self).__init__(pos, angle,speed,reverse,group)
        self.r = 0


    def update(self):
        self.angle += 0.02
        self.r += 0.2
        if self.reverse:
            self.pos = angles.project(self.pos, -self.angle, -self.r)
        else:
            self.pos = angles.project(self.pos, self.angle, self.r)
        self.rect.center = self.pos
        if self.rect.top > HEIGHT:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()


class Boss2B2(Bullet):
    def __init__(self, pos, angle, size, speed, group):
        super(Boss2B2, self).__init__(group)
        self.pos = pos
        self.angle = angle
        self.size = size
        self.radius = self.size / 2.0
        self.speed = speed
        self.delta_move = angles.project((0, 0), self.angle / 180.0 * 3.14, self.speed)
        image = pg.transform.scale(GFX['b2b1'], (self.size,  2 *self.size))
        self.image = pg.transform.rotate(image,self.angle + 90)
        self.rect = self.image.get_rect(center=self.pos)
        self.frame = 0



    def update(self):
        self.check_kill()
        self.pos = (self.pos[0] + self.delta_move[0], self.pos[1] + self.delta_move[1])
        self.rect.center = self.pos
        if self.rect.top > HEIGHT:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > WIDTH:
            self.kill()
        elif self.rect.right < 0:
            self.kill()


class Boss2Weapon2(object):
    def __init__(self,pos, frame,group):
        Boss2B2(pos, -45+frame, 30, 10, group)
        Boss2B2(pos, 45 +frame, 30, 10, group)
        Boss2B2(pos, 135 +frame, 30, 10, group)
        Boss2B2(pos, -135 +frame, 30, 10, group)
class Boss4Bullet1(CorporalBullet):
    def __init__(self,p_center,p_radius,p_angle,target,*group):
        super(Boss4Bullet1,self).__init__(p_center,p_radius,p_angle,target,*group)
        self.image = pg.transform.scale(GFX['ebt3'],(10,10))

    def update(self):
        self.frame += 1
        self.p_angle += 5
        self.p_radius += 0.5

        self.check_kill()
        self.p_center = (self.p_center[0] + self.delta_move[0], self.p_center[1] + self.delta_move[1])
        self.p_angle_rad = self.p_angle * 3.14/180
        self.pos = angles.project(self.p_center, self.p_angle_rad, self.p_radius)
        self.rect.center = self.pos

class Boss4Bullet2(EnemyBullet):
    images = cycle([GFX['ebt{}'.format(x)] for x in range(5,12,1)])
    def __init__(self, pos, angle, target, size, speed, group):
        super(Boss4Bullet2, self).__init__(pos, angle, target, size, speed, group)
        self.group = group
        image = next(Boss4Bullet2.images)
        self.image = pg.transform.scale(image,(self.size,self.size))


    def update(self):
        self.frame += 1
        self.pos = (self.pos[0] + self.delta_move[0], self.pos[1] + self.delta_move[1])
        self.rect.center = self.pos
        if self.rect.bottom > HEIGHT:
            self.kill()
            if self.size > 20:
                Boss4Bullet2(self.pos,random.randint(10,170),None,self.size-10,5,self.group)
                Boss4Bullet2(self.pos, random.randint(10, 170), None, self.size-10, 5, self.group)
        elif self.rect.top < 0:
            self.kill()
            if self.size > 20:
                Boss4Bullet2(self.pos,random.randint(-170,-10),None,self.size-10,5,self.group)
                Boss4Bullet2(self.pos, random.randint(-170, -10), None, self.size-10, 5, self.group)
        elif self.rect.right > WIDTH:
            self.kill()
            if self.size > 20:
                Boss4Bullet2(self.pos,random.randint(100,260),None,self.size-10,5,self.group)
                Boss4Bullet2(self.pos, random.randint(100, 260), None, self.size-10, 5, self.group)
        elif self.rect.left < 0:
            self.kill()
            if self.size > 20:
                Boss4Bullet2(self.pos,random.randint(-80,80),None,self.size-10,5,self.group)
                Boss4Bullet2(self.pos, random.randint(-80, 80), None, self.size-10, 5, self.group)


class Boss4Weappon1(object):
    def __init__(self,pos,target, num, group):
        self.pos = pos
        for angle in range(0, 360, 10):
            a = angle % (360/num)
            p_radius = abs(a - (180/num))
            Boss4Bullet1(self.pos,p_radius,angle,target,group)

class Boss5Bullet(Boss4Bullet2):
    def __init__(self,game, pos, angle, target,  group):
        super(Boss5Bullet, self).__init__(pos, angle, target, 40, 3, group)
        self.game = game

    def find_target_pos(self):
        p1 = self.game.player_1
        p2 = self.game.player_2
        if p1.groups() and p2.groups():
            d1 = angles.get_distance(self.pos, p1.pos)
            d2 = angles.get_distance(self.pos, p2.pos)
            if d1 >= d2:
                return p1.pos
            else:
                return p2.pos
        elif p1.groups() and not p2.groups():
            return p1.pos
        elif p2.groups() and not p1.groups():
            return p2.pos
        else:
            return self.pos

    def update(self):
        self.frame += 1
        target = self.find_target_pos()
        self.angle = angles.get_angle(self.pos, target)
        self.delta_move = angles.project((0, 0), self.angle, self.speed)
        self.pos = (self.pos[0] + self.delta_move[0], self.pos[1] + self.delta_move[1])
        self.rect.center = self.pos
        if self.frame >= 500:
            self.kill()



