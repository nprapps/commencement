#!/usr/bin/env python

import json
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = '.quote_images'

SIZE_DEFAULT = 48
SIZE_MIN = 16
SIZE_MAX = 64
SIZE_DELTA = 4
OPTIMAL_LINES = 4

fonts = {}
textwrapper = textwrap.TextWrapper(width=30)

def optimize_text_size(text):
    size = SIZE_DEFAULT

    lines = textwrapper.wrap(text)

    if len(lines) == OPTIMAL_LINES:
        pass
    elif len(lines) < OPTIMAL_LINES:
        while len(lines) < OPTIMAL_LINES:
            if size == SIZE_MAX:
                break 
                
            size += SIZE_DELTA 

            lines = textwrapper.wrap(text)
    else:
        while len(lines) > OPTIMAL_LINES:
            if size == SIZE_MIN:
                break
                
            size -= SIZE_DELTA 

            lines = textwrapper.wrap(text)

    return (lines, size)

def render(speech):
    img = Image.new('RGB', (640, 640), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    lines, size = optimize_text_size(speech['money_quote'])

    y = 0

    for line in lines:
        draw.text((0, y), line, font=fonts[size], fill=(0, 0, 0))

        y += size

    img.save('%s/%s.png' % (OUT_DIR, speech['slug']), 'PNG')

def main():
    for size in xrange(SIZE_MIN, SIZE_MAX + 1, SIZE_DELTA):
        fonts[size] =  ImageFont.truetype('Gotham-Book.otf', size)

    with open('www/static-data/data.json') as f:
        data = json.load(f)

    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    for speech in data[:5]:
        render(speech)

if __name__ == '__main__':
    main()
