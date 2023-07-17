'''
MOVE THIS SOMEWHERE ELSE
This folder should only contain things that are directly used and
related to mantaray_control.

Author: William Y.
'''

import pandas as pd
import numpy as np
import os

def parse_data():
    SHEET_NAMES = ["10 V", "12 V", "14 V", "16 V", "18 V", "20 V"]
    DATA_DIR = os.path.join(os.getcwd(), "data", "t200_data")
    DATA_PATH = os.path.join(DATA_DIR, "t200_data.xlsx")
    columns = {"pwm": " PWM (µs)", "rpm":" RPM", "cur":" Current (A)", "volt":" Voltage (V)","pow":" Power (W)", "force":" Force (Kg f)", "eff":" Efficiency (g/W)"}
    num_columns = len(columns)

    useful_cols = [[columns["force"], columns["pwm"]],[columns["force"], columns["cur"]],[columns["force"], columns["pow"]],[columns["force"], columns["eff"]],]
    
    for sheet in SHEET_NAMES:
        current_dir = os.path.join(DATA_DIR, sheet)
        data = pd.read_excel(
            DATA_PATH, sheet_name=sheet,
            engine='openpyxl',
        )
        for cols in useful_cols:
            df = data.filter(items=cols)
            key0 = list(filter(lambda x: columns[x] == cols[0], columns))[0]
            key1 = list(filter(lambda x: columns[x] == cols[1], columns))[0]
            
            file_path = os.path.join(current_dir, f"{key0}_{key1}.csv")

            df.to_csv(file_path)
            # print(f"This would be in a file called {file_name}.csv and at location: {current_dir}")

def print_csv(file_path, col):
    data = pd.read_csv(file_path)
    data = data.values[:,col]
    for val in data:
        print(val, end=" ")
    print("")

if __name__ == "__main__":
    DATA_DIR = os.path.join(os.getcwd(), "data", "t200_data")
    file_path = os.path.join(DATA_DIR, "20 V", "force_pwm.csv")
    print_csv(file_path, 1)
    print_csv(file_path, 2)