# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2013 - George Y. Kussumoto <georgeyk.dev@gmail.com>
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
##

import os
import random
import string
import sys
import tempfile
import time

from PIL import Image
from pyocr import pyocr
import requests

from models import SodexoCard, parse_html


def process_image(filename, limit=225):
    # read in colour channels
    img = Image.open(filename)
    # resize to make more clearer
    m = 2
    img = img.resize((int(img.size[0]*m), int(img.size[1]*m))).convert('RGBA')
    pixdata = img.load()

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < limit:
                # make dark color black
                pixdata[x, y] = (0, 0, 0, 255)
            else:
                # make light color white
                pixdata[x, y] = (255, 255, 255, 255)
    # convert image to single channel greyscale
    return img.convert('L')


def validate_captcha(value):
    size = 5
    alpha = string.uppercase + string.digits
    captcha = ''
    for char in value:
        if char in alpha:
            captcha += char
    if len(captcha) == size:
        return captcha
    return u''


def download_captcha(url, session):
    c = session.get(url)
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(c.content)
    f.close()
    return f.name


def saldo_sodexo(card, card_type, cpf):
    session = requests.Session()
    url = 'https://sodexosaldocartao.com.br/saldocartao/consultaSaldo.do?operation=consult'
    captcha_url = 'https://sodexosaldocartao.com.br/saldocartao/jcaptcha.do'
    captcha = download_captcha(captcha_url, session)

    tool = pyocr.get_available_tools()[0]
    value = tool.image_to_string(process_image(captcha))
    os.unlink(captcha)
    validated = validate_captcha(value)

    if validated:
        data = {'service': card_type,
                'cardNumber': card,
                'cpf': cpf,
                'jcaptcha_response': validated,
                'x': '6',
                'y': '9'}
        r = session.post(url, params=data)

        if not 'textRed' in r.content:
            model = parse_html(r.content)
            print model['name']
            print model['company']
            print model['status']
            print model['card']
            print model['balance']
            return True
    return False


# testing ...

def usage(args):
    print 'Usage: %s [vr|va] card-number cpf' % (args[0],)


def main(args):
    card_code, card, cpf = args[1:]
    card_type = False
    if card_code == 'vr':
        card_type = SodexoCard.VR
    elif card_code == 'va':
        card_type = SodexoCard.VA

    if not (card_type and card and cpf):
        usage(args)
        return

    for i in range(50):
        time.sleep(random.random())
        if saldo_sodexo(card, card_type, cpf):
            print i
            break


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage(sys.argv)
    else:
        main(sys.argv)
