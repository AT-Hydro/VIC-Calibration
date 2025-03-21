import sys
import pandas as pd
import os
from datetime import datetime, timedelta
from DAFunctions import glob_parm_set 


idx = int(sys.argv[1])
gauges =  pd.read_csv("Gauges2.csv")
gauge   = gauges.gauge_id[idx]
base_folder   = os.getcwd()
DA_path       = os.path.join(base_folder, "DA")
Master_folder = os.path.join(DA_path, f"Ensemble_{gauge}")
start_date  = datetime(2013,10,1)
current_date= start_date
end_date    = datetime(2018,10,1)
while current_date <= end_date:
    for ens in range(100):
        gaugepath     = os.path.join(Master_folder ,  f"Ens_{ens}")
        glob_parm_set(gaugepath, start_date= current_date, read_state = True)
    current_date += timedelta(days=1)
    