from commission import Merge
import pandas as pd
import os

UPLOAD_FOLDER =  r".\uploads"

# import warnings
# warnings.simplefilter("ignore")
# wb = load_workbook("./uploads/commission_statement_704685_2020-10-01.xlsx")
# warnings.simplefilter("default")

# merge = Merge()
# merge.begin(3)

# df = pd.read_excel('./uploads/oct 2020.xlsx', engine='openpyxl')
# df = pd.read_excel('./uploads/july 2020 (1).xlsx', sheet_name='Commission Transactions', engine = 'openpyxl')
# print(df.head())

filelist = [ f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".xlsx") ]
for f in filelist:
    os.remove(os.path.join(UPLOAD_FOLDER, f))