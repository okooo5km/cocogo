#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : optimize.py
@desc          : 定义子命令 optimize 的处理逻辑
@dateTime      : 2021/01/23 11:07:03
@author        : 5km
@contact       : 5km@smslit.cn
"""
import os
import json
import shutil
from datetime import datetime

import typer
import imagesize

from .utilities import CoCoCallback


def echo_summary_item(item: str, num1: int, num2: int, comment: str = None):
    echo_str = typer.style(f"  - {item}: ",
                           fg=typer.colors.YELLOW)
    echo_str += typer.style(f"{num1}",
                            fg=typer.colors.BRIGHT_RED, bold=True)
    echo_str += typer.style(f" / ",
                            fg=typer.colors.BRIGHT_BLACK)
    echo_str += typer.style(f"{num2} ",
                            fg=typer.colors.BRIGHT_GREEN, bold=True)
    if comment:
        echo_str += typer.style(comment, fg=typer.colors.BRIGHT_BLACK)

    typer.echo(echo_str)


def main(json_file: str = typer.Argument(...,
                                         callback=CoCoCallback.check_file,
                                         help="CoCo 标注文件路径"),
         img_dir: str = typer.Argument(...,
                                       callback=CoCoCallback.check_img_dir,
                                       help="标注文件对应的图像目录"),
         prefix: str = typer.Option("processed", "--prefix", "-p",
                                    help="优化后标注文件名的前缀"),
         verbose: bool = typer.Option(False, "--verbose", "-v", show_default=False,
                                      help="罗嗦模式，打印全部信息"),
         override: bool = typer.Option(False, "--override", "-o", show_default=False,
                                       help="保存文件覆盖原标注文件"),
         check_size: bool = typer.Option(False,
                                         help="检查标注文件中图像宽高是否与图像文件一致")):
    typer.secho("\nJson 数据加载中 ...", fg=typer.colors.YELLOW)
    with open(json_file, "r") as fp:
        json_data = json.load(fp)
    typer.secho("  完成!", fg=typer.colors.BRIGHT_GREEN)

    images_data = json_data.get("images", [])
    annotations_data = json_data.get("annotations", [])

    total_num_of_img = len(images_data)
    miss_num_of_img = 0
    new_images_data = []
    deleted_img_ids = []

    typer.secho("\n缺失的图像检索中 ...", fg=typer.colors.YELLOW)

    with typer.progressbar(range(total_num_of_img), fill_char="█",
                           label="checking",  empty_char="") as progress:
        for idx in progress:
            image = images_data[idx]
            image_id = image.get("id")
            file_name = image.get("file_name")
            file_path = os.path.join(img_dir, file_name)
            if not os.path.exists(file_path):
                miss_num_of_img += 1
                deleted_img_ids.append(image_id)
                if verbose:
                    typer.echo(f"  {image_id}. {file_name} - 缺失")
            else:
                if check_size:
                    image_width, image_height = imagesize.get(file_path)
                    if (image_width != image["width"]) or (image_height != image["height"]):
                        image["width"] = image_width
                        image["height"] = image_height
                        if verbose:
                            typer.echo(
                                f"  {image_id}. {file_name} - 宽高与图像实际尺寸不一致，已修复")
                new_images_data.append(image)
    typer.secho("  完成!", fg=typer.colors.BRIGHT_GREEN)

    deleted_num_of_anno = 0
    total_num_of_anno = len(annotations_data)
    new_annotations_data = []

    typer.secho("\n缺失图像相关标注数据检索中 ...", fg=typer.colors.YELLOW)
    with typer.progressbar(range(total_num_of_anno), fill_char="█",
                           label="checking",  empty_char="") as progress:
        for idx in progress:
            annotation = annotations_data[idx]
            image_id = annotation.get("image_id")
            if image_id in deleted_img_ids:
                deleted_num_of_anno += 1
                if verbose:
                    typer.echo(f"  {annotation} - 失效")
            else:
                new_annotations_data.append(annotation)
    typer.secho("  完成!", fg=typer.colors.BRIGHT_GREEN)

    typer.secho("\nJson 数据保存中 ...", fg=typer.colors.YELLOW)
    new_json_data = {}
    for key in json_data.keys():
        if key == "images":
            new_json_data[key] = new_images_data
        elif key == "annotations":
            new_json_data[key] = new_annotations_data
        else:
            new_json_data[key] = json_data[key]
    if override:
        new_json_file_path = json_file
        json_file_backup = json_file + ".backup." + \
            datetime.now().strftime("%Y%m%d%H%M%S")
        # backup the in file
        shutil.copy(json_file, json_file_backup)
    else:
        new_json_file_name = f"{prefix}_{os.path.basename(json_file)}"
        new_json_file_path = os.path.join(os.path.dirname(json_file),
                                          new_json_file_name)
    with open(new_json_file_path, "w") as fp:
        json.dump(new_json_data, fp)
    echo_str = typer.style("  完成! - ", fg=typer.colors.BRIGHT_GREEN)
    echo_str += typer.style(f"{new_json_file_path}",
                            fg=typer.colors.GREEN, bold=True)
    typer.echo(echo_str)

    typer.secho("\n优化总结:", fg=typer.colors.BRIGHT_YELLOW, bold=True)
    echo_summary_item("图像", miss_num_of_img, total_num_of_img, "(缺失/全部)")
    echo_summary_item("标注", deleted_num_of_anno, total_num_of_anno, "(失效/全部)")
