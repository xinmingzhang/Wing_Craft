import sys
import json
import pygame as pg
from .. import tools
from ..prepare import SCORE
from ..components import transition


class GameOver(tools._State):
    def __init__(self):
        super(GameOver, self).__init__()
        self.bg = pg.Surface((600,800))
        self.bg.fill((0,0,0))

    def startup(self, persist):
        self.transition = transition.StageTransition(6)
        self.persist = persist
        self.player_1 = self.persist['player_1']
        self.player_2 = self.persist['player_2']
        try:
            self.player_1_score = self.persist['player_1'].score
        except:
            self.player_1_score = 0
        try:
            self.player_2_score = self.persist['player_2'].score
        except:
            self.player_2_score = 0

        with open(SCORE, 'r') as f:
            self.scoreboard = json.load(f)
        self.done = False
        self.highscore = self.scoreboard[0][2]
        self.passing_score = self.scoreboard[4][2]
        self.frame = 0

    def check_score(self):
        if self.player_1_score > self.passing_score:
            self.scoreboard.append(['player_1',self.player_1.id,self.player_1.score])
            self.scoreboard = sorted(self.scoreboard, key=lambda c: c[2], reverse=True)[:5]


        if self.player_2_score > self.passing_score:
            self.scoreboard.append(['player_2', self.player_2.id, self.player_2.score])
            self.scoreboard = sorted(self.scoreboard, key=lambda c: c[2], reverse=True)[:5]


    def cleanup(self):
        persist = {}
        persist['coins'] = self.persist['coins']
        persist['controls'] = self.persist['controls']
        if self.next == 'TITLE':
            return persist
        elif self.next == 'NAME':
            persist['scoreboard'] = self.scoreboard
            return persist


    def get_event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self, dt):
        self.transition.fade_in()
        self.frame += 1
        if self.frame == 150:
            self.done = True
            if self.player_1_score > self.passing_score or self.player_2_score > self.passing_score:
                self.check_score()
                self.next = 'NAME'
            else:
                self.next = 'TITLE'

    def draw(self, surface):
        surface.blit(self.bg,(0,0))
        self.transition.draw(surface)