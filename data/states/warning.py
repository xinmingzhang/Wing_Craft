import sys
import pygame as pg
from .. import tools
from ..prepare import GFX
from ..components import transition

class Warnings(tools._State):
    def __init__(self):
        super(Warnings, self).__init__()
        self.next = 'TITLE'
        self.timer = 300
        self.frame = 0
        self.bg = GFX['warning']
        self.transition = transition.Transition()


       
    def startup(self, persist):
        pass

    def cleanup(self):
        pass

    def get_event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()


    def update(self, dt):
        self.transition.fade_in()
        self.frame += 1
        if self.frame > 150:
            self.done = self.transition.fade_out()




    def draw(self, surface):
        surface.blit(self.bg,(0,0))
        self.transition.draw(surface)


