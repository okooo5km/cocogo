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
import matplotlib
from typing import List, Any, Dict

import typer
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
from .consts import __description__, __version__

matplotlib.use("Agg")


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
            result[aspect_ratio_str]["count"] += 1
        else:
            result[aspect_ratio_str] = {
                "count": 1,
                "width": width,
                "height": height
            }
    return result


def plot_images_quantities(
        data: Dict[str, Dict[str, int]],
        title: str = "quantities of images with different width and height",
        output_dir: str = "plots"
):
    """绘制图像按照宽高统计的信息

    Args:
        data (Dict[str, Dict[str, int]]): 图像的宽高统计数据，例如：
        {
            "1.33-(2592, 1944)": {
                "count": 1083,
                "width": 2592,
                "height": 1944
            }
        }
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    counts = []
    legends = []
    max_width, max_height, max_count = 0, 0, 0

    plt.figure(figsize=(8, 8))

    for value in data.values():
        count = value.get("count")
        max_count = max(max_count, count)

    color = mcolors.CSS4_COLORS["blue"]

    current_axis = plt.gca()

    for index, value in enumerate(data.values()):
        count = value.get("count")
        width = value.get("width")
        height = value.get("height")
        counts.append(count)
        current_axis.add_patch(plt.Rectangle(
            (0, 0),
            width,
            height,
            linewidth=1,
            edgecolor=color,
            facecolor="none",
            alpha=count*0.5/max_count + 0.1)
        )
        legends.append(f"Pic({width},{height}) - {count}")
        max_width = max(max_width, width)
        max_height = max(max_height, height)

    # plt.legend(legends, ncol=3, loc="best", fontsize=8)
    plt.title("test")
    plt.xlabel("width")
    plt.ylabel("height")
    plt.xlim((-100, max_width + 100))
    plt.ylim((-100, 1.3 * max_height))
    image_name = f"{title}.svg"
    image_path = os.path.join(output_dir, image_name)

    # 保存图像
    plt.savefig(image_path, bbox_inches='tight')

    # 关闭 figure
    plt.close("all")


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


def plot_wh_normalization(raw_data: dict = {},
                          step: float = 0.02,
                          title: str = "Annotations of all categories",
                          output_dir: str = "plots"):
    """ 绘制 bbox 宽高按图像宽高归一化统计热力分布

    Args:
        raw_data (dict, optional): 统计的数据. Defaults to {}.
        step (float, optional): 粒度. Defaults to 0.02.
        title (str, optional): 图像标题. Defaults to "Annotations of all categories".
        output_dir (str, optional): 图像保存目录. Defaults to "plots".
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dw, dh = step, step

    h, w = np.mgrid[0:1+dh:dh, 0:1+dw:dw]
    quantity = round(1.0 / step)
    data = np.zeros((quantity, quantity))
    v_max = 0
    for i in range(0, quantity):
        for j in range(0, quantity):
            w_ij = w[i][j]
            h_ij = h[i][j]
            key = f"{w_ij:.2f}-{h_ij:.2f}"
            data[i][j] = len(raw_data[key]["annotations"])
            if data[i][j] > v_max:
                v_max = data[i][j]

    plt.figure(figsize=(10, 8))

    plt.pcolor(w, h, data, cmap='Blues', vmin=0, vmax=v_max)
    plt.title(title)
    plt.xlabel("width")
    plt.ylabel("height")
    plt.colorbar()

    image_name = f"{title}.svg"
    image_path = os.path.join(output_dir, image_name)

    # 保存图像
    plt.savefig(image_path, bbox_inches='tight')

    # 关闭 figure
    plt.close("all")


def plot_category_quantities(names: list = [],
                             quantities: list = [],
                             title: str = "Quantities of annotations for all categories",
                             output_dir: str = "plots"):
    """ 绘制所有类别的数量统计直方图

    Args:
        names (list, optional): 类别名称列表. Defaults to [].
        quantities (list, optional): 对应类别的 annotations 数量. Defaults to [].
        title (str, optional): 直方图标题. Defaults to "Quantities of all categories".
        output_dir (str, optional): 直方图保存目录. Defaults to "plots".
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(12, 4))

    plt.bar(names, quantities)
    # 绘制数字标签
    for a, b in zip(names, quantities):
        plt.text(a, b+0.05, f"{b}", ha="center", va="bottom", fontsize=8)
    plt.title(title)
    plt.xticks(rotation=30)
    plt.xlabel("category name")
    plt.ylabel("category quantity")

    image_name = f"{title}.svg"
    image_path = os.path.join(output_dir, image_name)

    # bbox_inches 解决 xticks 内容显示不全的问题
    plt.savefig(image_path, bbox_inches='tight')

    # 关闭 figure
    plt.close("all")


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
