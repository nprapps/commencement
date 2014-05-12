#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import os
import textwrap
import HTMLParser

from typogrify.filters import smartypants

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = 'www/quote-images'

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 640
TEXT_MARGIN = (40, 40, 200, 40)
TEXT_MAX_WIDTH = CANVAS_WIDTH - (TEXT_MARGIN[1] + TEXT_MARGIN[3])

SIZE_MIN = 16
SIZE_MAX = 64
SIZE_DELTA = 4

LINE_MIN = 16
LINE_MAX = 50
LINE_DELTA = 2 

LOGO = Image.open('www/assets/npr-white.png')

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

def optimize_text(text, max_height):
    permutations = {}
    
    for size in fonts['bold'].keys():
        for wrap_count in xrange(LINE_MIN, LINE_MAX + 1, LINE_DELTA):
            lines = textwrap.wrap(text, wrap_count)
            width, height = compute_size(lines, size)

            # Throw away any that exceed canvas space
            if width > TEXT_MAX_WIDTH - quote_width[size]:
                continue

            if height > max_height:
                continue

            permutations[(size, wrap_count)] = (width, height)

    optimal = (0, 0)

    # Find the largest font size that's in the butter zone
    for k, v in permutations.items():
        size, wrap_count = k
        width, height = v

        if size > optimal[0]:
            optimal = k
        elif size == optimal[0] and wrap_count > optimal[1]:
            optimal = k

    return optimal

def render(quote, name, slug, mug_src):
    img = Image.new('RGB', (640, 640), (17, 17, 17))
    draw = ImageDraw.Draw(img)
    text_margin = TEXT_MARGIN

    parse = HTMLParser.HTMLParser()

    text = u'“%s”' % quote
    text = parse.unescape(text)

    if mug_src != '' and os.path.exists('www/assets/mugs/%s' % mug_src):
        text_margin = (230, 40, 200, 40)

        mask =  Image.open('www/assets/mug-mask.png')
        mask = mask.resize((150,150),1)

        mug = Image.open('www/assets/mugs/%s' % mug_src)
        mug = mug.resize((150,150),1)
        mug_xy = (
            (CANVAS_WIDTH / 2) - mug.size[0] / 2,
            40
        )

        img.paste(mug, mug_xy, mask)

    max_height = CANVAS_WIDTH - (text_margin[0] + text_margin[2]) 
    size, wrap_count = optimize_text(text, max_height)
    font = fonts['bold'][size]
    lines = textwrap.wrap(text, wrap_count)

    y = text_margin[0]

    for i, line in enumerate(lines):
        x = text_margin[1]

        if i > 0:
            x += quote_width[size]

        draw.text((x, y), line, font=fonts['bold'][size], fill=(255, 255, 255))

        y += size

    y += size 

    text = u'— %s' % name 
    size = min(size, 32)
    font = fonts['book'][size]
    width, height = font.getsize(text)
    x = (CANVAS_WIDTH - text_margin[1]) - width

    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    logo_xy = (
        (CANVAS_WIDTH - 40) - LOGO.size[0],
        (CANVAS_HEIGHT - 40) - LOGO.size[1]
    )

    img.paste(LOGO, logo_xy)

    img.save('%s/%s.png' % (OUT_DIR, slug), 'PNG')

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

        if speech['money_quote']:
            render(speech['money_quote'], speech['name'], speech['slug'], speech['img'])

        if speech['money_quote2']:
            slug = '%s-2' % speech['slug']

            print slug
            render(speech['money_quote2'], speech['name'], '%s-2' % slug, speech['img'])

if __name__ == '__main__':
    main()
