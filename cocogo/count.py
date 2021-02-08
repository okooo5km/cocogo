#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : count.py
@desc          : count 子命令处理
@dateTime      : 2021/01/23 11:28:53
@author        : 5km
@contact       : 5km@smslit.cn
"""
import os
import json

import typer

from .models import CoCOItem
from .utilities import (CoCoCallback,
                        build_idx_table,
                        init_scatter_data,
                        plot_wh_normalization,
                        plot_category_quantities,
                        classify_with_aspect_ratio)


def main(json_file: str = typer.Argument(..., callback=CoCoCallback.check_file, help="指定待检索的 json 文件"),
         item: CoCOItem = typer.Option(CoCOItem.images, "--item", "-i", show_choices=True, help="检索项")):

    def echo_item_count(item: CoCOItem, num):
        echo_str = typer.style("\n检索到数据项 ", fg=typer.colors.BRIGHT_YELLOW)
        echo_str += typer.style(f"{item.value} ",
                                fg=typer.colors.BRIGHT_BLUE, bold=True)
        echo_str += typer.style(f"{num}",
                                fg=typer.colors.BRIGHT_GREEN, bold=True)
        echo_str += typer.style(" 条记录!", fg=typer.colors.BRIGHT_YELLOW)
        typer.echo(echo_str)

    typer.secho("\n加载 json 文件数据中...", fg=typer.colors.BRIGHT_BLACK)
    with open(json_file, "r") as fp:
        json_data = json.load(fp)

    keys = json_data.keys()

    if item in keys:
        item_obj = json_data.get(item)
        if isinstance(item_obj, list):
            echo_item_count(item, len(item_obj))
            if item == "images":
                classified_result = classify_with_aspect_ratio(images=item_obj)
                typer.secho("\n图像不同宽高比数量统计如下:", fg=typer.colors.BRIGHT_YELLOW)
                for ratio_str, value in classified_result.items():
                    echo_str = typer.style(
                        f"  宽高比 {ratio_str}: ", fg=typer.colors.BRIGHT_BLUE)
                    echo_str += typer.style(f"{value}",
                                            fg=typer.colors.BRIGHT_GREEN, bold=True)
                    echo_str += typer.style(" 张", fg=typer.colors.BRIGHT_BLACK)
                    typer.echo(echo_str)

            elif item == "annotations":
                # 初始化散点图数据
                STEP = 0.02
                scatter_data = init_scatter_data(step=STEP)
                # 建立 images 索引
                image_idx_table = build_idx_table(
                    json_data.get("images"),
                    "images"
                )
                # 建立 categories 索引
                category_idx_table = build_idx_table(
                    json_data.get("categories"),
                    "categories"
                )

                # 统计 bbox 数据
                typer.secho("\n统计标注数据...", fg=typer.colors.BRIGHT_BLACK)
                for idx, annotation in enumerate(item_obj):
                    image_id = annotation.get("image_id")
                    category_id = annotation.get("category_id")
                    image = image_idx_table.get(image_id)
                    category = category_idx_table.get(category_id)

                    # 归一化 width height
                    image_width = image.get("width")
                    image_height = image.get("height")
                    ann_width = annotation.get("bbox")[2]
                    ann_height = annotation.get("bbox")[3]
                    if ann_width > image_width:
                        ann_width = image_width - 2
                    if ann_height > image_height:
                        ann_height = image_height - 2
                    w = ann_width / image_width
                    h = ann_height / image_height

                    category["data"].append(idx)

                    _w = w // STEP * STEP
                    _h = h // STEP * STEP

                    scatter_key = f"{_w:.2f}-{_h:.2f}"
                    scatter_data[scatter_key]["annotations"].append(idx)

                    if "scatter" not in category:
                        category["scatter"] = init_scatter_data(step=STEP)

                    category["scatter"][scatter_key]["annotations"].append(idx)

                typer.secho("完成！", fg=typer.colors.BRIGHT_BLACK)

                typer.secho("\n标注数据按分类统计如下：", fg=typer.colors.BRIGHT_YELLOW)
                plots_dir = os.path.abspath("plots")
                quantities = []
                category_names = []
                for category in category_idx_table.values():
                    echo_info = typer.style(f"  {category.get('name')}: ",
                                            fg=typer.colors.BRIGHT_BLACK,
                                            bold=True)
                    echo_info += typer.style(f"{len(category.get('data'))}",
                                             fg=typer.colors.BRIGHT_GREEN,
                                             bold=True)
                    echo_info += typer.style(f" 条",
                                             fg=typer.colors.BRIGHT_BLACK)
                    typer.echo(echo_info)
                    # 绘制每一种类别的宽高归一化分布图
                    plot_wh_normalization(category["scatter"],
                                          title=f"Annotations of {category['name']}")
                    category_names.append(category["name"])
                    quantities.append(len(category["data"]))

                # 绘制归一化的宽高分布图
                plot_wh_normalization(scatter_data,
                                      output_dir=plots_dir)
                # 绘制所有类别对应 annotation 的数量直方图
                plot_category_quantities(category_names,
                                         quantities,
                                         output_dir=plots_dir)

                echo_info = typer.style("\n统计图表已保存至目录 - ",
                                        fg=typer.colors.BRIGHT_YELLOW)
                echo_info += typer.style(f"{plots_dir}",
                                         fg=typer.colors.BRIGHT_GREEN,
                                         bold=True)
                typer.echo(echo_info)

        else:
            echo_item_count(item, 1)

    else:
        echo_item_count(item, 0)
