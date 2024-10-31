#!/bin/bash

# 遍历 ~/recorded_trackfiles 目录下的所有一级文件夹
for dir in $HOME/recorded_trackfiles/*/; do
    # 获取文件夹名称
    folder_name=$(basename "$dir")
    
    # 执行 Python 脚本，替换 xxx
    python it_all_data_pre.py -d train -s "$folder_name"
    python it_all_data_pre.py -d val -s "$folder_name"
done
