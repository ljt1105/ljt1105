import sys

sys.path.append(r'C:/PythonProjects/ljt1105/TradeVerification/modules')

import read_files
import refine_data
import reconcile_data

import numpy as np
import pandas as pd
from tabulate import tabulate
import datetime
import time



oms_df, trader_df, td, td_tr = read_files.read_df_files()
time.sleep(1)
trader_df3, oms_df4 = refine_data.refine_df(oms_df, trader_df, td)
time.sleep(1)
difference_df = reconcile_data.reconcile_data(trader_df3, oms_df4, td)