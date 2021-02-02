#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@fileName      : main.py
@desc          : 对 coco 标注文件进行简单的检索或简单处理
@dateTime      : 2021/01/22 11:41:51
@author        : 5km
@contact       : 5km@smslit.cn
'''

import typer

from .consts import __description__
from . import count, detail, info, optimize, version


app = typer.Typer(help=__description__)

app.command('list', help='查询数据')(detail.main)
app.command('count', help='统计数据')(count.main)
app.command('version', help="查看当前使用 cocogo 的版本")(version.main)
app.command('info', help='查看文件中的基本信息，可以指定具体内容项')(info.main)
app.command('optimize', help='优化数据，删除没有的图像数据及相关标注信息')(optimize.main)
