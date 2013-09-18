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

from collections import defaultdict

from lxml import html


def parse_html(data):
# optmize this queries
    xpath_name = '/html/body/center/table/tr[3]/td/table/tr/td[3]/div/table/tr[1]/td[2]/var[1]/text()[1]'
    xpath_card = '/html/body/center/table/tr[3]/td/table/tr/td[3]/div/table/tr[1]/td[1]/var/text()'
    xpath_company = '/html/body/center/table/tr[3]/td/table/tr/td[3]/div/table/tr[1]/td[2]/var[2]/text()'
    xpath_balance = '//*[@id="balance"]/var/text()'
    xpath_status = '/html/body/center/table/tr[3]/td/table/tr/td[3]/div/table/tr[3]/td[2]/var/text()'

    e = html.fromstring(data)
    user = defaultdict(str)

    name = e.xpath(xpath_name)[0]
    if name:
        user['name'] = name.strip()

    card = e.xpath(xpath_card)[0]
    if card:
        user['card'] = card.strip()

    company = e.xpath(xpath_company)[0]
    if company:
        user['company'] = company.strip()

    balance = e.xpath(xpath_balance)[0]
    if balance:
        user['balance'] = balance.strip()

    status = e.xpath(xpath_status)[0]
    if status:
        user['status'] = status.strip()

    return user


class SodexoCard(object):
    VR = '5;1;6'
    VA = '5;2;4'
