#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@fileName      : utilities.py
@desc          : 
@dateTime      : 2021/01/23 11:09:02
@author        : 5km
@contact       : 5km@smslit.cn
'''
import os
from typing import List, Any, Dict

import typer

from .consts import __description__, __version__


def classify_with_aspect_ratio(images: List[Dict[str, Any]]) -> Dict[str, int]:
    '''按照宽高比对图像进行分类

    Args:
        images (List[Dict[str, Any]]): [description]

    Returns:
        Dict[str, int]: [description]
    '''
    result: Dict[str, List[int]] = {}
    for image in images:
        width = image.get('width')
        height = image.get('height')
        aspect_ratio_str = f'{round(width / height, 2)}-({width}, {height})'
        if aspect_ratio_str in result:
            result[aspect_ratio_str] += 1
        else:
            result[aspect_ratio_str] = 0
    return result


class CoCoCallback:

    @staticmethod
    def check_file(value: str):
        '''检查文件路径
        '''
        if not os.path.exists(value):
            raise typer.BadParameter('文件不存在!')
        if os.path.isdir(value) or (not value.endswith('.json')):
            raise typer.BadParameter('请指定有效的 coco json 文件!')
        return value

    @staticmethod
    def check_img_dir(value: str):
        if not os.path.exists(value):
            raise typer.BadParameter('图像路径不存在!')
        if os.path.isfile(value):
            raise typer.BadParameter('请指定有效的图像路径!')
        return os.path.abspath(value)

    @staticmethod
    def version_echo(value: bool):
        if value:
            typer.secho(f'\n{__description__}\n',
                        fg=typer.colors.BRIGHT_GREEN)
            echo_version_str = typer.style(
                '版本号: ', fg=typer.colors.BRIGHT_BLACK, bold=True)
            echo_version_str += typer.style(
                f' v{__version__} ', fg=typer.colors.YELLOW, bold=True)
            typer.echo(echo_version_str + '\n')
            raise typer.Exit()
