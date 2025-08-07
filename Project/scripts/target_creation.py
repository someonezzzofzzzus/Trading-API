import time,requests,json,math

from datetime import datetime

from nacl.bindings import crypto_sign  

from openpyxl import load_workbook 

import pandas as pd

public_key = ""
secret_key = ""

#Read the file which contains nessesary indicators of the wanted item 
file = pd.read_excel(r"../trading_results/skins_Offers.xlsx", sheet_name="offers")
item_names = file["Item Name"].tolist()
HTP_list = file["Highest Target Price"].tolist()
lowest_price_list = file["Lowest Offer Price"].tolist()
ptr_20 = file["PTR 20"].tolist()
MaxTP = file["MaxTP"].tolist()
Min_Week = file["Min Week"].tolist()

#Read the file containing bought Items information: ID/Name/Price/Date
file_bought = pd.read_excel(r"../trading_results/buy_registration.xlsx", sheet_name="Reg")
bought_info = {"ID" : file_bought["Asset ID"].tolist(),"Names" : file_bought["Item Name"].tolist(),"Prices" : file_bought["Price"].tolist(),"Dates" : file_bought["Date"].tolist()}

#QoS
active_sales_sorted = {}

#Qil
inventory_assets ={}

#Total of QoS + Qil
total = {}
    
#Items that have passed 
passed_items = {}


def encryption_get(pKey,sKey,url):
    
    # ---------------------------------------------------------------
    nonce = str(round(datetime.now().timestamp()))  
    api_url_path = url

    #Encryption process for reqests
    method = "GET"
    string_to_sign = method + api_url_path + nonce
    signature_prefix = "dmar ed25519 "
    encoded = string_to_sign.encode('utf-8')
    secret_bytes = bytes.fromhex(sKey)
    signature_bytes = crypto_sign(encoded, bytes.fromhex(sKey))
    signature = signature_bytes[:64].hex()
    headers = {
        "X-Api-Key": pKey,
        "X-Request-Sign": signature_prefix + signature,
        "X-Sign-Date": nonce
    }
    #-------------------------------------------------------------------
    
    return headers

def get_balance(pKey,sKey):
    
    headers = encryption_get(pKey,sKey,"/account/v1/balance")
    
    market_response = json.loads(requests.get("https://api.dmarket.com/account/v1/balance", headers=headers).text)
    return int(market_response.get("usd"))/100



def get_active_offers(pKey,sKey):
    
    headers = encryption_get(pKey,sKey,"/marketplace-api/v1/user-offers?GameID=a8db&Status=OfferStatusDefault&SortType=UserOffersSortTypeDefault&BasicFilters.Currency=USD")
    
    market_response = json.loads(requests.get("https://api.dmarket.com/marketplace-api/v1/user-offers?GameID=a8db&Status=OfferStatusDefault&SortType=UserOffersSortTypeDefault&BasicFilters.Currency=USD",headers=headers).text)
    return market_response["Items"]


def get_inventory_info(pKey,sKey,name):
    
    search_name = name.replace(" | ", " ").replace("(","").replace(" ","%20").replace(")","")

    headers = encryption_get(pKey,sKey,"/marketplace-api/v1/user-inventory?GameID=a8db&BasicFilters.Title="+search_name+"&BasicFilters.InMarket=true&SortType=UserInventorySortTypeDefault&Presentation=InventoryPresentationSimple")

    market_response = json.loads(requests.get("https://api.dmarket.com/marketplace-api/v1/user-inventory?GameID=a8db&BasicFilters.Title="+search_name+"&BasicFilters.InMarket=true&SortType=UserInventorySortTypeDefault&Presentation=InventoryPresentationSimple",headers=headers).text)
    return market_response


def calculating_APP(buy_history, given_name):
    app = 0
    index_record = []
    for index,item_name in enumerate(buy_history.get("Names")):
        if item_name == given_name:
            index_record.append(index)
    
    for ind in index_record:
        app += buy_history.get("Prices")[ind]
        
    return app



def build_target_field_tested(offer, P_Q_list):
    response = {"targets": [
        {"amount": P_Q_list[1], "gameId": offer["gameId"], "price": {"amount": str(P_Q_list[0]*100), "currency": "USD"},
         "attributes": {"gameId": offer["gameId"],
                        "categoryPath": offer["extra"]["categoryPath"],
                        "title": offer["title"],
                        "name": offer["title"],
                        "image": offer["image"],
                        "floatPartValue": "FT-0"}}
    ]}

    return response

