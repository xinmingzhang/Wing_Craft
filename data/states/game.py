import sys
import json
import pygame as pg
from .. import tools
from ..components import player, background, bullet, hud, loadenemy, explosion, transition
from ..prepare import  MUSIC, SFX, SCORE


class Game(tools._State):
    def __init__(self, level):
        super(Game, self).__init__()
        self.level = level
        self.background = background.Background(self.level)

        self.coins = 0

        self.players = pg.sprite.Group()
        self.player_1_bullets = pg.sprite.Group()
        self.player_2_bullets = pg.sprite.Group()
        self.explosion_effect = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.enemies_hit_box = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()

        self.player_1 = pg.sprite.Sprite()
        self.player_2 = pg.sprite.Sprite()
        self.boss = pg.sprite.Sprite()

        self.p1_score = 0
        self.p2_score = 0



        self.choice = [False, False]

        self.stage_clear = False
        self.show_label_time = 250
        self.show_label_timer = 0

        self.player_1_choose = False
        self.player_2_choose = False
        self.choose_player_1_time = 20
        self.choose_player_2_time = 20
        self.show_continue = False
        self.hud = hud.Hud(self)

    def set_music(self):
        if self.level == 1:
            pg.mixer.music.load(MUSIC['01_-_speedway_0'])
        elif self.level == 2:
            pg.mixer.music.load(MUSIC['02_-_chip_beach_0'])
        elif self.level == 3:
            pg.mixer.music.load(MUSIC['03_-_press_any_key_to_continue_0'])
        elif self.level == 4:
            pg.mixer.music.load(MUSIC['04_-_i_want_more_candy_0'])
        elif self.level == 5:
            pg.mixer.music.load(MUSIC['05_-_rain_island_0'])
        pg.mixer.music.play(-1)

    def startup(self, persist):
        self.frame = 0
        self.done = False


        self.players = pg.sprite.Group()
        self.player_1_bullets = pg.sprite.Group()
        self.player_2_bullets = pg.sprite.Group()
        self.explosion_effect = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.enemies_hit_box = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.player_1 = pg.sprite.Sprite()
        self.player_2 = pg.sprite.Sprite()
        self.boss = pg.sprite.Sprite()




        self.persist = persist
        self.controls = self.persist['controls']
        self.coins = self.persist['coins']
        try:
            self.choice = self.persist['choice']
            if self.choice[0] in (1, 3):
                id = self.choice[0]
                self.player_1 = player.Player(self, (150, 700), id, self.players)
            if self.choice[1] in (2, 4):
                id = self.choice[1]
                self.player_2 = player.Player(self, (450, 700), id, self.players)
        except:
            pass

        try:
            self.player_1 = self.persist['player_1']
            if self.player_1.groups():
                self.player_1.pos = (150, 700)
                self.player_1.rect.center = self.player_1.pos
                self.player_1.hitbox.rect.center = self.player_1.pos
                self.player_1.game = self
                self.players.add(self.player_1)

            self.player_2 = self.persist['player_2']
            if self.player_2.groups():
                self.player_2.pos = (450, 700)
                self.player_1.rect.center = self.player_2.pos
                self.player_1.hitbox.rect.center = self.player_2.pos
                self.player_2.game = self
                self.players.add(self.player_2)
        except:
            pass

        self.player_1.weapon_1 = False
        self.player_1.weapon_2 = False
        self.player_2.weapon_1 = False
        self.player_2.weapon_2 = False
        self.set_music()

        self.show_continue = False
        self.c_time = 10
        self.fade_effect = False
        self.transion = transition.StageTransition(self.level)
        self.event_block = True

        with open(SCORE, 'r') as f:
            self.scoreboard = json.load(f)
        self.highscore = self.scoreboard[0][2]


        self.stage_clear = False
        self.show_label_time = 250
        self.show_label_timer = 0
        self.p1_score = 0
        self.p2_score = 0


    def cleanup(self):
        pg.mixer.music.fadeout(500)
        persist = {}
        persist['coins'] = self.coins
        persist['controls'] = self.controls
        persist['player_1'] = self.player_1
        persist['player_2'] = self.player_2
        return persist

    def get_event(self):
        if self.event_block == True:
            pass
        else:
            self.get_player_event()

    def get_player_event(self):
        key = pg.key.get_pressed()
        if self.player_1.groups():

            if key[self.controls['1p_up']] and key[self.controls['1p_down']]:
                self.player_1.direction[1] = 0
            elif key[self.controls['1p_up']]:
                self.player_1.direction[1] = -1
            elif key[self.controls['1p_down']]:
                self.player_1.direction[1] = 1
            else:
                self.player_1.direction[1] = 0

            if key[self.controls['1p_left']] and key[self.controls['1p_right']]:
                self.player_1.direction[0] = 0
            elif key[self.controls['1p_left']]:
                self.player_1.direction[0] = -1
            elif key[self.controls['1p_right']]:
                self.player_1.direction[0] = 1
            else:
                self.player_1.direction[0] = 0

            if key[self.controls['1p_button_a']]:
                if pg.time.get_ticks() - self.player_1.weapon_time < self.player_1.weapon_toggle_time:
                    self.player_1.weapon_1 = True
                else:
                    self.player_1.weapon_1 = False
                    self.player_1.weapon_2 = True

        if self.player_2.groups():

            if key[self.controls['2p_up']] and key[self.controls['2p_down']]:
                self.player_2.direction[1] = 0
            elif key[self.controls['2p_up']]:
                self.player_2.direction[1] = -1
            elif key[self.controls['2p_down']]:
                self.player_2.direction[1] = 1
            else:
                self.player_2.direction[1] = 0

            if key[self.controls['2p_left']] and key[self.controls['2p_right']]:
                self.player_2.direction[0] = 0
            elif key[self.controls['2p_left']]:
                self.player_2.direction[0] = -1
            elif key[self.controls['2p_right']]:
                self.player_2.direction[0] = 1
            else:
                self.player_2.direction[0] = 0

            if key[self.controls['2p_button_a']]:
                self.player_2.weapon_1 = True
                if pg.time.get_ticks() - self.player_2.weapon_time > self.player_2.weapon_toggle_time:
                    self.player_2.weapon_2 = True
                    self.player_2.weapon_1 = False
                    # else:
                    #     self.player_2.weapon_1 = False
                    #     self.player_2.weapon_2 = True

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key in (self.controls['1p_coin'], self.controls['2p_coin']):
                    SFX['coin'].play()
                    self.coins += 1
                if event.key == self.controls['1p_start']:
                    if self.coins > 0 and not self.player_1.groups():
                        self.coins -= 1
                        self.player_1_choose = True
                        self.show_continue = False
                        self.choice[0] = 1
                if event.key == self.controls['2p_start']:
                    if self.coins > 0 and not self.player_2.groups():
                        self.coins -= 1
                        self.player_2_choose = True
                        self.show_continue = False
                        self.choice[1] = 2
                if event.key in (
                self.controls['1p_up'], self.controls['1p_down'], self.controls['1p_left'], self.controls['1p_right']):
                    if self.player_1_choose == True:
                        self.choice[0] = (self.choice[0] + 2) % 4

                if event.key in (
                self.controls['2p_up'], self.controls['2p_down'], self.controls['2p_left'], self.controls['2p_right']):
                    if self.player_2_choose == True:
                        self.choice[1] = (self.choice[1] + 1) % 4 + 1

                if event.key == self.controls['1p_button_a']:
                    if self.player_1.groups():
                        self.player_1.weapon_time = pg.time.get_ticks()
                    if self.player_1_choose == True:
                        self.player_1 = player.Player(self, (150, 700), self.choice[0], self.players)
                        self.player_1_choose = False
                        self.choose_player_1_time = 20
                if event.key == self.controls['1p_button_b']:
                    if self.player_1.groups():
                        self.player_1.check_bomb()
                    if self.player_1_choose == True:
                        self.player_1 = player.Player(self, (150, 700), self.choice[0], self.players)
                        self.player_1_choose = False
                        self.choose_player_1_time = 20
                if event.key == self.controls['2p_button_a']:
                    if self.player_2.groups():
                        self.player_2.weapon_time = pg.time.get_ticks()
                    if self.player_2_choose == True:
                        self.player_2 = player.Player(self, (450, 700), self.choice[1], self.players)
                        self.player_2_choose = False
                        self.choose_player_2_time = 20
                if event.key == self.controls['2p_button_b']:
                    if self.player_2.groups():
                        self.player_2.check_bomb()
                    if self.player_2_choose == True:
                        self.player_2 = player.Player(self, (450, 700), self.choice[1], self.players)
                        self.player_2_choose = False
                        self.choose_player_2_time = 20


            elif event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == self.controls['1p_button_a']:
                    if self.player_1.groups():
                        self.player_1.weapon_1 = False
                        self.player_1.weapon_2 = False

                if event.key == self.controls['2p_button_a']:
                    if self.player_2.groups():
                        self.player_2.weapon_1 = False
                        self.player_2.weapon_2 = False

    def choose_players(self):
        if self.player_1_choose == True:
            if self.frame % 60 == 1:
                self.choose_player_1_time -= 1
            if self.choose_player_1_time <= 0:
                self.player_1 = player.Player(self, (150, 700), self.choice[0], self.players)
                self.player_1_choose = False
                self.choose_player_1_time = 20
        if self.player_2_choose == True:
            if self.frame % 60 == 1:
                self.choose_player_2_time -= 1
            if self.choose_player_2_time <= 0:
                self.player_2 = player.Player(self, (450, 700), self.choice[1], self.players)
                self.player_2_choose = False
                self.choose_player_2_time = 20

    def player_weapon_update(self, dt):
        if self.player_1.groups() and self.player_1.explosion != True:
            if self.player_1.weapon_1 == True:
                bullet.PlayerWeapon1(self.player_1, self.player_1_bullets)
            elif self.player_1.weapon_2 == True:
                bullet.PlayerLaserBullet(self, self.player_1, self.player_1_bullets)
        else:
            self.player_1_bullets.empty()
        if self.player_2.groups() and self.player_2.explosion != True:
            if self.player_2.weapon_1 == True:
                bullet.PlayerWeapon1(self.player_2, self.player_2_bullets)
            elif self.player_2.weapon_2 == True:
                bullet.PlayerLaserBullet(self, self.player_2, self.player_2_bullets)
        else:
            self.player_2_bullets.empty()
        self.player_1_bullets.update(dt)
        self.player_2_bullets.update(dt)

    def bullet_enemy_check(self):
        if self.player_1.groups():
            p1_bc_dict = pg.sprite.groupcollide(self.player_1_bullets, self.enemies_hit_box, True, False)
            for a in list(p1_bc_dict.keys()):
                self.player_1.get_bullet_score()
                for enemy in p1_bc_dict[a]:
                    enemy.body.get_damage(self.player_1)
                explosion.BulletExplsoion(self, self.player_1.weapon_level, a.pos, self.explosion_effect)
                if self.player_1.weapon_2 == True:
                    for b in self.player_1_bullets:
                        if b.pos[1] <= a.pos[1]:
                            b.kill()
        if self.player_2.groups():
            p2_bc_dict = pg.sprite.groupcollide(self.player_2_bullets, self.enemies_hit_box, True, False)
            for a in list(p2_bc_dict.keys()):
                self.player_2.get_bullet_score()
                for enemy in p2_bc_dict[a]:
                    enemy.body.get_damage(self.player_2)
                explosion.BulletExplsoion(self, self.player_2.weapon_level, a.pos, self.explosion_effect)
                if self.player_2.weapon_2 == True:
                    for b in self.player_2_bullets:
                        if b.pos[1] <= a.pos[1]:
                            b.kill()

    def item_player_check(self):
        if self.player_1.groups():
            p1_it_dict = pg.sprite.spritecollide(self.player_1, self.items, True)
            for item in p1_it_dict:
                self.player_1.item_collide(item)
        if self.player_2.groups():
            p2_it_dict = pg.sprite.spritecollide(self.player_2, self.items, True)
            for item in p2_it_dict:
                self.player_2.item_collide(item)

    def bullet_player_check(self):
        if self.player_1.groups():
            if pg.sprite.spritecollideany(self.player_1.hitbox, self.enemies_hit_box) or pg.sprite.spritecollideany(
                    self.player_1.hitbox, self.enemy_bullets, collided=pg.sprite.collide_circle):
                if self.player_1.invincible == False:
                    self.player_1.explosion = True
        if self.player_2.groups():
            if pg.sprite.spritecollideany(self.player_2.hitbox, self.enemies_hit_box) or pg.sprite.spritecollideany(
                    self.player_2.hitbox, self.enemy_bullets, collided=pg.sprite.collide_circle):
                if self.player_2.invincible == False:
                    self.player_2.explosion = True

    def collosion_check(self):
        self.bullet_enemy_check()
        self.item_player_check()
        self.bullet_player_check()

    def bomb_effect_check(self):
        if self.player_1.groups():
            if self.player_1.bomb_on:
                self.player_1.bomb_effect()
        if self.player_2.groups():
            if self.player_2.bomb_on:
                self.player_2.bomb_effect()

    def check_continue(self, dt):
        if (self.player_1_choose == False and self.player_2_choose == False) and (
            not self.player_1.groups() and not self.player_2.groups()):
            self.show_continue = True
            self.c_time -= dt / 1000.0
            if self.c_time <= 0:
                self.done = True
                self.next = 'LEVEL6'
        else:
            self.show_continue = False
            self.c_time = 10

    def stage_clear_effect(self):
        if self.player_1_choose == True:
            self.player_1 = player.Player(self, (150, 700), self.choice[0], self.players)
            self.player_1_choose = False
            self.choose_player_1_time = 20
        if self.player_2_choose == True:
            self.player_2 = player.Player(self, (450, 700), self.choice[1], self.players)
            self.player_2_choose = False
            self.choose_player_2_time = 20
        pg.mixer.music.fadeout(500)
        self.player_1_bullets.empty()
        if self.player_1.groups():
            self.player_1.pos = (150,700)
            self.player_1.rect.center = self.player_1.pos
            self.player_1.hitbox.center = self.player_1.pos
            self.player_1.direction = [0, 0]
        if self.player_2.groups():
            self.player_2.pos = (450,700)
            self.player_2.rect.center = self.player_2.pos
            self.player_2.hitbox.center = self.player_2.pos
            self.player_2.direction = [0, 0]
        self.player_2_bullets.empty()
        self.event_block = True
        self.show_label_timer += 1
        if self.show_label_timer >= self.show_label_time:
            self.done = True
            self.next = 'LEVEL{}'.format(self.level + 1)

    def update(self, dt):
        self.transion.fade_in()
        if self.frame == 201:
            self.event_block = False
        self.check_continue(dt)
        if not self.show_continue:
            if self.stage_clear == True:
                self.stage_clear_effect()
            self.frame += 1
            enemy = loadenemy.get_enemies_from_map(self, self.frame, self.level)
            if enemy is not None:
                if enemy.tag == 'enemy':
                    self.enemies.add(enemy)
                    self.enemies_hit_box.add(enemy.hit_box)
                elif enemy.tag == 'boss':
                    self.enemies.add(enemy)
                    self.enemies_hit_box.add(enemy.hit_box)
                    self.boss = enemy
                elif enemy.tag == 'effect':
                    self.explosion_effect.add(enemy)
            self.choose_players()
            self.background.update()
            self.player_weapon_update(dt)
            self.explosion_effect.update()
            self.items.update()
            self.players.update(dt)
            self.enemies.update()
            self.enemies_hit_box.update(dt)
            self.enemy_bullets.update()
            self.bomb_effect_check()
            self.collosion_check()


        elif self.show_continue:
            pass
        self.hud.update()



    def draw(self, surface):
        self.background.draw(surface)
        self.enemies.draw(surface)
        self.items.draw(surface)
        self.player_1_bullets.draw(surface)
        self.player_2_bullets.draw(surface)
        self.explosion_effect.draw(surface)
        self.players.draw(surface)
        self.enemy_bullets.draw(surface)
        self.hud.draw(surface)
        self.transion.draw(surface)
