#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@fileName      : models.py
@desc          : 定义数据类型
@dateTime      : 2021/01/23 11:12:37
@author        : 5km
@contact       : 5km@smslit.cn
'''

from enum import Enum


class CoCOItem(str, Enum):
    info = 'info'
    type = 'type'
    images = 'images'
    annotations = 'annotations'
    categories = 'categories'
    licenses = 'licenses'
