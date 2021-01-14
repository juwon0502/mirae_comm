import pandas as pd
import numpy as np
import os
# COL_NAMES = ['Name', 'Tran Type' , 'Effective Date' ,'Plan Name']

# Q1 = 1
# Q2 = 2
# Q3 = 3
# Q4 = 4


class Merge(object):

    def begin(self, quarter, mon1, mon2, mon3):
        # quarter = int(input("What quarter?\n1. Jan-Mar\n2. Apr-Jun\n3. Jul-Sep\n4. Oct-Dec\n")) 
        COL_NAMES = ['Name', 'Tran Type' , 'Effective Date' ,'Plan Name']
        YEAR = '2020'
        if quarter == 1:
            month_name = ['JAN', 'FEB', 'MAR']     
        if quarter == 2:
            month_name = ['APR', 'MAY', 'JUN']      
        if quarter == 3:
            month_name = ['JUL', 'AUG', 'SEP']     
        if quarter == 4:
            month_name = ['OCT', 'NOV', 'DEC']
            
        new_col = []
        all_col = []
        all_col = COL_NAMES

        for months in month_name:
            all_col.append(months + " Income")
            new_col.append(months + " Income")
            all_col.append(months + " Chargeback")
            new_col.append(months + " Chargeback")
        all_col.append('Total')
        new_col.append('Total')
                
        date_type = pd.DataFrame(columns = [all_col])

        mon1 = self.fill_df(month_name[0], mon1, all_col)
        mon2 = self.fill_df(month_name[1], mon2, all_col)
        mon3 = self.fill_df(month_name[2], mon3, all_col)

        date_type = pd.concat([mon1] + [mon2] + [mon3])
        date_type['Total'] = date_type.iloc[:,4:10].sum(axis = 1)

        agent_per = pd.read_csv('agent_per.csv')
        agent_per = agent_per.drop(columns = ('Unnamed: 0'))
        agent_per = agent_per.set_index('Cust')
        agent_dict = agent_per.to_dict()

        values = date_type.groupby('Name').sum()
        date_type.drop(date_type.columns.difference(['Name', 'Tran Type' , 'Effective Date' ,'Plan Name']), 1, inplace=True)
        date_type = date_type.drop_duplicates('Name')
        cust_dict = date_type.to_dict()
        money_dict = values.to_dict()
        
        df = pd.DataFrame(columns = COL_NAMES)
        df = df.iloc[0:0]

        for index in cust_dict['Name']:
            key = cust_dict['Name'][index]
            try:
                mid_init = key.split(' ')[2]
                if len(mid_init) == 1:
                    agent_key = key[:-2]
                if key.split(' ')[2] == " ":
                    key = key.split(' ')[0:2] + key.split(' ')[3:]
                    agent_key = key
            except:
                agent_key = key
            tt = cust_dict['Tran Type'][index]
            ed = cust_dict['Effective Date'][index]
            pn = cust_dict['Plan Name'][index]
            mon1_income = money_dict[new_col[0]][key]
            mon2_income = money_dict[new_col[2]][key]
            mon3_income = money_dict[new_col[4]][key]
            mon1_cb = money_dict[new_col[1]][key]
            mon2_cb = money_dict[new_col[3]][key]
            mon3_cb = money_dict[new_col[5]][key]
            total_comm = money_dict['Total'][key]
            try:
                agent_name = agent_dict['Agent'][key]
                per = agent_dict['Percentage'][key]
                per_comm = float(total_comm) * float(per)/100
            except:
                try:
                    agent_name = agent_dict['Agent'][agent_key]           
                    per = agent_dict['Percentage'][agent_key]
                    per_comm = float(total_comm) * float(per)/100
                except:
                    agent_name = np.nan
                    per = np.nan
                    per_comm = np.nan
            df = df.append({'Name':key, 'Agent':agent_name, 'Per %':per, 'Tran Type':tt, 'Effective Date':ed, 'Plan Name':pn,new_col[0]:mon1_income,\
                new_col[1]:mon1_cb, new_col[2]:mon2_income, new_col[3]:mon2_cb, new_col[4]:mon3_income, new_col[5]:mon3_cb, 'Total':total_comm,\
                    'Percent Commission':per_comm}, ignore_index = True)

        df = df.sort_values('Name')
        cols = list(df.columns.values)
        df = df[[cols[0]] + cols[11:13] + cols[1:11] + [cols[13]]]
            # df.head()

        df.to_excel(os.path.join("uploads", 'Q' + str(quarter) + '-' + YEAR +'-comm.xlsx'))

    def fill_df(self, month, data, useful):
        data['Name'] = data['Member Name'].str.strip('.')   
        data['Tran Type'] = data['Commission Action']
        data['Effective Date'] = data['Original Effective Date']
        data['Plan Name'] = data['Plan Type']
        data[month + ' Income'] = np.where(data['Commission'] + data['UAD Activity'] > -0.001, data['Commission'] + data['UAD Activity'], 0)
        data[month + ' Chargeback'] = np.where(data['Commission'] + data['UAD Activity'] < 0, data['Commission'] + data['UAD Activity'], 0)
        data.drop(data.columns.difference(useful), 1, inplace=True)
        data = data.loc[data['Tran Type'].str[0:2] != "HA"]
        return data

# def main():
#     merge = Merge()
#     merge.begin(3)
# main()
