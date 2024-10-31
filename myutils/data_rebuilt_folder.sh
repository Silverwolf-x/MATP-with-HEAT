#!/bin/bash

# 设置路径
DATASET_DIR="$HOME/dataset/Multi-v1"
RECORD_DIR="$DATASET_DIR/recorded_trackfiles"

# 创建recorded_trackfiles文件夹（如果不存在）
mkdir -p "$RECORD_DIR"

# 函数：创建新文件夹结构并移动文件
create_structure_and_move() {
    local filename="$1"
    local filetype="$2" # train或val
    local basename_no_ext=$(basename "$filename" .csv | sed "s/_$filetype//")

    # 创建新的文件夹结构
    mkdir -p "$RECORD_DIR/$basename_no_ext/train"
    mkdir -p "$RECORD_DIR/$basename_no_ext/val"

    # 移动文件到对应的文件夹
    if [ "$filetype" == "train" ]; then
        cp "$filename" "$RECORD_DIR/$basename_no_ext/train/"
    else
        cp "$filename" "$RECORD_DIR/$basename_no_ext/val/"
    fi
}

# 遍历train文件夹中的所有csv文件
for file in "$DATASET_DIR/train/"*.csv; do
    create_structure_and_move "$file" "train"
done

# 遍历val文件夹中的所有csv文件
for file in "$DATASET_DIR/val/"*.csv; do
    create_structure_and_move "$file" "val"
done

echo "操作完成，文件已成功复制并重新组织到$RECORD_DIR"
