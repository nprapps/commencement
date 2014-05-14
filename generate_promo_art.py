#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import os

from PIL import Image, ImageDraw

OUT_DIR = 'www/assets/'

CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 576
SIZE = 64

img = Image.new('RGB', (1024, 576), (17, 17, 17))
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
    last_mug = ''

    with open('www/static-data/data.json') as f:
        data = json.load(f)

    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)



    for speech in data:
        print speech['slug']

        if speech['img'] and speech['name'] != last_mug:
            add_grid_mug(speech['img'], x, y)

            last_mug = speech['name']

            if x < CANVAS_WIDTH:
                x += SIZE
            elif y < CANVAS_HEIGHT:
                x = 0
                y += SIZE
            else:
                continue


    img.save('%spromo_art.png' % OUT_DIR, 'PNG')

if __name__ == '__main__':
    main()
