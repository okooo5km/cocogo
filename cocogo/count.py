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
from .utilities import (plot_wh,
                        CoCoCallback,
                        build_idx_table,
                        init_scatter_data,
                        plot_wh_normalization,
                        init_norm_scatter_data,
                        plot_images_quantities,
                        plot_category_quantities,
                        classify_with_aspect_ratio,
                        find_max_size_of_annotations)


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

    plots_dir = os.path.abspath(
        f"{os.path.basename(json_file).replace('.json', '')}-plots")

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
                    count = value.get('count', 0)
                    echo_str += typer.style(f"{count}",
                                            fg=typer.colors.BRIGHT_GREEN, bold=True)
                    echo_str += typer.style(" 张", fg=typer.colors.BRIGHT_BLACK)
                    typer.echo(echo_str)
                # 绘制图像统计信息
                plot_images_quantities(classified_result, output_dir=plots_dir)

                typer.secho(f"\n图像不同宽高比数量统计图像保存至目录 - {plots_dir}",
                            fg=typer.colors.BRIGHT_YELLOW)

            elif item == "annotations":
                # 获取图像最大宽、高
                max_width, max_height = find_max_size_of_annotations(item_obj)
                # 初始化归一化散点图数据
                NORM_STEP = 0.02
                norm_scatter_data = init_norm_scatter_data(step=NORM_STEP)

                # 初始化标注框原尺寸散点数据
                max_size = max(max_width, max_height)
                STEP = 64
                scatter_data = init_scatter_data(max_size, max_size, STEP)

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
                    ann_max_size = max(ann_width, ann_height)
                    # 减 2 是为了不让归一化数据超过 1.0 ，2 随意定的，大于 0 即可
                    if ann_width > image_width:
                        ann_width = image_width - 2
                    if ann_height > image_height:
                        ann_height = image_height - 2
                    w = ann_width / image_width
                    h = ann_height / image_height

                    category["data"].append(annotation)

                    # 存值范围的尺寸
                    _w = ann_width // STEP * STEP
                    _h = ann_height // STEP * STEP

                    # 归一化尺寸
                    __w = w // NORM_STEP * NORM_STEP
                    __h = h // NORM_STEP * NORM_STEP

                    scatter_key = f"{_w}-{_h}"
                    scatter_data[scatter_key]["annotations"].append(idx)

                    # 归一化数据 key
                    norm_scatter_key = f"{__w:.2f}-{__h:.2f}"
                    norm_scatter_data[norm_scatter_key]["annotations"].append(
                        idx)

                    if "scatter" not in category:
                        category["scatter"] = init_scatter_data(
                            max_x=max_size,
                            max_y=max_size,
                            step=STEP)
                    if "norm_scatter" not in category:
                        category["norm_scatter"] = init_norm_scatter_data(
                            step=NORM_STEP)
                    if "max_size" not in category:
                        category["max_size"] = 0

                    category["scatter"][scatter_key]["annotations"].append(idx)
                    category["norm_scatter"][norm_scatter_key]["annotations"].append(
                        idx)
                    category["max_size"] = max(
                        category["max_size"], ann_max_size)

                typer.secho("完成！", fg=typer.colors.BRIGHT_BLACK)

                typer.secho("\n标注数据按分类统计如下：", fg=typer.colors.BRIGHT_YELLOW)

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
                    if category.get("norm_scatter"):
                        plot_wh_normalization(category["norm_scatter"],
                                              title=f"Annotation normalized size of {category['name']}",
                                              output_dir=plots_dir)

                    # 绘制每一种类别的宽高分布图
                    if category.get("scatter"):
                        plot_wh(category["scatter"],
                                step=STEP,
                                max_size=category["max_size"],
                                title=f"Annotation size of {category['name']}",
                                output_dir=plots_dir)

                    category_names.append(category["name"])
                    quantities.append(len(category["data"]))

                # 绘制归一化的宽高分布图
                plot_wh_normalization(norm_scatter_data,
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
