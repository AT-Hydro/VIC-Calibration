import pandas as pd
import os
import shutil
import glob
import sys

gauges =  pd.read_csv("Gauges2.csv")

Master_folder_path =  os.path.join(os.getcwd(), "DA", f"Ensemble_{gauges['gauge_id'].iat[int(sys.argv[1])]}")
if not os.path.exists(Master_folder_path):
    os.makedirs(Master_folder_path)

for ens in range(100):

    sub_ens = os.path.join(Master_folder_path, f"Ens_{ens}")
    if not os.path.exists(sub_ens):
        os.makedirs(sub_ens)
    
    src  = os.path.join(os.getcwd(), "CONUS", str(gauges['gauge_id'].iat[int(sys.argv[1])]).zfill(8))
    shutil.copytree(src, sub_ens, dirs_exist_ok=True)