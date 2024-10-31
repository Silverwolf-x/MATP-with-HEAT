import os
import pandas as pd
import sys
from tqdm import tqdm
# 设置输入目录

def split_csv(file_path):
    """按照 case_id 拆分 CSV 文件并保存新的文件"""
    csv_file = os.path.basename(file_path)
    case_name = os.path.splitext(csv_file)[0]  
    sub_dir = os.path.dirname(file_path)  # 获取当前文件所在目录

    # 读取 CSV 文件，指定数据类型以优化内存使用
    df = pd.read_csv(file_path, dtype={'case_id': 'category'})  # 将 case_id 列设置为分类类型

    if 'case_id' in df.columns:
        # 按 'case_id' 拆分 DataFrame
        for case_id, group in tqdm(df.groupby('case_id',observed=False),miniters=500):
            global output_dir
            output_dir = sub_dir.replace(DIR, "", 1)
            # 输出在~/recorded_trackfiles
            os.makedirs(output_dir,exist_ok=True)

            group.drop(columns='case_id',inplace=True)
            output_file_name = f"{case_name}_{pd.to_numeric(case_id).astype(int)}.csv"  
            output_file_path = os.path.join(output_dir, output_file_name)

            group.to_csv(output_file_path, index=False, compression='infer')  
    else:
        print(f"文件 {csv_file} 中未找到 'case_id' 列。")

if __name__ == '__main__':
    from config import PRE_DATASET_DIR,DIR
    # 获取指定的处理文件夹名称（如无指定则处理所有文件夹）
    target_case_name = 'DR_CHN_Merging_ZS0' or None

    csv_files = []
    
    for root, dirs, files in os.walk(f'{PRE_DATASET_DIR}/recorded_trackfiles'):
        for f in files:
            if f.endswith('.csv'):
                # 如果指定了目标文件夹，只处理该文件夹中的文件
                if target_case_name:
                    if target_case_name in root:
                        csv_files.append(os.path.join(root, f))
                else:
                    csv_files.append(os.path.join(root, f))

    for csv_file in csv_files:
        split_csv(csv_file)
    print(f'完成！输出文件夹在{output_dir}')
