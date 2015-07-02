#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import os
import random

from PIL import Image, ImageDraw

OUT_DIR = 'www/assets/'

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 480
SIZE = 160

img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), (17, 17, 17))
draw = ImageDraw.Draw(img)

def add_grid_mug(mug_src, x, y):

    if mug_src != '' and os.path.exists('www/assets/mugs/%s' % mug_src):
        mug = Image.open('www/assets/mugs/%s' % mug_src)
        mug = mug.resize((SIZE,SIZE),1)
        mug_xy = (x,y)

        img.paste(mug, mug_xy)

def main():
    x = 0
    y = 0

    mugs = [
        'david_carr.jpg',
        'diana_nyad.jpg',
        'kanye.jpg',
        'janetyellen.jpg',
        'maya_rudolph.jpg',
        'mindy_kaling.jpg',
        'scorsese.jpg',
        'terry_gross.jpg',
        'zadie_smith.jpg',
        'john_legend.jpg',
        'john_kerry.jpg',
        'victor_hwang.jpg',
        'neil-degrasse-tyson.jpg',
        'michelle-obama.jpg',
        'dalai-lama.jpg',
    ]

    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    for mug in mugs:
        print mug

        add_grid_mug(mug, x, y)

        if x < CANVAS_WIDTH - SIZE:
            x += SIZE
        elif y < CANVAS_HEIGHT - SIZE:
            x = 0
            y += SIZE
        else:
            continue

    img.save('%spromo_art.png' % OUT_DIR, 'PNG')

if __name__ == '__main__':
    main()
