#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : utilities.py
@desc          : 
@dateTime      : 2021/01/23 11:09:02
@author        : 5km
@contact       : 5km@smslit.cn
"""
import os
from typing import List, Any, Dict

import typer

from .consts import __description__, __version__


def classify_with_aspect_ratio(images: List[Dict[str, Any]]) -> Dict[str, int]:
    """按照宽高比对图像进行分类

    Args:
        images (List[Dict[str, Any]]): 标注文件中图像数据

    Returns:
        Dict[str, int]: 统计后的图像数据
    """
    result: Dict[str, List[int]] = {}
    for image in images:
        width = image.get("width")
        height = image.get("height")
        aspect_ratio_str = f"{round(width / height, 2)}-({width}, {height})"
        if aspect_ratio_str in result:
            result[aspect_ratio_str] += 1
        else:
            result[aspect_ratio_str] = 1
    return result


def init_scatter_data(step: float = 0.02) -> Dict[str, Dict[str, Any]]:
    """ bbox 散点图数据初始化（归一化）
    """
    if step > 0.5:
        step = 0.02
    scatter_dict: Dict[str, Dict[str, Any]] = {}
    nums = [i / 100.0 for i in range(0, 100, int(step*100.0))]
    for i in nums:
        for j in nums:
            scatter_dict[f"{i:.2f}-{j:.2f}"] = {
                "x": i,
                "y": j,
                "annotations": []
            }
    return scatter_dict


def build_idx_table(items: List[Dict[str, Any]],
                    table_name: str = "images") -> Dict[int, Dict[str, int]]:
    """重建数据索引表

    Args:
        items (List[Dict[str, Any]]): 待建立索引的数据
        table_name str: 索引表标记名称

    Returns:
        Dict[int, Dict[str, int]]: 索引表
    """
    idx_dict: Dict[int, Dict[str, int]] = {}
    typer.secho(f"\n建立 {table_name} 索引...", fg=typer.colors.BRIGHT_BLACK)
    for item in items:
        item["data"] = []
        idx_dict[item.get("id")] = item
    typer.secho("完成!", fg=typer.colors.BRIGHT_BLACK)

    return idx_dict


class CoCoCallback:

    @staticmethod
    def check_file(value: str):
        """检查文件路径
        """
        if not os.path.exists(value):
            raise typer.BadParameter("文件不存在!")
        if os.path.isdir(value) or (not value.endswith(".json")):
            raise typer.BadParameter("请指定有效的 coco json 文件!")
        return value

    @staticmethod
    def check_img_dir(value: str):
        if not os.path.exists(value):
            raise typer.BadParameter("图像路径不存在!")
        if os.path.isfile(value):
            raise typer.BadParameter("请指定有效的图像路径!")
        return os.path.abspath(value)

    @staticmethod
    def version_echo(value: bool):
        if value:
            typer.secho(f"\n{__description__}\n",
                        fg=typer.colors.BRIGHT_GREEN)
            echo_version_str = typer.style("版本号: ",
                                           fg=typer.colors.BRIGHT_BLACK,
                                           bold=True)
            echo_version_str += typer.style(
                f" v{__version__} ", fg=typer.colors.YELLOW, bold=True)
            typer.echo(echo_version_str + "\n")
            raise typer.Exit()
