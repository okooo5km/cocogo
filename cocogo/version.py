#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : version.py
@desc          : 打印版本信息
@dateTime      : 2021/02/02 13:11:57
@author        : 5km
@contact       : 5km@smslit.cn
"""

import typer


from .consts import __version__


def main():
    typer.echo()
    typer.secho(f"  v{__version__}", fg=typer.colors.BRIGHT_YELLOW, bold=True)
