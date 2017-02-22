from __future__ import division
import os
import random
import pygame as pg

os.environ['SDL_VIDEO_CENTERED'] = '1'

W = 600
H = 800

class Smile(object):
    def __init__(self):
        pg.init()
        self.sound = pg.mixer.Sound('./resources/sound/laughter.ogg')
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.i = 2
        self.time = 0
        self.timer = self.sound.get_length()+0.5
        
    def run(self):
        

        channel = self.sound.play()
        while not self.done:
            dt = self.clock.tick(self.fps)/1000.0
            self.time += dt

            if self.i < H:
                self.i += 4
            elif self.i >= H:
                self.i = H

            a = self.i / H * 1.0

            p1 = (int(W/2.0 - W/8*2.5*a),int(H/2.0*a))
            p2 = (int(W/2.0 - W/8*2*a),int((H/2.0 - W/8.0)*a))
            p3 = (int(W/2.0 - W/8*1.5*a),int(H/2.0*a))
            p4 = (int(W/2.0 - W/8*0.5*a),int(H/2.0*a))
            p5 = (int(W/2.0) ,int((H/2.0 + W/8.0)*a))
            p6 = (int(W/2.0 + W/8*0.5*a),int(H/2.0*a))
            p7 = (int(W/2.0 + W/8*1.5*a),int(H/2.0*a))
            p8 = (int(W/2.0 + W/8*2*a),int((H/2.0 - W/8.0)*a))
            p9 = (int(W/2.0 + W/8*2.5*a),int(H/2.0*a))
            screen = pg.display.set_mode((W,self.i),pg.NOFRAME)
            channel.set_volume(self.i /800.0 , 1-self.i /800.0 )
            screen.fill((0,0,0))
            if self.i < H:
                rr = random.randint
                pg.draw.lines(screen,(rr(0,255),rr(0,255),rr(0,255)),False,[p1,p2,p3], int(20 * a))
                pg.draw.lines(screen,(rr(0,255),rr(0,255),rr(0,255)),False,[p4,p5,p6], int(20 * a))
                pg.draw.lines(screen,(rr(0,255),rr(0,255),rr(0,255)),False,[p7,p8,p9], int(20 * a))
            if self.i == H:
                pg.draw.lines(screen,(255,255,255),False,[p1,p2,p3], int(20 * a))
                pg.draw.lines(screen,(255,255,255),False,[p4,p5,p6], int(20 * a))
                pg.draw.lines(screen,(255,255,255),False,[p7,p8,p9], int(20 * a))                
            pg.display.update()

            if self.time >= self.timer:
                screen = pg.display.set_mode((W,H))
                for i in range(10,H,2):
                    pg.draw.circle(screen,(255,255,255),(W//2,H//2),i)
                    pg.display.update()
                self.done = True
        pg.quit()
        
        