def build_target_fn_mw(offer, P_Q_list):
    response = {"targets": [
        {"amount": P_Q_list[1], "gameId": offer["gameId"], "price": {"amount": str(P_Q_list[0]*100), "currency": "USD"},
         "attributes": {"gameId": offer["gameId"],
                        "categoryPath": offer["extra"]["categoryPath"],
                        "title": offer["title"],
                        "name": offer["title"],
                        "image": offer["image"]}}
                                                                                ]}
    return response
    

    
def post_headers(body,pKey,sKey):   
     
    nonce = str(round(datetime.now().timestamp()))
    api_url_path = "/exchange/v1/target/create"
    method = "POST"
    string_to_sign = method + api_url_path + json.dumps(body) + nonce
    signature_prefix = "dmar ed25519 "
    encoded = string_to_sign.encode('utf-8')
    secret_bytes = bytes.fromhex(sKey)
    signature_bytes = crypto_sign(encoded, bytes.fromhex(sKey))
    signature = signature_bytes[:64].hex()
    headers = {
        "X-Api-Key": pKey,
        "X-Request-Sign": signature_prefix + signature,
        "X-Sign-Date": nonce
    }
    return headers   

#User Balance USD
# balance = get_balance(public_key,secret_key)
balance  = 100

active_sales = get_active_offers(public_key,secret_key)



# Get active user's sales
for position in active_sales:
    title = position.get("Title")
    if title in active_sales_sorted.keys():
        active_sales_sorted.update({title:active_sales_sorted.get(title)})
    else:
        active_sales_sorted[title] = 1

#Get user's inventory information
for item in item_names:
    inventory_response = get_inventory_info(public_key,secret_key,item)
    inventory_assets[item] = len(inventory_response["Items"])

#Put together active user's sales & inventory info
for item in item_names:
    if active_sales_sorted.get(item) == None:
        item_1 = 0
    else:
        item_1 = active_sales_sorted.get(item)
    if inventory_assets.get(item) == []:
        item_2 = 0
    else:
        item_2 = inventory_assets.get(item)
    total[item] =  item_1 + item_2


    
            
    
    



for i in range(len(item_names)):
    # Target Preliminary Coniditions Check for ---> item_names[i]
    if MaxTP[i]>HTP_list[i]:
        if balance > (HTP_list[i]+0.01):
            if total[item_names[i]] < Min_Week[i]/10:
                app = calculating_APP(bought_info,item_names[i])
                ta = balance + (app * total[item_names[i]])
                if (app * total[item_names[i]]) < ta/40:
                    passed_items[item_names[i]] = [round((HTP_list[i]+0.01),2) , math.floor((ta/40 - app*(total[item_names[i]]))/(HTP_list[i]+0.01))]
                          
                    
print(passed_items)
                    
                    
                    
#Start creating targets
for skin_name,data in passed_items.items():
    
    if skin_name.find("(Field-Tested)") != -1:
        
        print("CREATING")
        search_name = skin_name.replace(" | ", "%").replace("(","%").replace(" ","%").replace(")","%")
        
        market_response = requests.get("https://api.dmarket.com/exchange/v1/market/items?gameId=a8db&title="+search_name+"&limit=1&offset=0&orderBy=price&orderDir=asc&currency=USD")
        offer = json.loads(market_response.text)["objects"]
        get_offer = offer[0]
        
        target_body = build_target_field_tested(get_offer,data)
        headers = post_headers(target_body,public_key,secret_key)
        
        resp = requests.post("https://api.dmarket.com/exchange/v1/target/create", json=target_body, headers=headers)
        print(resp)
        
        print(f"Target for {search_name.replace("%"," ")} has been created")
        
    else:
        print(2)
        search_name = skin_name.replace(" | ", "%").replace("(","%").replace(" ","%").replace(")","%")
        
        market_response = requests.get("https://api.dmarket.com/exchange/v1/market/items?gameId=a8db&title="+search_name+"&limit=1&offset=0&orderBy=price&orderDir=asc&currency=USD")
        offer = json.loads(market_response.text)["objects"]
        get_offer = offer[0]
        
        target_body = build_target_fn_mw(get_offer,data)
        headers = post_headers(target_body,public_key,secret_key)
        
        resp = requests.post("https://api.dmarket.com/exchange/v1/target/create", json=target_body, headers=headers)
        
        print(resp)
        print(f"Target for {search_name.replace("%"," ")} has been created")
        
        



