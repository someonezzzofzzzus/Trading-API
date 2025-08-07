from openpyxl import load_workbook 

import pandas as pd

file = pd.read_excel(r"../trading_results/skins_mwv.xlsx", sheet_name="skins_mwv")
skins_name = file["Item Name"].tolist()

min_week = file["Min Week"].tolist()

indicators = {}

for i in range(len(skins_name)):
    indicators[skins_name[i]] = [min_week[i],round(min_week[i]/5)]
  
  
  
    
all_data =[]   
   
for name,data in indicators.items():
    row = {
            "Item Name" : name,
            "Min Week": data[0],
            "Min Week / 5": data[1]
    }
    all_data.append(row)

df_all = pd.DataFrame(all_data) 

with pd.ExcelWriter(r"../trading_results/skins_history_indicators.xlsx", engine="openpyxl") as writer:
    
    df_all.to_excel(writer, sheet_name="indicators", index=False)
