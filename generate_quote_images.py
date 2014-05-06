#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = '.quote_images'

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 640
TEXT_MARGIN = (40, 40, 200, 40)
TEXT_MAX_WIDTH = CANVAS_WIDTH - (TEXT_MARGIN[1] + TEXT_MARGIN[3])
TEXT_MAX_HEIGHT = CANVAS_WIDTH - (TEXT_MARGIN[0] + TEXT_MARGIN[2])

SIZE_MIN = 16
SIZE_MAX = 64
SIZE_DELTA = 4

LINE_MIN = 15
LINE_MAX = 40
LINE_DELTA = 5
LINE_OPTIMAL = (30, 35)

LOGO = Image.open('www/assets/npr-home.png')

fonts = {}
fonts['book'] = {}
fonts['bold'] = {}

quote_width = {}

def compute_size(lines, fontsize):
    font = fonts['bold'][fontsize]
    width = 0
    height = 0

    for line in lines:
        x, y = font.getsize(line)

        width = max((width, x))
        height += y
    
    return width, height

def optimize_text(text):
    permutations = {}
    
    for size in fonts['bold'].keys():
        for wrap_count in xrange(LINE_MIN, LINE_MAX + 1, LINE_DELTA):
            lines = textwrap.wrap(text, wrap_count)
            width, height = compute_size(lines, size)

            # Throw away any that exceed canvas space
            if width > TEXT_MAX_WIDTH - quote_width[size]:
                continue

            if height > TEXT_MAX_HEIGHT:
                continue

            permutations[(size, wrap_count)] = (width, height)

    optimal = (0, 0)
    sub_optimal = (0, 0)

    # Find the largest font size that's in the butter zone
    for k, v in permutations.items():
        size, wrap_count = k
        width, height = v

        if wrap_count in LINE_OPTIMAL:
            if size > optimal[0]:
                optimal = k
        else:
            if size > sub_optimal[0]:
                sub_optimal = k

    if not optimal:
        return sub_optimal

    return optimal

def render(speech):
    img = Image.new('RGB', (640, 640), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    text = u'“%s”' % speech['money_quote']
    size, wrap_count = optimize_text(text)
    font = fonts['bold'][size]    
    quote_size = font.getsize(text[0])
    lines = textwrap.wrap(text, wrap_count)

    y = TEXT_MARGIN[0]

    for i, line in enumerate(lines):
        x = TEXT_MARGIN[1]
    
        if i > 0:
            x += quote_width[size]

        draw.text((x, y), line, font=fonts['bold'][size], fill=(0, 0, 0))

        y += size

    y += size 

    text = u'— %s' % speech['name']
    size = min(size, 32)
    font = fonts['book'][size]
    width, height = font.getsize(text)
    x = (CANVAS_WIDTH - TEXT_MARGIN[1]) - width

    draw.text((x, y), text, font=font, fill=(0, 0, 0))

    logo_xy = (
        (CANVAS_WIDTH - 40) - LOGO.size[0],
        (CANVAS_HEIGHT - 40) - LOGO.size[1]
    )

    img.paste(LOGO, logo_xy)

    img.save('%s/%s.png' % (OUT_DIR, speech['slug']), 'PNG')

def main():
    for size in xrange(SIZE_MIN, SIZE_MAX + 1, SIZE_DELTA):
        fonts['book'][size] =  ImageFont.truetype('www/assets/Gotham-Book.otf', size)
        fonts['bold'][size] =  ImageFont.truetype('www/assets/Gotham-Bold.otf', size)
        quote_width[size] = fonts['bold'][size].getsize(u'“')[0]

    with open('www/static-data/data.json') as f:
        data = json.load(f)

    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    for speech in data:
        print speech['slug']
        render(speech)

if __name__ == '__main__':
    main()
