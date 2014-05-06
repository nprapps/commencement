#!/usr/bin/env python

import json
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = '.quote_images'

MAX_WIDTH = 640
MAX_HEIGHT = 640

SIZE_MIN = 16
SIZE_MAX = 64
SIZE_DELTA = 4

LINE_MIN = 15
LINE_MAX = 40
LINE_DELTA = 5
LINE_OPTIMAL = (20, 25)

fonts = {}

# VARIABLES
# font size
# line char length

def compute_size(lines, fontsize):
    font = fonts[fontsize]
    width = 0
    height = 0

    for line in lines:
        x, y = font.getsize(line)

        width = max((width, x))
        height += y
    
    return width, height

def optimize_text(text):
    permutations = {}
    
    for size in fonts.keys():
        for wrap_count in xrange(LINE_MIN, LINE_MAX + 1, LINE_DELTA):
            lines = textwrap.wrap(text, wrap_count)
            width, height = compute_size(lines, size)

            # Throw away any that exceed canvas space
            if width > MAX_WIDTH:
                continue

            if height > MAX_HEIGHT:
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

    text = speech['money_quote']
    size, wrap_count = optimize_text(text)
    lines = textwrap.wrap(text, wrap_count)

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
