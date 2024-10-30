# 配置说明
20241030
## 前言
requirements的版本太老了，wheel编译会失败，换用最新的版本就行。python==3.10.15

现在我们有几个文件夹在主目录~下并列，后两者是git clone我fork后的版本得到的
```
├── dataset
│   ├── ...
├── INTERPRET_challenge_regular_generalizability_track
│   ├── ...
├── MATP-with-HEAT
│   ├── ...
```
以下都以dataset/Multi-v1为示例，其他同理
## 预处理
**INTERPRET_challenge_regular_generalizability_track** 目标：重新按frame_id排序得到sorted文件夹
0. case_id处理说明
    本次处理中case_id是不规范的列，综合考虑如下因素：
    - INTERPRET_challenge_regular_generalizability_track代码中不允许包含case_id列
    - MATP-with-HEAT并没有提及case_id列
    - MATP-with-HEAT数据载入中的所有samples，是指所有scenario_names(如DR_CHN_Merging_ZS2)文件夹下的所有csv，详见IT_ALL_MTP_dataset函数定义
    因此决定，将每个csv按照case_id拆分成若干个csv

1. 重构文件夹
    在`data_rebuilt_folder.sh`开头填写要运行的数据集地址，然后运行
    ```cmd
    sh data_rebuilt_folder.sh
    ```
    在数据集dataset/Multi-v1下生成符合input样式的`recorded_trackfiles`，复制到`INTERPRET_challenge_regular_generalizability_track`下
2. case_id处理


## 主程序
**MATP-with-HEAT**

按照以下格式摆放数据集
```
├── maps
├── recorded_trackfiles
│   ├── DR_CHN_Merging_ZS
│   │   ├── train
│   │   │   └── sorted
│   │   └── val
│   │       └── sorted
│   ├── ...
│   │   
│   ├── ...
│   │   
│   └── DR_USA_Roundabout_SR
│       ├── train
│       │   └── sorted
│       └── val
│           └── sorted
└── submission-sample
```
1. 建立config.py



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
