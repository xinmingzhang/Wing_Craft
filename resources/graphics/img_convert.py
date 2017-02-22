import os
import pygame as pg

for i in os.listdir('.'):
    try:
        img = pg.image.load(i)
        pg.image.save(img,i)
    except:
        print(i + 'failed')
print('done')
