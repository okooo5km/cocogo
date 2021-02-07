#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : info.py
@desc          : info 子命令的处理
@dateTime      : 2021/01/23 11:17:19
@author        : 5km
@contact       : 5km@smslit.cn
"""
import json

import typer

from .models import CoCOItem
from .utilities import CoCoCallback


def main(json_file: str = typer.Argument(..., callback=CoCoCallback.check_file, help="指定待检索的 json 文件"),
         item: CoCOItem = typer.Option(None, "--item", "-i", help="检索项")):
    with open(json_file, "r") as fp:
        json_data = json.load(fp=fp)

    def echo_info_of_dict(data: dict):
        for key, value in data.items():
            info_str = "  "
            info_str += typer.style(key + ": ",
                                    fg=typer.colors.BRIGHT_GREEN, bold=True)
            if isinstance(value, list):
                value = "[ ... ]"
            elif isinstance(value, dict):
                value = "{ ... }"
            info_str += typer.style(f"{value}",
                                    fg=typer.colors.BRIGHT_BLACK)
            typer.echo(info_str)

    keys = json_data.keys()
    if item is None:
        info = json_data.get("info")
        if info:
            typer.secho("\n文件基本信息如下: \n", fg=typer.colors.BRIGHT_YELLOW)
            echo_info_of_dict(info)

        typer.secho("\n文件中包含内容项如下：\n", fg=typer.colors.BRIGHT_YELLOW)
        keys_str = ", ".join(keys)
        typer.secho(f"  {keys_str}", fg=typer.colors.BRIGHT_BLUE, bold=True)
    elif item not in keys:
        raise typer.BadParameter("指定项不存在，可以先不指定，查看有哪些包含项！")
    else:
        typer.secho(f"\n指定项 {item} 内容格式如下：\n", fg=typer.colors.BRIGHT_YELLOW)
        item_obj = json_data.get(item)
        if isinstance(item_obj, list):
            if len(item_obj) == 0:
                typer.secho("  空", fg=typer.colors.BRIGHT_RED, bold=True)
                typer.Exit(0)
            else:
                echo_info_of_dict(item_obj[0])
        elif isinstance(item_obj, dict):
            echo_info_of_dict(item_obj)
        else:
            typer.secho(f"  {item_obj}",
                        fg=typer.colors.BRIGHT_BLUE, bold=True)
