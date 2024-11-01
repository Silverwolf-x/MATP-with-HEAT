# 配置说明
20241101 for windows

- 设置项目目录地址ROOT，随时随地运行代码
- 再次用os.path.join()规范所有路径，windows和linux都能顺利运行
- 将shell文件改为python文件方便直接使用

## 前言

requirements的版本太老了，wheel编译会失败，换用最新的版本就行。python==3.10.15

### 项目目录ROOT设置

在`MATP-with-HEAT\myutils\config.py`下，填写ROOT为你要存放的地方。以下是示例

```python
ROOT = 'D:' # 放到D盘
ROOT = 'C:\\Users\\Administrator\\Desktop' # 放到桌面。Administrator是我的用户名，具体以你的桌面名字为准
```

填写`DATASET`为要处理的某个数据集。以下用`DATASET='Multi-v1'`做示例，其他同理

### 放置文件

在 https://github.com/Silverwolf-x/MATP-with-HEAT 下载源码，把dataset和MATP-with-HEAT放在ROOT。例如，如果你设置`ROOT = 'D:'`，那么应该放在D盘下面

现在ROOT放置着以下文件

```text
├── dataset
│   ├── Multi-v1
│   ├── ...
├── MATP-with-HEAT
│   ├── ...
```

## 预处理--得到sorted文件

目标：重新按frame_id排序得到sorted文件夹

### 重构文件夹

- 目标：重构Multi-v1的文件夹的样式以进行下一步处理
- 运行：`MATP-with-HEAT\myutils\data_rebuilt_folder.py`
- 输入（运行时自动输入）：Multi-v1下的所有csv文件
- 输出：一个地址。重构后的文件放在这个文件夹内，即dataset\Multi-v1\recorded_trackfiles

### case_id处理

- 目标：将csv数据按照case_id拆解成多个csv，并去除case_id列，以匹配`segment_data.py`的输入格式
- 注释：改动`split_case.py`变量名`target_case_name`，示例如下
 ```python
target_case_name = 'DR_CHN_Merging_ZS0' # 默认。只处理ZS0
target_case_name = None # 全部处理
```
- 输入（运行时自动输入）：dataset\Multi-v1\recorded_trackfiles\下指定的`target_case_name`的所有csv
- 运行：`MATP-with-HEAT\myutils\split_case.py`
- 输出：一个地址。处理后的文件放在这个文件夹内，即ROOT\recorded_trackfiles

> 代码说明：用pathlib截取路径

### sorted

- 目标：重新按frame_id排序得到sorted文件夹
- 注释：`segment_data.py`采用default指令的默认设置为block_len=40，gap_len=20，argv_len=0，一般够用
- 输入（运行时自动输入）：ROOT\recorded_trackfiles下所有csv
- 运行：`MATP-with-HEAT\myutils\segment_data.py`
- 输出：ROOT\recorded_trackfiles下train和val各得到sorted文件夹

## 主程序

现在ROOT放置着以下文件

```text
├── dataset
├── MATP-with-HEAT
│   ├── ...
├── recorded_trackfiles
│   ├── DR_CHN_Merging_ZS0
│   │   ├── train
│   │   │   └── sorted
│   │   └── val
│   │       └── sorted
│   ├── ...
```

### map对应

- 目标：`MATP-with-HEAT/visualizations/map_png`和`MATP-with-HEAT/visualizations/osm_maps`要有对应场景的png和osm
- 示例：处理DR_CHN_Merging_ZS0，要复制一份DR_CHN_Merging_ZS0_map.png和DR_CHN_Merging_ZS0.osm放到上述位置

### 准备载入数据【运行时间很长】

- 目标：合并每个csv和地图的坐标，将每个csv转化成pyg，生成一个地图数据MAP.pt
- 输入（运行时自动输入）：ROOT\recorded_trackfiles下所有csv
- 运行：`MATP-with-HEAT\myutils\data_pre_run.py`
- 输出：MAP.pt和每个csv转换后的pyg。输出在ROOT\heatmtp_it_data
- 注释：ZS0的val中1.5GB的csv处理完约需要90分钟，具体时间视CPU性能

> 代码说明：源代码`np.unique(self.cur_track['frame_id'])[10:-self.fut_len]`的[10:-30]提取会让返回空列表,使得无法生成pyg

> 可以先停止并注释`data_pre_run.py`的train部分再运行，用生成val和train的部分pyg继续做下一步测试


### train

现在ROOT放置着以下文件

```text
├── dataset
├── MATP-with-HEAT
├── recorded_trackfiles
├── heatmtp_it_data
│   ├── DR_CHN_Merging_ZS0
│   │   ├── train
│   │   ├── val
│   │   └── MAP.pt
│   ├── ...
```

- 目标：尝试使用部分pyg运行，看到训练进度条就是胜利
- 注释：如果使用其他模型，可能需要更改`args['encoder_size']`和`args['heat_in_channels_node']`=128
- 输入（运行时自动输入）：ROOT\recorded_trackfiles下所有csv
- 运行：`MATP-with-HEAT\it_all_dataset.py`
- 输出：输出log和模型在`MATP-with-HEAT\it_all_models`文件夹

![](myutils\finish.jpg)


---

# MATP-with-HEAT
This repo contains the code for our paper entitled "Multi-Agent Trajectory Prediction with Heterogeneous Edge-Enhanced Graph Attention Network", IEEE T-ITS, 2022.

## Install dependencies via pip.
`pip install -r requirements.txt`

## Data preprocessing
The strucutre of the raw INTERACTION Dataset can be found in `INTERACTION Dataset Tree.txt`.

To obtain the sorted dataset, please refer to 
[INTERPRET_challenge_regular_generalizability_track](https://github.com/interaction-dataset/INTERPRET_challenge_regular_generalizability_track). 

Run `bash datapre_run.sh` to process all the scenarios provided by the INTERACTION dataset.

## Models
Base model -> Heat model -> HeatIR model.

## Traning
Run `python it_all_train.py -m Heat` to train the one-channel HEAT-based trajectory predictor.

## Validation

## Citation
If you have found this work to be useful, please consider citing our paper:
```
@article{mo2022multi,
  title={Multi-agent trajectory prediction with heterogeneous edge-enhanced graph attention network},
  author={Mo, Xiaoyu and Huang, Zhiyu and Xing, Yang and Lv, Chen},
  journal={IEEE Transactions on Intelligent Transportation Systems},
  year={2022},
  publisher={IEEE}
}
```
