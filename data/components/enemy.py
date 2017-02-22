import random
from itertools import cycle
import pygame as pg
from . import bullet
from .explosion import EnemyExplosion, Emerge2, Exhaust, RotateRing, Cone, EndingExplosion, Radar
from .angles import get_angle, get_distance, project
from ..prepare import GFX, SCREENRECT
from .items import Coin, Powerup, Bomb, Life


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super(Enemy, self).__init__()
        self.tag = 'enemy'
        self.game = game
        self.pos = pos
        self.hit_box = pg.sprite.Sprite()
        self.frame = 0

    def find_target_pos(self):
        p1 = self.game.player_1
        p2 = self.game.player_2
        if p1.groups() and p2.groups():
            d1 = get_distance(self.pos, p1.pos)
            d2 = get_distance(self.pos, p2.pos)
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

    def get_damage(self, player):
        damage = player.bullet_damage
        self.health -= damage

    def get_bomb_damage(self):
        if SCREENRECT.collidepoint(self.pos):
            self.health -= 15

    def update_pos(self):
        pass

    def update_img(self):
        pass

    def check_death(self):
        pass

    def check_shoot(self):
        pass

    def custom(self):
        pass

    def update(self):
        self.frame += 1
        self.update_pos()
        self.update_img()
        self.check_shoot()
        self.check_death()
        self.custom()


class Private0(Enemy):
    def __init__(self, game, pos):
        super(Private0, self).__init__(game, pos)
        self.health = 10
        self.speed = 7
        self.s_pos = self.pos
        self.e_pos = self.find_target_pos()

        self.image = GFX['e_private0']
        self.orig_image = GFX['e_private0']
        self.image_rot_angle = 0
        self.rect = self.image.get_rect(center=self.s_pos)

        self.hit_box.image = pg.Surface((20, 20))
        self.hit_box.rect = self.hit_box.image.get_rect(center=(self.pos[0], self.pos[1] - 6))
        self.hit_box.body = self

    def update_pos(self):
        if self.s_pos == self.e_pos:
            self.kill()
            self.hit_box.kill()
        elif self.s_pos[0] == self.e_pos[0]:
            self.pos = (self.s_pos[0], self.s_pos[1] + self.speed * self.frame)
            if self.e_pos[1] > self.s_pos[1]:
                self.image_rot_angle = 0
            elif self.e_pos[1] < self.s_pos[1]:
                self.image_rot_angle = 180
        elif self.s_pos[1] == self.e_pos[1]:
            self.pos = (self.s_pos[0] + self.speed * self.frame, self.s_pos[1])
            if self.e_pos[0] > self.s_pos[0]:
                self.image_rot_angle = 90
            elif self.e_pos[0] < self.s_pos[0]:
                self.image_rot_angle = -90
        else:
            # parabola curve
            y = self.s_pos[1] + self.frame * self.speed
            p = -(self.s_pos[1] - self.e_pos[1]) * (self.s_pos[1] - self.e_pos[1]) / 2.0 / (
                self.s_pos[0] - self.e_pos[0])
            x = (y - self.s_pos[1]) ** 2 / 2.0 / p + self.s_pos[0]
            self.pos = (x, y)

            angle = get_angle(self.pos, self.e_pos) / 6.28 * 360
            if self.e_pos[0] > self.s_pos[0]:
                if self.e_pos[0] > self.pos[0]:
                    self.image_rot_angle = angle + 90
                elif self.e_pos[0] < self.pos[0]:
                    self.image_rot_angle = angle - 90
            if self.e_pos[0] < self.s_pos[0]:
                if self.e_pos[0] < self.pos[0]:
                    self.image_rot_angle = angle + 90
                elif self.e_pos[0] > self.pos[0]:
                    self.image_rot_angle = angle - 90
        self.rect.center = self.pos
        self.hit_box.rect.center = (self.pos[0], self.pos[1] - 6)

    def update_img(self):
        rot_image = self.orig_image.copy()
        self.image = pg.transform.rotate(rot_image, self.image_rot_angle)

    def check_death(self):
        if self.frame >= 200:
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            Coin(self.game, self.pos, None)
            self.kill()
            self.hit_box.kill()


