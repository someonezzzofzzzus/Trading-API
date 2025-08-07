import time,requests,json 

from datetime import datetime, timedelta

from openpyxl import load_workbook 

from nacl.bindings import crypto_sign  

import pandas as pd

file = pd.read_excel(r"../trading_results/Skins.xlsx", sheet_name="ref_price")
new_skins_names = file["Item Name"].tolist()

rootApiUrl = "https://api.dmarket.com"

history = pd.read_excel(r"../trading_results/skins_weekly_history.xlsx", sheet_name="skins_weekly_volumes")
old_nm = history["Item Name"].tolist()
old_w1 = history["Week 01"].tolist()
old_w2 = history["Week 02"].tolist()
old_w3 = history["Week 03"].tolist()
old_w4 = history["Week 04"].tolist()
checkDT = history["Last Change"].tolist()[-1]




# Subsitute for account's keys
public_key = "6a3ad4d139a43678628849a6278616bc19bc2e1f41c145c53f078ae8d884716a"
secret_key = "015ce764035d8d8e544b845a23ba70ab1a11d944891f160586c4252d3996f3e96a3ad4d139a43678628849a6278616bc19bc2e1f41c145c53f078ae8d884716a"


#for all history
total_info_of_sales = {}


# for passed offers history
all_item_history = {}
passed_offers = {}

def get_sales_history(name):
    #function requesting the trading history with limits of 500
            
    # ---------------------------------------------------------------
    nonce = str(round(datetime.now().timestamp()))
    api_url_path = "/trade-aggregator/v1/last-sales?gameId=a8db&title="+name+"&limit=500"

    #Encryption process for reqests
    method = "GET"
    string_to_sign = method + api_url_path + nonce
    signature_prefix = "dmar ed25519 "
    encoded = string_to_sign.encode('utf-8')
    secret_bytes = bytes.fromhex(secret_key)
    signature_bytes = crypto_sign(encoded, bytes.fromhex(secret_key))
    signature = signature_bytes[:64].hex()
    headers = {
        "X-Api-Key": public_key,
        "X-Request-Sign": signature_prefix + signature,
        "X-Sign-Date": nonce
    }
    #-------------------------------------------------------------------
    
    
    
    market_response = json.loads(requests.get(rootApiUrl + api_url_path, headers=headers).text)
    return market_response.get('sales')



def get_latest_sunday(dt):
    days_to_subtract = (dt.weekday() + 1) % 7  # Sunday is 6, Monday is 0
    last_sunday = dt - timedelta(days=days_to_subtract)
    
    # Set the time to 23:59:59
    last_sunday_at_235959 = last_sunday.replace(hour=23, minute=59, second=59, microsecond=0)
    
    return last_sunday_at_235959


last_sunday = get_latest_sunday(datetime.now())

def week_pass(date):
    
    date1 = datetime.strptime(date,"%d.%m.%Y" )
    
    
    
    if datetime.now() > date1 + timedelta(weeks=1):
        return True
    else:
        return False
    
    

def get_weeks_count(item_history=list()):  
    
    items_per_week_count = 0
    
    for sale in item_history:
        
        sale_date = datetime.fromtimestamp(int(sale.get("date")))

        if sale_date > (last_sunday - timedelta(weeks=1)):

            if sale_date < last_sunday:
                items_per_week_count += 1                
        else:
            pass
    
    
    return items_per_week_count


    
    
def sorting_sales_info(item_history):
    price_list=[]
    date_list=[]
    offer_type=[]
    for item in item_history:
        price_list.append(item.get("price"))
        date_list.append(datetime.fromtimestamp(int(item.get("date"))))
        offer_type.append(item.get("txOperationType"))
    
    return [price_list,date_list,offer_type]






if (week_pass(checkDT)):
    for item in new_skins_names:

            trading_history_list = get_sales_history(item.replace(" | ","%20%7C%20").replace(" (","%20%28").replace(")","%29").replace(" ","%20"))

            # Dictionary to record history of every item history (MWV CHECKS NOT INCLUDED)
            total_info_of_sales[item] = sorting_sales_info(trading_history_list)

            # Check the item history on MWV (MWV CHECKS INCLUDING)
            result = get_weeks_count(trading_history_list)

            if type(result) == int:
                all_item_history[item] = [result,old_w1[new_skins_names.index(item)],old_w2[new_skins_names.index(item)],old_w3[new_skins_names.index(item)]]
                print(all_item_history)
                
    
    
    
    with pd.ExcelWriter(r"../trading_results/skins_weekly_history.xlsx", engine="openpyxl") as writer:
    
    # -- passed offers contructor for excel    
        all_data = []

        for skin_name, data in all_item_history.items():
            row = {
                'Item Name': skin_name,
                F"Week 01": data[0],
                f"Week 02": data[1],
                f"Week 03" : data[2],
                f"Week 04": data[3]
            }
            all_data.append(row)    
            
            
        mark = {f"Last Change" : last_sunday.strftime("%d.%m.%Y")}
        all_data.append(mark)
        
        
        df_all = pd.DataFrame(all_data)
        # --- finish contructing

        df_all.to_excel(writer, sheet_name="skins_weekly_volumes", index=False)

        for skin_name,data in total_info_of_sales.items():
            # Create a DataFrame for each sheet
            df = pd.DataFrame({
                'Date&Time': data[1],
                'OperationType': data[2],
                'Price': data[0]
            })

            # Write the DataFrame to the sheet
            df.to_excel(writer,sheet_name=skin_name,index=False)

            workbook = writer.book
            sheet = workbook[skin_name]

            for col in sheet.columns:
                max_length = max(len(str(cell.value)) for cell in col)
                adjusted_width = max_length + 2  # Add some padding to the width
                sheet.column_dimensions[col[0].column_letter].width = adjusted_width


        workbook = writer.book
        sheet = workbook["skins_weekly_volumes"]

        for col in sheet.columns:
            max_length = max(len(str(cell.value)) for cell in col)
            adjusted_width = max_length + 2  # Add some padding to the width
            sheet.column_dimensions[col[0].column_letter].width = adjusted_width
        
        
        print("ITEMS HISTORY HAS BEEN UPDATED")
        
        
        
        
        
        
        
        
else:
    print(f"Too early!!!\n RUN this code on Monday {get_latest_sunday(datetime.now() + timedelta(weeks=1))}")








    
        
        





