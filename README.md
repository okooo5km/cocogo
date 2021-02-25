# CoCoGo

又名“抠二狗”，用于检索指定 coco json 文件中的关键信息以及进行简单的数据优化处理。

使用 [poetry](https://python-poetry.org/)构建项目和管理环境依赖。

## python 

使用 python3.6 以上版本开发。

## 安装

### pip 安装

```shell
pip install cocogo
```

### poetry 安装

```shell
# 克隆仓库
git clone https://github.com/smslit/cocogo.git
# 安装
cd cocogo && poetry install
```

## 开发

安装 poetry 后执行以下命令就可以 

```shell
# 仅安装依赖
poetry install --no-root
```

## 使用

执行命令打印帮助信息。

```shell
cocogo --help

Usage: cocogo [OPTIONS] COMMAND [ARGS]...

  此工具可以帮助您针对 coco 标注文件进行简单的检索或简单处理，帮助详见 https://github.com/smslit/cocogo

Options:
  --help                          Show this message and exit.

Commands:
  count     统计数据
  info      查看文件中的基本信息，可以指定具体内容项
  list      查询数据
  optimize  优化数据，删除没有的图像数据及相关标注信息
  version   查看当前使用 cocogo 的版本
```

可以看到目前功能有：

- 统计数据
- 查看基本信息
- 检索数据
- 优化数据
- 查看版本

每个功能对应一个子命令。

### 统计数据

使用 count 子命令。

```shell
cocogo count --help

Usage: cocogo count [OPTIONS] JSON_FILE

  统计数据

Arguments:
  JSON_FILE  指定待检索的 json 文件  [required]

Options:
  -i, --item [info|type|images|annotations|categories|licenses]
                                  检索项  [default: images]
  --help                          Show this message and exit.
```

可以看到使用方式很简单，当然功能也很简单，只有一个选项就是指定要统计项，统计项不指定默认为图像，现在只是统计个数。

比如：

```shell
cocogo count -i images eval.json

加载 json 文件数据中...

检索到数据项 images 3471 条记录!

图像不同宽高比数量统计如下:
  宽高比 1.33-(2592, 1944): 1083 张
  宽高比 1.33-(1200, 900): 2195 张
  宽高比 1.76-(1920, 1088): 20 张
  宽高比 1.33-(3264, 2448): 36 张
  宽高比 1.33-(1296, 972): 60 张
  宽高比 1.33-(3200, 2400): 25 张
  宽高比 1.33-(900, 675): 4 张
  宽高比 1.33-(2560, 1920): 11 张
  宽高比 1.33-(4160, 3120): 1 张
  宽高比 1.79-(1276, 714): 2 张
  宽高比 1.78-(1280, 720): 8 张
  宽高比 0.75-(960, 1280): 2 张
  宽高比 1.33-(896, 672): 3 张
  宽高比 1.33-(907, 680): 7 张
  宽高比 1.33-(3968, 2976): 3 张
  宽高比 1.33-(648, 486): 3 张
  宽高比 0.75-(1080, 1440): 1 张
  宽高比 1.22-(704, 576): 2 张
  宽高比 1.78-(1920, 1080): 3 张
  宽高比 1.33-(1920, 1440): 1 张
  宽高比 0.75-(2976, 3968): 1 张
```

统计图像会列出各个宽、高比的图像个数，同时会生成按照宽高统计的尺寸分布图，如下：

<img src="https://pichome-1254392422.cos.ap-chengdu.myqcloud.com/uPic/5-20210225171723.svg" width="480px">

另外统计 annotation 的化还会生成相应的图表（各类别 annotation 的数量、 各类别 annotation 宽高归一化分布）：

```shell
cocogo count -i annotations train.json 

加载 json 文件数据中...

检索到数据项 annotations 371852 条记录!

建立 images 索引...
完成!

建立 categories 索引...
完成!

统计标注数据...
完成！

标注数据按分类统计如下：
  moxxxxne: 56686 条
  toxxxxne: 85002 条
  pxxxxar: 4465 条
  pxxxxr: 19337 条
  txxxxk: 18322 条
  dxxxxr: 49688 条
  fxxxxe: 3303 条
  sxxxxg: 25944 条
  cxxxxs: 6068 条
  dxxxxof: 45610 条
  cxxxxer: 8524 条
  pxxxxe: 5152 条
  vxxxxn: 6995 条
  txxxxer: 12392 条
  sxxxxck: 9377 条
  rxxxxer: 1596 条
  wxxxxl: 5584 条
  bxxxxd: 7807 条

统计图表已保存至目录 - /data/plots
```

- 各类别统计数量直方图例图：

  <img src="https://pichome-1254392422.cos.ap-chengdu.myqcloud.com/uPic/3-20210225171743.svg" width="480px">

- 所有类别的 annotation 宽高归一化分布图例图：

  <img src="https://pichome-1254392422.cos.ap-chengdu.myqcloud.com/uPic/1-20210225171755.svg" width="480px">

- 指定类别的 annotation 宽高归一化分布图例图（motorcarane）：

  <img src="https://pichome-1254392422.cos.ap-chengdu.myqcloud.com/uPic/2-20210225171806.svg" width="480px">

- 指定类别的 annotation 宽高实际尺寸分布图例图（motorcarane）：

  <img src="https://pichome-1254392422.cos.ap-chengdu.myqcloud.com/uPic/4-20210225171818.svg" width="480px">

### 查看基本信息

使用 info 子命令。
```shell
cocogo info --help

Usage: cocogo info [OPTIONS] JSON_FILE

  查看文件中的基本信息，可以指定具体内容项

Arguments:
  JSON_FILE  指定待检索的 json 文件  [required]

Options:
  -i, --item [info|type|images|annotations|categories|licenses]
                                  检索项
  --help                          Show this message and exit.
```

用来查看包含了哪些关键字段信息，又一个指定查看项的参数，不指定参数项会列出指定 json 文件中包含的关键字段：

```shell
cocogo info eval.json

文件中包含内容项如下：

  images, type, annotations, categories
```

所以我们就可以查看上面列出的文件包含内容项的信息，比如 images 的：

```shell
cocogo info -i images eval.json

指定项 images 内容格式如下：

  file_name: 97454.jpg
  height: 1944
  width: 2592
  id: 0
```

一般就是看内容结构。

### 检索数据

使用 list 子命令， 主要是列出指定范围内指定项目的数据。

```shell
cocogo list --help                                       
Usage: cocogo list [OPTIONS] JSON_FILE

  查询数据

Arguments:
  JSON_FILE  指定待检索的 json 文件  [required]

Options:
  -i, --item [info|type|images|annotations|categories|licenses]
                                  检索项  [default: images]
  -s, --start INTEGER             列出数据的起始位置  [default: 0]
  -e, --end INTEGER               列出数据的结束位置  [default: 10]
  --help                          Show this message and exit.
```

默认列出图像的 0 ～ 10 的数据。

比如列出标注的 12 ～ 18 (左闭右开区间) 的数据：

```shell
cocogo list -s 12 -e 18 -i annnotations eval.json

加载 json 文件数据中...

  {'area': 16544, 'iscrowd': 0, 'bbox': [293, 485, 176, 94], 'category_id': 6, 'ignore': 0, 'segmentation': [], 'image_id': 1, 'id': 13}
  {'area': 21012, 'iscrowd': 0, 'bbox': [1253, 196, 103, 204], 'category_id': 12, 'ignore': 0, 'segmentation': [], 'image_id': 1, 'id': 14}
  {'area': 22704, 'iscrowd': 0, 'bbox': [709, 167, 86, 264], 'category_id': 12, 'ignore': 0, 'segmentation': [], 'image_id': 1, 'id': 15}
  {'area': 1204, 'iscrowd': 0, 'bbox': [649, 387, 43, 28], 'category_id': 6, 'ignore': 0, 'segmentation': [], 'image_id': 1, 'id': 16}
  {'area': 1406, 'iscrowd': 0, 'bbox': [472, 342, 38, 37], 'category_id': 6, 'ignore': 0, 'segmentation': [], 'image_id': 1, 'id': 17}
  {'area': 5160, 'iscrowd': 0, 'bbox': [337, 453, 120, 43], 'category_id': 5, 'ignore': 0, 'segmentation': [], 'image_id': 1, 'id': 18}

共列出 6(12~18) 条记录!
```

### 优化数据

```shell
cocogo optimize --help

Usage: cocogo optimize [OPTIONS] JSON_FILE IMG_DIR

  优化数据，删除没有的图像数据及相关标注信息

Arguments:
  JSON_FILE  CoCo 标注文件路径  [required]
  IMG_DIR    标注文件对应的图像目录  [required]

Options:
  -p, --prefix TEXT               优化后标注文件名的前缀  [default: processed]
  -v, --verbose                   罗嗦模式，打印全部信息
  -o, --override                  保存文件覆盖原标注文件
  --check-size / --no-check-size  检查标注文件中图像宽高是否与图像文件一致  [default: False]
  --help                          Show this message and exit.
```

默认情况下，生成优化后的 json 文件带有前缀 `processed`，如果指定 `override` 选项会覆盖原来的 json 文件。

默认优化的内容只是检查数据中图像文件是否存在，不存在就会删除相应的图像记录和标注记录，如果指定 `--check-size` 会检查图像数据中宽、高是否与原图的宽高一致，如果不一致会更新为正确的宽、高数据。

两个必须的参数是：

- coco json 文件
- 对应 json 文件的图像目录

```shell
cocogo optimize train.json train_imgs 

Json 数据加载中 ...
  完成!

缺失的图像检索中 ...
checking  [████████████████████████████████████]  100%         
  完成!

缺失图像相关标注数据检索中 ...
checking  [████████████████████████████████████]  100%         
  完成!

Json 数据保存中 ...
  完成! - ./processed_train.json

优化总结:
  - 图像: 0 / 127015 (缺失/全部)
  - 标注: 0 / 371852 (失效/全部)
```