class Private1(Enemy):
    def __init__(self, game, pos):
        super(Private1, self).__init__(game, pos)
        self.target = self.find_target_pos()
        self.health = 20
        self.image = GFX['e_private1_body']
        self.r = self.image.get_width() / 2
        self.image1 = self.image.copy()
        self.turret_image = GFX['e_private1_turret']
        self.gun_image = GFX['e_private1_gun']
        self.orig_image0 = GFX['e_private1']
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 2
        self.direction = [0, 1]
        self.rot_ang = 0
        self.hit_box.image = pg.Surface((40, 40))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.bullet_pos = self.pos
        self.fire_on = False

    def update_img(self):
        angle = get_angle(self.pos, self.target)
        self.bullet_pos = project(self.pos, angle, self.r)
        rot_ang = angle / 6.28 * 360 + 90
        self.image = self.image1.copy()
        rot_image = self.turret_image.copy()
        o_size = rot_image.get_size()
        self.t_image = pg.transform.rotate(rot_image, rot_ang)
        r_size = self.t_image.get_size()
        a, b = (r_size[0] - o_size[0]) / 2, (r_size[1] - o_size[1]) / 2
        self.image.blit(self.t_image, (-a, -b))
        self.image.blit(self.gun_image, (0, 0))

    def update_pos(self):
        self.pos = (self.pos[0], self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        self.hit_box.rect.center = self.pos

    def check_shoot(self):
        if self.frame % 90 >= 60:
            self.fire_on = True
            if self.frame % 6 == 1:
                self.target = self.find_target_pos()
                bullet.PrivateBullet(self.bullet_pos, self.target, self.game.enemy_bullets)
        else:
            self.fire_on = False

    def check_death(self):
        if self.rect.top >= 800:
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            a = (self.pos[0] - 10, self.pos[1] - 10)
            b = (self.pos[0] + 10, self.pos[1] + 10)
            Coin(self.game, a, None)
            Coin(self.game, b, None)
            self.kill()
            self.hit_box.kill()


class Corporal0(Enemy):
    def __init__(self, game, pos):
        super(Corporal0, self).__init__(game, pos)
        self.target = self.find_target_pos()
        self.health = 100
        self.speed = 1
        self.direction = [0, 1]
        self.pos = self.pos
        self.image = pg.transform.flip(GFX['e_corporal0'], False, True)
        self.radius = self.image.get_width() / 2.0
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((44, 50))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.exhaust = Exhaust(self, (0, -90), 1, True)
        self.frame = 0

    def check_shoot(self):
        if self.frame % 200 > 100:
            if self.frame % 200 == 150:
                self.target = self.find_target_pos()
                angle = get_angle(self.pos, self.target) * 180 / 3.14
                for i in range(0, 360, 15):
                    a = angle - i
                    if a >= 30 or a <= -30:
                        bullet.CorporalBullet(self.pos, 0, i, self.target, self.game.enemy_bullets)

    def update_pos(self):
        self.pos = (self.pos[0], self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        self.hit_box.rect.center = self.pos

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust)

    def check_death(self):
        if self.rect.top >= 800:
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            for i in range(3):
                Coin(self.game, (self.pos[0] + random.randint(-20, 20), self.pos[1] + random.randint(-25, 25)), None)
            self.kill()
            self.hit_box.kill()


class Sergeant0(Enemy):
    def __init__(self, game, pos):
        super(Sergeant0, self).__init__(game, pos)
        self.target = self.find_target_pos()
        self.health = 300
        self.speed = 1
        self.direction = [0, 1]
        self.image = pg.transform.flip(GFX['e_sergeant0'], False, True)
        self.radius = self.image.get_width() / 2.0
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((60, 60))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.exhaust1 = Exhaust(self, (-15, -90), 1, True)
        self.exhaust2 = Exhaust(self, (15, -90), 1, True)
        self.frame = 0

    def shoot(self):
        self.target = self.find_target_pos()
        angle = get_angle(self.pos, self.target) * 180 / 3.14
        pos1 = (self.pos[0] - 40, self.pos[1] + 55)
        pos2 = (self.pos[0] + 40, self.pos[1] + 55)
        bullet.SergeantWeapon2(pos1, self.target, self.game.enemy_bullets)
        bullet.SergeantWeapon2(pos2, self.target, self.game.enemy_bullets)

    def update_pos(self):
        self.pos = (self.pos[0], self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        self.hit_box.rect.center = self.pos

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)

    def check_shoot(self):
        if self.frame % 200 > 100:
            if self.frame % 10 == 1:
                self.shoot()

    def check_death(self):
        if self.rect.top >= 800:
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            for i in range(5):
                Coin(self.game, (self.pos[0] + random.randint(-30, 30), self.pos[1] + random.randint(-30, 30)), None)
            self.kill()
            self.hit_box.kill()


class Sergeant1(Sergeant0):
    def __init__(self, game, pos):
        super(Sergeant1, self).__init__(game, pos)
        self.image = pg.transform.flip(GFX['e_sergeant1'], False, True)

    def shoot(self):
        self.target = self.find_target_pos()
        angle = get_angle(self.pos, self.target) * 180 / 3.14
        pos1 = (self.pos[0] - 40, self.pos[1] + 55)
        pos2 = (self.pos[0] + 40, self.pos[1] + 55)
        bullet.SergeantWeapon1(pos1, self.target, self.game.enemy_bullets)
        bullet.SergeantWeapon1(pos2, self.target, self.game.enemy_bullets)


class SecondLieutenant0(Enemy):
    def __init__(self, game, pos):
        super(SecondLieutenant0, self).__init__(game, pos)
        self.health = 400
        self.speed = 0.5
        self.pos = self.pos
        self.direction = [0, -1]
        self.image = pg.transform.flip(GFX['e_secondlieutenant0'], False, False)
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((50, 180))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.exhaust1 = Exhaust(self, (0, 150), 3, False)
        self.exhaust2 = Exhaust(self, (10, 150), 3, False)
        self.exhaust3 = Exhaust(self, (-10, 150), 3, False)
        self.frame = 0


        self.w = self.image.get_width() / 2.0
        self.h = self.image.get_height() / 2.0
        self.effect_images = cycle([GFX['e_00{}{}'.format((x + 1) // 10, (x + 1) % 10)] for x in range(10)])
        self.effect_image = next(self.effect_images)
        self.shoot_on = False

    def shoot(self):
        pos0 = (self.pos[0] - 43, self.pos[1] + 90)
        pos1 = (self.pos[0] + 43, self.pos[1] + 90)
        pos2 = (self.pos[0] - 43, self.pos[1] + 30)
        pos3 = (self.pos[0] + 43, self.pos[1] + 30)
        pos4 = (self.pos[0] - 43, self.pos[1] - 40)
        pos5 = (self.pos[0] + 43, self.pos[1] - 40)
        bullet.EnemyBullet(pos0, 180, None, 20,5, self.game.enemy_bullets)
        bullet.EnemyBullet(pos1, 0, None, 20, 5,self.game.enemy_bullets)
        bullet.EnemyBullet(pos2, 180, None, 20,5, self.game.enemy_bullets)
        bullet.EnemyBullet(pos3, 0, None,20,5, self.game.enemy_bullets)
        bullet.EnemyBullet(pos4, 180, None,20, 5,self.game.enemy_bullets)
        bullet.EnemyBullet(pos5, 0, None,20, 5,self.game.enemy_bullets)


    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)
            self.game.explosion_effect.add(self.exhaust3)
        if self.shoot_on == True:

            self.image = pg.transform.flip(GFX['e_secondlieutenant0'], False, False)
            self.image.blit(self.effect_image, (self.w - 32 - 43, self.h - 32 +90 ))
            self.image.blit(self.effect_image, (self.w - 32 + 43, self.h - 32 + 90))
            self.image.blit(self.effect_image, (self.w - 32 - 43, self.h - 32 + 30))
            self.image.blit(self.effect_image, (self.w - 32 + 43, self.h - 32 + 30))
            self.image.blit(self.effect_image, (self.w - 32 - 43, self.h - 32 - 40))
            self.image.blit(self.effect_image, (self.w - 32 + 43, self.h - 32 - 40))
            self.effect_image = next(self.effect_images)
        else:
            self.image = pg.transform.flip(GFX['e_secondlieutenant0'], False, False)

    def update_pos(self):
        self.pos = (self.pos[0], self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        self.hit_box.rect.center = self.pos

    def check_shoot(self):
        if self.frame % 200 > 150:
            if self.frame % 10 == 1:
                self.shoot_on = True
                self.shoot()
                self.direction = [0, 0]
        else:
            self.shoot_on = False
            self.direction = [0, -1]

    def check_death(self):
        if self.rect.bottom <= 0:
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            for i in range(7):
                Coin(self.game, (self.pos[0] + random.randint(-25, 25), self.pos[1] + random.randint(-90, 90)), None)
            self.kill()
            self.hit_box.kill()


class SecondLieutenant1(SecondLieutenant0):
    def __init__(self, game, pos):
        super(SecondLieutenant1, self).__init__(game, pos)
        self.speed = 0.5
        self.image = pg.transform.flip(GFX['e_secondlieutenant1'], False, False)
        self.exhaust1 = Exhaust(self, (0, 160), 3, False)
        self.exhaust2 = Exhaust(self, (10, 160), 3, False)
        self.exhaust3 = Exhaust(self, (-10, 160), 3, False)

    def shoot(self):
        pos0 = (self.pos[0], self.pos[1] - 88)
        pos1 = (self.pos[0], self.pos[1] - 50)
        pos2 = (self.pos[0], self.pos[1] - 13)
        pos3 = (self.pos[0], self.pos[1] + 24)
        pos4 = (self.pos[0], self.pos[1] + 60)
        bullet.EnemyBullet(pos0, 135 + self.frame,None, 15,5, self.game.enemy_bullets)
        bullet.EnemyBullet(pos1, 45 + self.frame,None, 15,5, self.game.enemy_bullets)
        bullet.EnemyBullet(pos2, 90 + self.frame, None,15, 5,self.game.enemy_bullets)
        bullet.EnemyBullet(pos3, 215 + self.frame, None,15,5, self.game.enemy_bullets)
        bullet.EnemyBullet(pos4, 305 + self.frame,None, 15, 5,self.game.enemy_bullets)

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)
            self.game.explosion_effect.add(self.exhaust3)
        if self.shoot_on == True:

            self.image = pg.transform.flip(GFX['e_secondlieutenant1'], False, False)
            self.image.blit(self.effect_image, (self.w - 32 , self.h - 32 -88 ))
            self.image.blit(self.effect_image, (self.w - 32, self.h - 32 -50))
            self.image.blit(self.effect_image, (self.w - 32, self.h - 32 -13))
            self.image.blit(self.effect_image, (self.w - 32, self.h - 32 + 24))
            self.image.blit(self.effect_image, (self.w - 32, self.h - 32 +60))
            self.effect_image = next(self.effect_images)
        else:
            self.image = pg.transform.flip(GFX['e_secondlieutenant1'], False, False)


class FirstLieutenant0(Enemy):
    def __init__(self, game, pos):
        super(FirstLieutenant0, self).__init__(game, pos)
        self.health = 400
        self.speed = 0.5
        self.pos = self.pos
        self.direction = [0, 1]
        self.image = pg.transform.flip(GFX['e_firstlieutenant0'], False, True)
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((80, 50))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.exhaust1 = Exhaust(self, (-24, -90), 1, True)
        self.exhaust2 = Exhaust(self, (+24, -90), 1, True)
        self.frame = 0

    def shoot(self):
        pos0 = (self.pos[0] - 20, self.pos[1] + 40)
        pos1 = (self.pos[0] + 20, self.pos[1] + 40)
        if self.game.player_1.groups() and self.game.player_2.groups():
            bullet.FLBulletA(pos0, 10, 0, self.game.player_1.pos, 15, self.game.enemy_bullets)
            bullet.FLBulletA(pos1, 10, 0, self.game.player_2.pos, 15, self.game.enemy_bullets)
        else:
            target = self.find_target_pos()
            bullet.FLBulletA(pos0, 10, 0, target, 15, self.game.enemy_bullets)
            bullet.FLBulletA(pos1, 10, 0, target, 15, self.game.enemy_bullets)

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)

    def update_pos(self):
        self.pos = (self.pos[0], self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        self.hit_box.rect.center = self.pos

    def check_shoot(self):
        if self.frame % 200 > 100:
            if self.frame % 5 == 1:
                self.shoot()

    def check_death(self):
        if self.rect.top >= 800:
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            for i in range(9):
                Coin(self.game, (self.pos[0] + random.randint(-40, 40), self.pos[1] + random.randint(-25, 25)), None)
            self.kill()
            self.hit_box.kill()


class FirstLieutenant1(FirstLieutenant0):
    def __init__(self, game, pos):
        super(FirstLieutenant1, self).__init__(game, pos)
        self.image = pg.transform.flip(GFX['e_firstlieutenant1'], False, True)

    def shoot(self):
        pos0 = (self.pos[0] - 20, self.pos[1] + 40)
        pos1 = (self.pos[0] + 20, self.pos[1] + 40)
        if self.game.player_1.groups() and self.game.player_2.groups():
            bullet.FLBulletB(pos0, 30, 0, self.game.player_1.pos, 15, self.game.enemy_bullets)
            bullet.FLBulletB(pos1, 30, 0, self.game.player_2.pos, 15, self.game.enemy_bullets)
        else:
            target = self.find_target_pos()
            bullet.FLBulletB(pos0, 30, 0, target, 15, self.game.enemy_bullets)
            bullet.FLBulletB(pos1, 30, 0, target, 15, self.game.enemy_bullets)


class Captain0(Enemy):
    def __init__(self, game, pos):
        super(Captain0, self).__init__(game, pos)
        self.health = 100
        self.speed = 0.5
        self.pos = self.pos
        self.direction = [0, 1]
        self.image = pg.transform.flip(GFX['e_captain0'], False, True)
        self.radius = self.image.get_width() / 2.0
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((60, 60))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.effect_images = cycle([GFX['e_00{}{}'.format((x + 1) // 10, (x + 1) % 10)] for x in range(10)])
        self.effect_image = next(self.effect_images)
        self.frame = 0

    def shoot(self):
        bullet.CaptainBullet0(self.pos, -self.frame * 5, self.game.enemy_bullets)
        bullet.CaptainBullet0(self.pos, self.frame * 5, self.game.enemy_bullets)

    def update_img(self):
        if self.frame % 200 > 100:
            self.image = pg.transform.flip(GFX['e_captain0'], False, True)
            self.image.blit(self.effect_image, (self.radius - 32, self.radius - 32))
            self.effect_image = next(self.effect_images)
            self.shoot()
        else:
            self.image = pg.transform.flip(GFX['e_captain0'], False, True)

    def update_pos(self):
        self.pos = (self.pos[0] + self.speed * self.direction[0], self.pos[1] + self.speed * self.direction[1])
        self.rect.center = self.pos
        self.hit_box.rect.center = self.pos

    def item(self):
        Bomb(self.game, self.pos)

    def check_death(self):
        if self.rect.top >= 800:
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            self.item()
            self.kill()
            self.hit_box.kill()


class Captain1(Captain0):
    def __init__(self, game, pos):
        super(Captain1, self).__init__(game, pos)
        self.image = pg.transform.flip(GFX['e_captain1'], False, True)

    def shoot(self):
        bullet.CaptainBullet1(self.pos, self.frame, self.game.enemy_bullets)

    def item(self):
        Powerup(self.game, self.pos)

    def update_img(self):
        if self.frame % 200 > 100:
            self.image = pg.transform.flip(GFX['e_captain1'], False, True)
            self.image.blit(self.effect_image, (self.radius - 32, self.radius - 32))
            self.effect_image = next(self.effect_images)
            self.shoot()
        else:
            self.image = pg.transform.flip(GFX['e_captain1'], False, True)


class Major0(Enemy):
    def __init__(self, game, pos):
        super(Major0, self).__init__(game, pos)
        self.health = 800
        self.speed = 1
        self.pos = self.pos
        self.direction = [1, 0]
        self.image = pg.transform.flip(GFX['e_major0'], False, True)
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((80, 50))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.exhaust1 = Exhaust(self, (-20, -55), 3, True)
        self.exhaust2 = Exhaust(self, (+20, -55), 3, True)
        self.frame = 0

    def shoot(self):
        pos0 = (self.pos[0] - 72, self.pos[1] + 22)
        pos1 = (self.pos[0] + 72, self.pos[1] + 22)
        target = self.find_target_pos()
        bullet.MajorBullet1(self.pos, self.game.enemy_bullets)
        bullet.SergeantWeapon1(pos0, target, self.game.enemy_bullets)
        bullet.SergeantWeapon1(pos1, target, self.game.enemy_bullets)

    def update_pos(self):
        self.pos = (self.pos[0] + self.direction[0] * self.speed, self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        self.hit_box.rect.center = self.pos
        if self.rect.left <= 0:
            self.direction = [1, 0]
        elif self.rect.right >= 600:
            self.direction = [-1, 0]

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)

    def check_death(self):
        if self.frame >= 2000:
            Emerge2(self.game, self.pos)
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            for i in range(15):
                Coin(self.game, (self.pos[0] + random.randint(-40, 40), self.pos[1] + random.randint(-25, 25)), None)
            self.kill()
            self.hit_box.kill()

    def check_shoot(self):
        if self.frame % 200 > 100:
            if self.frame % 90 == 1:
                self.shoot()


class Major1(Major0):
    def __init__(self, game, pos):
        super(Major1, self).__init__(game, pos)
        self.image = pg.transform.flip(GFX['e_major1'], False, True)

    def shoot(self):
        pos0 = (self.pos[0] - 72, self.pos[1] + 22)
        pos1 = (self.pos[0] + 72, self.pos[1] + 22)
        target = self.find_target_pos()
        bullet.MajorBullet2(self.pos, self.game.enemy_bullets)
        bullet.SergeantWeapon2(pos0, target, self.game.enemy_bullets)
        bullet.SergeantWeapon2(pos1, target, self.game.enemy_bullets)


class Colonel0(Enemy):
    def __init__(self, game, pos):
        super(Colonel0, self).__init__(game, pos)
        self.health = 800
        self.speed = 1
        self.pos = self.pos
        self.direction = [1, 0]
        self.image = pg.transform.flip(GFX['e_colonel0'], False, True)
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((128, 80))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.exhaust1 = Exhaust(self, (-48, -63), 2, True)
        self.exhaust2 = Exhaust(self, (+48, -63), 2, True)
        self.frame = 0
        self.w = self.image.get_width() / 2.0
        self.h = self.image.get_height() / 2.0
        self.effect_images = cycle([GFX['e_00{}{}'.format((x + 1) // 10, (x + 1) % 10)] for x in range(10)])
        self.effect_image = next(self.effect_images)
        self.shoot_on = False

    def shoot(self):
        if self.frame % 200 == 110:
            bullet.ColonelWeapon1(self.pos, 7, self.game.enemy_bullets)

        elif self.frame % 200 == 120:
            bullet.ColonelWeapon1(self.pos, 6, self.game.enemy_bullets)
        elif self.frame % 200 == 130:
            bullet.ColonelWeapon1(self.pos, 5, self.game.enemy_bullets)
        elif self.frame % 200 == 140:
            bullet.ColonelWeapon1(self.pos, 4, self.game.enemy_bullets)
        elif self.frame % 200 == 150:
            bullet.ColonelWeapon1(self.pos, 3, self.game.enemy_bullets)
        elif self.frame % 200 == 160:
            bullet.ColonelWeapon1(self.pos, 2, self.game.enemy_bullets)
        elif self.frame % 200 == 170:
            bullet.ColonelWeapon1(self.pos, 1, self.game.enemy_bullets)

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)

        if self.shoot_on == True:
            self.image = pg.transform.flip(GFX['e_colonel0'], False, True)
            self.image.blit(self.effect_image, (self.w - 32, self.h - 32))
            self.effect_image = next(self.effect_images)
        elif self.shoot_on == False:
            self.image = pg.transform.flip(GFX['e_colonel0'], False, True)

    def update_pos(self):
        self.pos = (self.pos[0] + self.direction[0] * self.speed, self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        if self.rect.left <= 0:
            self.direction = [1, 0]
        elif self.rect.right >= 600:
            self.direction = [-1, 0]
        self.hit_box.rect.center = self.pos

    def check_shoot(self):
        if self.frame % 200 > 100:
            self.shoot()
            self.shoot_on = True
        else:
            self.shoot_on = False

    def check_death(self):
        if self.frame >= 2000:
            Emerge2(self.game, self.pos)
            self.kill()
            self.hit_box.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            for i in range(20):
                Coin(self.game, (self.pos[0] + random.randint(-60, 60), self.pos[1] + random.randint(-40, 40)), None)
            self.kill()
            self.hit_box.kill()


class Colonel1(Colonel0):
    def __init__(self, game, pos):
        super(Colonel1, self).__init__(game, pos)
        self.image = pg.transform.flip(GFX['e_colonel1'], False, True)

    def shoot(self):
        if self.frame % 200 == 110:
            bullet.ColonelWeapon2(self.pos, 7, self.game.enemy_bullets)

        elif self.frame % 200 == 120:
            bullet.ColonelWeapon2(self.pos, 6, self.game.enemy_bullets)
        elif self.frame % 200 == 130:
            bullet.ColonelWeapon2(self.pos, 5, self.game.enemy_bullets)
        elif self.frame % 200 == 140:
            bullet.ColonelWeapon2(self.pos, 4, self.game.enemy_bullets)
        elif self.frame % 200 == 150:
            bullet.ColonelWeapon2(self.pos, 3, self.game.enemy_bullets)
        elif self.frame % 200 == 160:
            bullet.ColonelWeapon2(self.pos, 2, self.game.enemy_bullets)
        elif self.frame % 200 == 170:
            bullet.ColonelWeapon2(self.pos, 1, self.game.enemy_bullets)

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)

        if self.shoot_on == True:
            self.image = pg.transform.flip(GFX['e_colonel1'], False, True)
            self.image.blit(self.effect_image, (self.w - 32, self.h - 32))
            self.effect_image = next(self.effect_images)
        elif self.shoot_on == False:
            self.image = pg.transform.flip(GFX['e_colonel1'], False, True)


class Boss1(Enemy):
    def __init__(self, game, pos):
        super(Boss1, self).__init__(game, pos)
        self.tag = 'boss'
        self.target = self.find_target_pos()
        self.o_health = 3000
        self.health = 3000
        self.health_ratio = self.health * 1.0 / self.o_health
        self.speed = 0.5
        self.direction = [1, 0]
        self.image = pg.transform.flip(GFX['boss11'], False, True)
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((100, 100))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.exhaust1 = Exhaust(self, (-78, -140), 2, True)
        self.exhaust2 = Exhaust(self, (78, -140), 2, True)
        self.heart = RotateRing(self, 200)

        self.w = self.image.get_width() / 2.0
        self.h = self.image.get_height() / 2.0
        self.effect_images = cycle([GFX['e_00{}{}'.format((x + 1) // 10, (x + 1) % 10)] for x in range(10)])
        self.effect_image = next(self.effect_images)
        self.shoot_on = False
        self.frame = 0

    def shoot(self):
        if self.health_ratio >= 0.5:
            if self.frame % 300 == 1:
                self.speed = 0
                self.shoot_on = False
                Cone(self.game, (self.pos[0], self.pos[1] + 250))
            elif self.frame % 300 >= 200:
                self.shoot_on = False
                self.speed = 0.5
            elif self.frame % 300 >= 100:
                self.speed = 0
                self.shoot_on = True
                bullet.EnemyBullet(self.pos, random.randint(-110, -70), None, 15, random.randint(5, 10),
                                   self.game.enemy_bullets)
        elif self.health_ratio >= 0.2:
            if self.frame % 20 == 1:
                self.shoot_on = True
                self.speed = 0.5
                bullet.Boss1Pattern1(self.pos, self.game.enemy_bullets)
            else:
                self.shoot_on = False
        else:
            self.speed = 0
            bullet.Boss1Pattern2(self.pos, self.frame, self.game.enemy_bullets)

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)
            self.game.explosion_effect.add(self.heart)
        if self.shoot_on == True:
            if self.health_ratio <= 0.2:
                self.image = pg.transform.flip(GFX['boss12'], False, True)
            else:
                self.image = pg.transform.flip(GFX['boss11'], False, True)
            self.image.blit(self.effect_image, (self.w - 32, self.h - 32))
            self.effect_image = next(self.effect_images)
        elif self.shoot_on == False:
            if self.health_ratio <= 0.2:
                self.image = pg.transform.flip(GFX['boss12'], False, True)
            else:
                self.image = pg.transform.flip(GFX['boss11'], False, True)

    def update_pos(self):
        self.pos = (self.pos[0] + self.direction[0] * self.speed, self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        if self.rect.left <= 0:
            self.direction = [1, 0]
        elif self.rect.right >= 600:
            self.direction = [-1, 0]
        self.hit_box.rect.center = self.pos

    def get_bomb_damage(self):
        self.health -= 15

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.hit_box.kill()
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            for i in range(50):
                Coin(self.game, (self.pos[0] + random.randint(-50, 50), self.pos[1] + random.randint(-50, 50)), None)
            EndingExplosion(self.game)
            try:
                self.game.p1_score = self.game.player_1.score
            except:
                pass
            try:
                self.game.p2_score = self.game.player_2.score
            except:
                pass

    def check_shoot(self):
        self.shoot()

    def custom(self):
        self.health_ratio = self.health * 1.0 / self.o_health


class Boss2(Enemy):
    def __init__(self, game, pos):
        super(Boss2, self).__init__(game, pos)
        self.tag = 'boss'
        self.target = self.find_target_pos()
        self.o_health = 6000
        self.health = 6000
        self.health_ratio = self.health * 1.0 / self.o_health
        self.speed = 0.5
        self.direction = [1, 0]
        self.image = pg.transform.flip(GFX['boss21'], False, True)
        self.rect = self.image.get_rect(center=self.pos)
        self.hit_box.image = pg.Surface((120, 120))
        self.hit_box.rect = self.hit_box.image.get_rect(center=self.pos)
        self.hit_box.body = self
        self.exhaust1 = Exhaust(self, (0, -120), 2, True)
        self.exhaust2 = Exhaust(self, (-15, -130), 2, True)
        self.exhaust3 = Exhaust(self, (15, -130), 2, True)
        self.heart = RotateRing(self, 240)

        self.w = self.image.get_width() / 2.0
        self.h = self.image.get_height() / 2.0
        self.effect_images = cycle([GFX['e_00{}{}'.format((x + 1) // 10, (x + 1) % 10)] for x in range(10)])
        self.effect_image = next(self.effect_images)
        self.shoot_on = False
        self.frame = 0

        self.reverse = False

    def shoot(self):
        if self.health_ratio >= 0.6:
            if self.frame % 300 >= 200:
                self.shoot_on = True
                bullet.Boss2B(self.pos, self.frame * 20, 5, self.reverse, self.game.enemy_bullets)
            else:
                self.shoot_on = False
        elif self.health_ratio >= 0.2:
            if self.frame % 300 == 100:
                num = random.randint(1, 2)
                bullet.Boss2Weapon1(self, self.game.enemy_bullets, self.reverse, num)
            elif self.frame % 300 >= 100:
                bullet.Boss2B1(self.pos, self.frame * 20, 5, self.reverse, self.game.enemy_bullets)
            elif self.frame % 300 == 1:
                Radar(self.game, self.pos, self.reverse)
            else:
                self.shoot_on = False

        else:
            self.shoot_on = True
            if self.frame % 10 == 1:
                bullet.Boss2Weapon2(self.pos, self.frame, self.game.enemy_bullets)
            pos1 = (self.pos[0] - 100, self.pos[1] + 45)
            pos2 = (self.pos[0] + 100, self.pos[1] + 45)
            target = self.find_target_pos()
            if self.frame % 20 == 1:
                bullet.SergeantWeapon1(pos1, target, self.game.enemy_bullets)
                bullet.SergeantWeapon1(pos2, target, self.game.enemy_bullets)

    def update_img(self):
        if self.groups():
            self.game.explosion_effect.add(self.exhaust1)
            self.game.explosion_effect.add(self.exhaust2)
            self.game.explosion_effect.add(self.exhaust3)
            self.game.explosion_effect.add(self.heart)
        if self.shoot_on == True:
            if self.health_ratio <= 0.2:
                self.image = pg.transform.flip(GFX['boss23'], False, True)
            elif self.health_ratio <= 0.6:
                self.image = pg.transform.flip(GFX['boss22'], False, True)
            else:
                self.image = pg.transform.flip(GFX['boss21'], False, True)
            self.image.blit(self.effect_image, (self.w - 32, self.h - 32))
            self.effect_image = next(self.effect_images)
        elif self.shoot_on == False:
            if self.health_ratio <= 0.2:
                self.image = pg.transform.flip(GFX['boss23'], False, True)
            elif self.health_ratio <= 0.6:
                self.image = pg.transform.flip(GFX['boss22'], False, True)
            else:
                self.image = pg.transform.flip(GFX['boss21'], False, True)

    def update_pos(self):
        self.pos = (self.pos[0] + self.direction[0] * self.speed, self.pos[1] + self.direction[1] * self.speed)
        self.rect.center = self.pos
        if self.rect.left <= 0:
            self.direction = [1, 0]
        elif self.rect.right >= 600:
            self.direction = [-1, 0]
        self.hit_box.rect.center = self.pos

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.hit_box.kill()
            EnemyExplosion(self.game, self, self.game.explosion_effect)
            for i in range(50):
                Coin(self.game, (self.pos[0] + random.randint(-50, 50), self.pos[1] + random.randint(-50, 50)), None)
            EndingExplosion(self.game)
            try:
                self.game.p1_score = self.game.player_1.score
            except:
                pass
            try:
                self.game.p2_score = self.game.player_2.score
            except:
                pass

    def check_shoot(self):
        self.shoot()

    def custom(self):
        self.health_ratio = self.health * 1.0 / self.o_health
        if self.direction[0] == -1:
            self.reverse = True
        else:
            self.reverse = False



class Boss3(Enemy):
    pass
