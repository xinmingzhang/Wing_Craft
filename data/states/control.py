import json
import pygame as pg
from .. import tools
from ..prepare import CTRL, GFX, FONT1,FONT3
from ..components.labels import Label
from ..components import transition


class Control(tools._State):
    def __init__(self):
        super(Control, self).__init__()
        self.bg = GFX['controls']
        self.transition = transition.Transition()
        self.next = 'TITLE'
        self.fade_effect = False

    def make_labels(self):
        self.labels = pg.sprite.Group()
        self.labellist = []
        self.label_centers = [(150 + x * 300, 360 + y * 50) for x in range(2) for y in range(8)]
        self.texts = ['1p_coin', '1p_start', '1p_up', '1p_down', '1p_left', '1p_right', '1p_button_a', '1p_button_b',
                      '2p_coin', '2p_start', '2p_up', '2p_down', '2p_left', '2p_right', '2p_button_a', '2p_button_b']
        for name, center in zip(self.texts, self.label_centers):
            self.labellist.append(
                Label(pg.key.name(self.controls[name]), {'center': center}, self.labels, font_path=FONT1,
                      font_size=25))

        self.hint_1 = Label('Esc to return',{'center':(300,750)},self.labels,font_path = FONT3,font_size = 25)

        self.hints =['Arrow Keys To Navigate / Enter To Unlock',
                     'Assign Your Own Key / Enter To Confirm']

        self.hint_2 = Label(self.hints[0],{'center':(300,780)},self.labels,font_path = FONT3,font_size = 25)


    def startup(self, persist):
        self.persist = persist
        self.change_label = False
        self.done = False
        self.controls = self.persist['controls']
        self.make_labels()
        self.choose = 0
        self.change_label = False
        self.transition = transition.Transition()
        self.fade_effect = False

    def cleanup(self):
        persist = {}
        persist['controls'] = self.controls
        persist['coins'] = self.persist['coins']
        return persist

    def set_new_key(self, key):
        select_label = self.labellist[self.choose]
        name = pg.key.name(key)
        select_label.text = name
        select_label.original_text = name
        self.controls[self.texts[self.choose]] = key

    def get_event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    with open(CTRL,'w') as f:
                        json.dump(self.controls,f)
                    self.fade_effect = True

                if not self.change_label:
                    if event.key == pg.K_RETURN:
                        self.change_label = True
                    if event.key == pg.K_UP:
                        self.choose = (self.choose - 1) % len(self.texts)
                    if event.key == pg.K_DOWN:
                        self.choose = (self.choose + 1) % len(self.texts)
                    if event.key == pg.K_LEFT:
                        self.choose = (self.choose - 8) % len(self.texts)
                    if event.key == pg.K_RIGHT:
                        self.choose = (self.choose + 8) % len(self.texts)
                elif self.change_label:
                    if event.key == pg.K_RETURN:
                        self.change_label = False
                    elif event.key == pg.K_ESCAPE:
                        pass
                    else:
                        self.set_new_key(event.key)

    def labels_update(self, dt):
        for label in self.labellist:
            if self.labellist.index(label) == self.choose:
                select_label = self.labellist[self.choose]
                if self.change_label == True:
                    select_label.fill_color = (255, 255, 0)
                    select_label.text_color = (0, 0, 0)
                    select_label.blink(dt)
                elif self.change_label == False:
                    select_label.fill_color = (0, 255, 0)
                    select_label.text_color = (255, 255, 255)
                    select_label.unblink()
            else:
                label.fill_color = None
            label.update_text()
        if self.change_label == True:
            self.hint_2.set_text(self.hints[1])
        elif self.change_label == False:
            self.hint_2.set_text(self.hints[0])


    def update(self, dt):
        self.transition.fade_in()
        self.labels_update(dt)
        if self.fade_effect == True:
            self.done = self.transition.fade_out()

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.labels.draw(surface)
        self.transition.draw(surface)
