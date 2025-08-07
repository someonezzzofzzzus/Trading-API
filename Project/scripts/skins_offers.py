import requests,json,time

import pandas as pd

public_key = ""
secret_key = ""

file_mwv = pd.read_excel(r"../trading_results/skins_mwv.xlsx", sheet_name="skins_mwv")
mwv_items = file_mwv["Item Name"].tolist()
mwv_itemMWV = file_mwv["Min Week"].tolist()

file_indicators = pd.read_excel(r"../trading_results/skins_history_indicators.xlsx", sheet_name="indicators")
indicators = file_indicators["Min Week / 5"].tolist()

offers_info = {}

def get_highest_target(name):
    
    
    search_name = name.replace(" | ","%20%7C%20").replace(" (","%20%28").replace(")","%29").replace(" ","%20")
    
    market_response = requests.get("https://api.dmarket.com/marketplace-api/v1/market-depth?gameId=a8db&title="+search_name+"&aggregatedData=Orders")
    offers = json.loads(market_response.text)["orders"]
    for target in offers:
        if target.get("attributes") == []:
            return target



def get_offer_from_market(name,limit="1"):
    
    search_name = name.replace(" | ", "%").replace("(","%").replace(" ","%").replace(")","%")
    
    market_repsonse = requests.get("https://api.dmarket.com/exchange/v1/market/items?gameId=a8db&title="+search_name+"&limit="+limit+"&offset=0&orderBy=price&orderDir=asc&currency=USD")
    offer = json.loads(market_repsonse.text)["objects"]
    time.sleep(0.2)
    return offer



def get_ptr20(item,indicator):
    
    response = get_offer_from_market(item,indicator)
    offer_price = response[-1].get("price").get("USD")
    return offer_price
    
    
    

for i in range(len(mwv_items)):
    
    item = mwv_items[i]
    response = get_highest_target(item)
    
    lowest_offer_price = get_offer_from_market(item)[0].get("price").get("USD")
    
    ptr_20 = int(get_ptr20(item,str(indicators[i])))/100
    
    MaxTP = round((float(ptr_20)/1.1/1.1),2)
    
    
    offers_info[item] = [float(response.get("price"))/100, response.get("amount"), float(lowest_offer_price)/100, float(ptr_20), str(MaxTP), mwv_itemMWV[i]] 
    
    
all_data =[]

for skin_name, data in offers_info.items():
    row = {
        'Item Name': skin_name,
        F"Highest Target Price": data[0],
        f"Target amount": data[1],
        f"Lowest Offer Price" : data[2],
        f"PTR 20": data[3],
        f"MaxTP" : data [4],
        f"Min Week" : data[5]
    }
    all_data.append(row)
    
df_all = pd.DataFrame(all_data)

with pd.ExcelWriter(r"../trading_results/skins_Offers.xlsx", engine="openpyxl") as writer:
    
    df_all.to_excel(writer, sheet_name="offers", index=False)
    
    workbook = writer.book
    sheet = workbook["offers"]
    for col in sheet.columns:
        max_length = max(len(str(cell.value)) for cell in col)
        adjusted_width = max_length + 2  # Add some padding to the width
        sheet.column_dimensions[col[0].column_letter].width = adjusted_width
    
    
    
print("Skins_offers been updated")