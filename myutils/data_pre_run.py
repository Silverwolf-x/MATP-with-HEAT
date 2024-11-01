import os
import subprocess
from config import DATASET_DIR,ROOT
# 定义 recorded_trackfiles 目录路径
recorded_trackfiles_dir = DATASET_DIR

# 遍历目录下的所有一级文件夹
for dir_name in os.listdir(recorded_trackfiles_dir):
    dir_path = os.path.join(recorded_trackfiles_dir, dir_name)
    python_path = os.path.join(ROOT,'MATP-with-HEAT','it_all_data_pre.py')
    if os.path.isdir(dir_path):
        subprocess.run(['python', python_path, '-d', 'train', '-s', dir_name])
        subprocess.run(['python', python_path, '-d', 'val', '-s', dir_name])