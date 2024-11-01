import glob
import os
import pandas as pd
import sys
from tqdm import tqdm
from config import DATASET_DIR,PRE_DATASET_DIR,ROOT
import pdb
from pathlib import Path
# 设置输入目录

def split_path(original_path,base_path):
    r'''
    D:\dataset\Multi-v1\recorded_trackfiles\DR_CHN_Merging_ZS0\train截取为D:\recorded_trackfiles\DR_CHN_Merging_ZS0\train
    '''
    original_path = Path(original_path)
    relative_path = original_path.relative_to(base_path) # 去除 base_path 部分
    new_path = os.path.join(ROOT,relative_path)
    return new_path

def split_csv(file_path):
    """按照 case_id 拆分 CSV 文件并保存新的文件"""
    csv_file = os.path.basename(file_path)
    case_name = os.path.splitext(csv_file)[0]  

    global OUTPUT_DIR
    # pdb.set_trace()
    OUTPUT_DIR = split_path(os.path.dirname(file_path),base_path=PRE_DATASET_DIR)
    os.makedirs(OUTPUT_DIR,exist_ok=True)

    df = pd.read_csv(file_path, dtype={'case_id': 'category'})  # 将 case_id 列设置为分类类型

    if 'case_id' in df.columns:
        for case_id, group in tqdm(df.groupby('case_id',observed=False),miniters=500): 

            group.drop(columns='case_id',inplace=True)
            output_file_name = f"{case_name}_{pd.to_numeric(case_id).astype(int)}.csv"  
            output_file_path = os.path.join(OUTPUT_DIR, output_file_name)

            group.to_csv(output_file_path, index=False, compression='infer')  
    else:
        print(f"文件 {csv_file} 中未找到 'case_id' 列。")

if __name__ == '__main__':

    # 获取指定的处理文件夹名称（如无指定则处理所有文件夹）
    target_case_name = 'DR_CHN_Merging_ZS0'

    csv_files = []
    
    for root, dirs, files in os.walk(PRE_DATASET_DIR):
        for f in files:
            if f.endswith('.csv'):
                # 如果指定了目标文件夹，只处理该文件夹中的文件
                if target_case_name:
                    if target_case_name in root:
                        csv_files.append(os.path.join(root, f))
                else:
                    csv_files.append(os.path.join(root, f))


    # pdb.set_trace()
    for csv_file in csv_files:
        split_csv(csv_file)
    print(f'完成！输出文件夹在{OUTPUT_DIR}')
