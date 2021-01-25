#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@fileName      : count.py
@desc          : count 子命令处理
@dateTime      : 2021/01/23 11:28:53
@author        : 5km
@contact       : 5km@smslit.cn
'''

import json

import typer

from .models import CoCOItem
from .utilities import CoCoCallback, classify_with_aspect_ratio


def main(json_file: str = typer.Argument(..., callback=CoCoCallback.check_file, help='指定待检索的 json 文件'),
         item: CoCOItem = typer.Option(CoCOItem.images, '--item', '-i', show_choices=True, help='检索项')):

    def echo_item_count(item: CoCOItem, num):
        echo_str = typer.style('\n检索到数据项 ', fg=typer.colors.BRIGHT_YELLOW)
        echo_str += typer.style(f'{item.value} ',
                                fg=typer.colors.BRIGHT_BLUE, bold=True)
        echo_str += typer.style(f'{num}',
                                fg=typer.colors.BRIGHT_GREEN, bold=True)
        echo_str += typer.style(' 条记录!', fg=typer.colors.BRIGHT_YELLOW)
        typer.echo(echo_str)

    typer.secho('\n加载 json 文件数据中...', fg=typer.colors.BRIGHT_BLACK)
    with open(json_file, 'r') as fp:
        json_data = json.load(fp)

    keys = json_data.keys()

    if item in keys:
        item_obj = json_data.get(item)
        if isinstance(item_obj, list):
            echo_item_count(item, len(item_obj))
            if item == 'images':
                classified_result = classify_with_aspect_ratio(images=item_obj)
                typer.secho('\n图像不同宽高比数量统计如下:', fg=typer.colors.BRIGHT_YELLOW)
                for ratio_str, value in classified_result.items():
                    echo_str = typer.style(
                        f'  宽高比 {ratio_str}: ', fg=typer.colors.BRIGHT_BLUE)
                    echo_str += typer.style(f'{value}',
                                            fg=typer.colors.BRIGHT_GREEN, bold=True)
                    echo_str += typer.style(' 张', fg=typer.colors.BRIGHT_BLACK)
                    typer.echo(echo_str)
        else:
            echo_item_count(item, 1)

    else:
        echo_item_count(item, 0)
