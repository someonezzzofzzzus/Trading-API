import time,requests,json 

from openpyxl import load_workbook 

import pandas as pd

from nacl.bindings import crypto_sign  

import Skins_names as sn

# Subsitute for account's keys
public_key = "6a3ad4d139a43678628849a6278616bc19bc2e1f41c145c53f078ae8d884716a"
secret_key = "015ce764035d8d8e544b845a23ba70ab1a11d944891f160586c4252d3996f3e96a3ad4d139a43678628849a6278616bc19bc2e1f41c145c53f078ae8d884716a"

#Exteriors of skins
exteriors = ["%Factory%New%","%Minimal%Wear%","%Field-Tested%"]

rootApiUrl = "https://api.dmarket.com"

sheet1_name = []
sheet1_price= []

sheet2_name = []
sheet2_price= []

sheets_data={}
            
            
def get_offer_from_market(name,limits="1"):
    
    try:
        #Get request without headers, set to find cheapest offer on the market 
        market_response = requests.get(rootApiUrl + "/exchange/v1/market/items?gameId=a8db&title="+name+"&limit="+limits+"&offset=0&orderBy=price&orderDir=asc&currency=USD")
        offers = json.loads(market_response.text)["objects"]
        print(offers[0])
        time.sleep(0.1)
        
        #If offer was not found, it return String
        if len(offers) <= 0:
            return f'Item {name} has not been found'
        return offers[0]
    finally:
        pass  


for name in sn.skins_name:
    
    search_name = name.replace(" | ", "%").replace("(","%").replace(" ","%").replace(")","%")

    response = get_offer_from_market(search_name)
    
    if type(response) == str:
        pass
    elif response == None:
        pass
    else:
        price = response.get("price").get("USD")
        
        if 50<int(price)<500:
            sheet2_name.append(response.get("title"))
            if len(price) < 3:
                sheet2_price.append("0." + price)
            else:
                sheet2_price.append(price[:-2]+"."+price[-2:])
            
        sheet1_name.append(response.get("title"))
        if len(price) < 3:
            sheet1_price.append("0." + price)
        else:
            sheet1_price.append(price[:-2]+"."+price[-2:])
            
                
results = {"type_&_wear":[sheet1_name,sheet1_price],"ref_price":[sheet2_name,sheet2_price]}




with pd.ExcelWriter(r"../trading_results/Skins.xlsx",engine="openpyxl") as writer:
    for sheet_name,data in results.items():
        
        df = pd.DataFrame({
            'Item Name' : data[0],
            'Price' : data[1]    
        })
                
        df.to_excel(writer,sheet_name=sheet_name,index=False)
    
        
    
        # Access the openpyxl workbook and sheet
        workbook = writer.book
        sheet = workbook[sheet_name]

        for col in sheet.columns:
            max_length = max(len(str(cell.value)) for cell in col)
            adjusted_width = max_length + 2  # Add some padding to the width
            sheet.column_dimensions[col[0].column_letter].width = adjusted_width
            

        
        

        
            

            
