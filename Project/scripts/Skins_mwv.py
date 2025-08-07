from openpyxl import load_workbook 

import pandas as pd

rootApiUrl = "https://api.dmarket.com"

sheets_name = ["skins_mwv","removed_added"]

file = pd.read_excel(r"../trading_results/skins_weekly_history.xlsx", sheet_name="skins_weekly_volumes")
skins_names = file["Item Name"].tolist()

week1 = file.iloc[:,1].to_list()
week2 = file.iloc[:,2].to_list()
week3 = file.iloc[:,3].to_list()
week4 = file.iloc[:,4].to_list()


weeks_volumes = {}
removed_items = {}


def check(item_history):
    for week in item_history:
        if week > 30:
            pass
        else:
            removed = weeks_volumes.popitem()
            removed_items[removed[0]]= removed[1]
            return False
    
    return True
        
        
for item in skins_names:
    
    item_week_list = [week1.pop(0),week2.pop(0),week3.pop(0),week4.pop(0)]
    
    copy_list = item_week_list.copy()
    copy_list.sort()
    
    item_week_list.append(copy_list[0])
    
    weeks_volumes[item] = item_week_list
    
    if check(weeks_volumes[item]):
        pass
   
#-----------------------------------------------------------   

all_data =[]   
   
for name,data in weeks_volumes.items():
    row = {
            "Item Name" : name,
            "Week 01": data[0],
            "Week 02": data[1],
            "Week 03": data[2],
            "Week 04": data[3],
            "Min Week": data [4]
    }
    all_data.append(row)

df_all = pd.DataFrame(all_data)     
        
#-----------------------------------------
all_data_2 =[]   
   
for name,data in removed_items.items():
    row = {
            "Item Name" : name,
            "Week 01": data[0],
            "Week 02": data[1],
            "Week 03": data[2],
            "Week 04": data[3]
    }
    all_data_2.append(row)

df_all_2 = pd.DataFrame(all_data_2) 

with pd.ExcelWriter(r"../trading_results/skins_mwv.xlsx", engine="openpyxl") as writer:
    
    df_all.to_excel(writer, sheet_name="skins_mwv", index=False)
    
    df_all_2.to_excel(writer, sheet_name="removed_added", index=False)
    
    workbook = writer.book
    for sheet in ["skins_mwv","removed_added"]:
        sheet = workbook[sheet]
        for col in sheet.columns:
            max_length = max(len(str(cell.value)) for cell in col)
            adjusted_width = max_length + 2  # Add some padding to the width
            sheet.column_dimensions[col[0].column_letter].width = adjusted_width    
        
    
    
    
    