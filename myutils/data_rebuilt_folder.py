import os
import shutil
from config import ROOT, PRE_DATASET_DIR
# 设置路径
DATASET_DIR = PRE_DATASET_DIR
RECORD_DIR = os.path.join(PRE_DATASET_DIR,"recorded_trackfiles")

os.makedirs(RECORD_DIR, exist_ok=True)

def create_structure_and_move(filename, filetype):
    basename_no_ext = os.path.splitext(os.path.basename(filename))[0].rsplit(f"_{filetype}", 1)[0]

    train_dir = os.path.join(RECORD_DIR, basename_no_ext, "train")
    val_dir = os.path.join(RECORD_DIR, basename_no_ext, "val")
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    if filetype == "train":
        shutil.copy(filename, train_dir)
    else:
        shutil.copy(filename, val_dir)

# 遍历train文件夹中的所有csv文件
train_folder = os.path.join(DATASET_DIR, "train")
for file in os.listdir(train_folder):
    if file.endswith(".csv"):
        create_structure_and_move(os.path.join(train_folder, file), "train")

# 遍历val文件夹中的所有csv文件
val_folder = os.path.join(DATASET_DIR, "val")
for file in os.listdir(val_folder):
    if file.endswith(".csv"):
        create_structure_and_move(os.path.join(val_folder, file), "val")

print(f"操作完成，文件已成功复制并重新组织到 {RECORD_DIR}")
