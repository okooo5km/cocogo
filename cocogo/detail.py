#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@fileName      : detail.py
@desc          : 
@dateTime      : 2021/01/23 11:32:19
@author        : 5km
@contact       : 5km@smslit.cn
'''
import json

import typer

from .models import CoCOItem
from .utilities import CoCoCallback


def main(json_file: str = typer.Argument(..., callback=CoCoCallback.check_file, help='指定待检索的 json 文件'),
         item: CoCOItem = typer.Option(
        CoCOItem.images, '--item', '-i', show_choices=True, help='检索项'),
        start_index: int = typer.Option(
        0, '--start', '-s', help='列出数据的起始位置'),
        end_index: int = typer.Option(10, '--end', '-e', help='列出数据的结束位置')):

    typer.secho('\n加载 json 文件数据中...', fg=typer.colors.BRIGHT_BLACK)
    with open(json_file, 'r') as fp:
        json_data = json.load(fp)

    keys = json_data.keys()

    typer.echo()

    if item in keys:
        item_obj = json_data.get(item)
        if isinstance(item_obj, list):
            end_index = min(len(item_obj), end_index)
            for list_item in item_obj[start_index: end_index]:
                typer.secho(f'  {list_item}', fg=typer.colors.BRIGHT_YELLOW)
            echo_str = typer.style('\n共列出 ', fg=typer.colors.BRIGHT_BLUE)
            echo_str += typer.style(f'{end_index - start_index}',
                                    bold=True, fg=typer.colors.BRIGHT_GREEN)
            echo_str += typer.style(f'({start_index}~{end_index}) 条记录!',
                                    fg=typer.colors.BRIGHT_BLUE)
            typer.echo(echo_str)
        elif isinstance(item_obj, dict):
            for key, value in enumerate(item_obj):
                echo_str = typer.style(
                    f'{key}', fg=typer.colors.BRIGHT_BLUE, bold=True)
                echo_str += typer.style(': ', fg=typer.colors.BRIGHT_BLACK)
                echo_str += typer.style(f'{value}',
                                        fg=typer.colors.BRIGHT_GREEN, bold=True)
                typer.echo(echo_str)
            typer.secho('共列出 1 条记录!', fg=typer.colors.BRIGHT_BLUE)
        else:
            typer.secho(item_obj, fg=typer.colors.BRIGHT_YELLOW)
    else:
        typer.secho('没有数据', fg=typer.colors.BRIGHT_RED)
