import pandas as pd
import requests


MAP_API_KEY = "AIzaSyA-wZq_7NGNrD10INV_PWHC18xgSY9vNGw"
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?"


# Use Google map API to get the lat, lng and formatted by input the rough address
def parse_address(address):
    params = {
        'key': MAP_API_KEY,
        'address': address
    }
    response = requests.get(BASE_URL, params=params).json()
    if response["status"] == "OK":
        lat = float(response["results"][0]["geometry"]["location"]["lat"])
        lng = float(response["results"][0]["geometry"]["location"]["lng"])
        formatted_address = response["results"][0]["formatted_address"]
        print(formatted_address)
        return lat, lng, formatted_address
    else:
        print("error")
        return "empty", "empty", "empty"


# Do the data clean for the machine learning model
def data_clean():
    # Read CSV file
    real_estate_london_df = pd.read_csv("data/rightmove_london.csv")
    real_estate_london_df = real_estate_london_df.drop(columns=["url", "agent_url", "full_postcode", "search_date"])
    real_estate_london_df = real_estate_london_df.drop([real_estate_london_df.columns[0]], axis=1)

    # Drop Nan
    real_estate_london_df = real_estate_london_df.dropna()

    # Deal with the \n and \r in address
    for i in range(0, len(real_estate_london_df)):
        real_estate_london_df.iloc[i]["address"] = real_estate_london_df.iloc[i]["address"].replace('\r', '').replace('\n', '')

    # Add new empty columns lat, lng and formatted
    real_estate_london_df = pd.concat([real_estate_london_df, pd.DataFrame(columns=["lat"])], sort=False)
    real_estate_london_df = pd.concat([real_estate_london_df, pd.DataFrame(columns=["lng"])], sort=False)
    real_estate_london_df = pd.concat([real_estate_london_df, pd.DataFrame(columns=["formatted_address"])], sort=False)
    real_estate_london_df.reset_index(inplace=True)
    # For security avoid abuse the api
    # for i in range(0, len(real_estate_london_df)):
    for i in range(0, 5):
        lat, lng, formatted_address = parse_address(real_estate_london_df.iloc[i]["address"])
        real_estate_london_df.loc[i, ['lat']] = lat
        real_estate_london_df.loc[i, ['lng']] = lng
        real_estate_london_df.loc[i, ['formatted_address']] = formatted_address

    real_estate_london_df = real_estate_london_df.drop(columns=["index"])
    real_estate_london_df.to_csv('rightmove_london_cleaned.csv')


def deal_empty():
    real_estate_london_df = pd.read_csv("data/rightmove_london_cleaned.csv")
    real_estate_london_df = real_estate_london_df[~real_estate_london_df["lat"].isin(["empty"])]
    real_estate_london_df = real_estate_london_df.drop([real_estate_london_df.columns[0]], axis=1)
    real_estate_london_df.to_csv('data/rightmove_london_cleaned.csv')


def deal_type():
    real_estate_london_df = pd.read_csv("data/rightmove_london_cleaned.csv")

    real_estate_london_df.reset_index(inplace=True)
    for i in range(0, len(real_estate_london_df)):
        current_string = real_estate_london_df.iloc[i]["type"]
        if "Studio flat" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Studio flat"
            continue
        elif "Studio apartment" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Studio apartment"
            continue
        elif "flat" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Flat"
            continue
        elif "apartment" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Apartment"
            continue
        elif "terraced house" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Terraced house"
            continue
        elif "maisonette" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Maisonette"
            continue
        elif "semi-detached house" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Semi-detached house"
            continue
        elif "detached house" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Detached house"
            continue
        elif "mews house" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Mews house"
            continue
        elif "end of terrace house" in current_string:
            real_estate_london_df.loc[i, ['type']] = "End of terrace house"
            continue
        elif "penthouse" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Penthouse"
            continue
        elif "duplex" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Duplex"
            continue
        elif "triplex" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Triplex"
            continue
        elif "bungalow" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Bungalow"
            continue
        elif "town house" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Town house"
            continue
        elif "cottage" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Cottage"
            continue
        elif "house" in current_string:
            real_estate_london_df.loc[i, ['type']] = "House"
            continue
        elif "property" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Property"
            continue
        elif "villa" in current_string:
            real_estate_london_df.loc[i, ['type']] = "Villa"
            continue
        else:
            real_estate_london_df.loc[i, ['type']] = "Other"
    # value_count = real_estate_london_df["type"].value_counts()
    real_estate_london_df = real_estate_london_df.drop(columns=["index"])
    real_estate_london_df = real_estate_london_df.drop([real_estate_london_df.columns[0]], axis=1)
    real_estate_london_df.to_csv('data/rightmove_london_cleaned_final.csv')


# Split price into label for classifier
def split_data():
    cleaned_df = pd.read_csv("data/rightmove_london_cleaned_final.csv")
    cleaned_df.reset_index(inplace=True)
    cleaned_df = pd.concat([cleaned_df, pd.DataFrame(columns=["label"])], sort=False)
    for i in range(0, len(cleaned_df)):
        if float(cleaned_df.iloc[i]["price"]) < 200000:
            cleaned_df.loc[i, ['label']] = "Less than 200000 GBP"
            continue
        if 200000 <= float(cleaned_df.iloc[i]["price"]) < 300000:
            cleaned_df.loc[i, ['label']] = "200000 to 300000 GBP"
            continue
        if 300000 <= float(cleaned_df.iloc[i]["price"]) < 350000:
            cleaned_df.loc[i, ['label']] = "300000 to 350000 GBP"
            continue
        if 350000 <= float(cleaned_df.iloc[i]["price"]) < 400000:
            cleaned_df.loc[i, ['label']] = "350000 to 400000 GBP"
            continue
        if 400000 <= float(cleaned_df.iloc[i]["price"]) < 450000:
            cleaned_df.loc[i, ['label']] = "400000 to 450000 GBP"
            continue
        if 450000 <= float(cleaned_df.iloc[i]["price"]) < 500000:
            cleaned_df.loc[i, ['label']] = "450000 to 500000 GBP"
            continue
        if 500000 <= float(cleaned_df.iloc[i]["price"]) < 550000:
            cleaned_df.loc[i, ['label']] = "500000 to 550000 GBP"
            continue
        if 550000 <= float(cleaned_df.iloc[i]["price"]) < 600000:
            cleaned_df.loc[i, ['label']] = "550000 to 600000 GBP"
            continue
        if 600000 <= float(cleaned_df.iloc[i]["price"]) < 650000:
            cleaned_df.loc[i, ['label']] = "600000 to 650000 GBP"
            continue
        if 650000 <= float(cleaned_df.iloc[i]["price"]) < 700000:
            cleaned_df.loc[i, ['label']] = "650000 to 700000 GBP"
            continue
        if 700000 <= float(cleaned_df.iloc[i]["price"]) < 800000:
            cleaned_df.loc[i, ['label']] = "700000 to 800000 GBP"
            continue
        if 800000 <= float(cleaned_df.iloc[i]["price"]) < 900000:
            cleaned_df.loc[i, ['label']] = "800000 to 900000 GBP"
            continue
        if 900000 <= float(cleaned_df.iloc[i]["price"]) < 1000000:
            cleaned_df.loc[i, ['label']] = "900000 to 1000000 GBP"
            continue
        if 1000000 <= float(cleaned_df.iloc[i]["price"]) < 1250000:
            cleaned_df.loc[i, ['label']] = "1000000 to 1250000 GBP"
            continue
        if 1250000 <= float(cleaned_df.iloc[i]["price"]) < 1500000:
            cleaned_df.loc[i, ['label']] = "1250000 to 1500000 GBP"
            continue
        if 1500000 <= float(cleaned_df.iloc[i]["price"]) < 1750000:
            cleaned_df.loc[i, ['label']] = "1500000 to 1750000 GBP"
            continue
        if 1750000 <= float(cleaned_df.iloc[i]["price"]) < 2000000:
            cleaned_df.loc[i, ['label']] = "1750000 to 2000000 GBP"
            continue
        if 2000000 <= float(cleaned_df.iloc[i]["price"]) < 2500000:
            cleaned_df.loc[i, ['label']] = "2000000 to 2500000 GBP"
            continue
        if 2500000 <= float(cleaned_df.iloc[i]["price"]) < 3000000:
            cleaned_df.loc[i, ['label']] = "2500000 to 3000000 GBP"
            continue
        if 3000000 <= float(cleaned_df.iloc[i]["price"]) < 4000000:
            cleaned_df.loc[i, ['label']] = "3000000 to 4000000 GBP"
            continue
        if 4000000 <= float(cleaned_df.iloc[i]["price"]) < 5000000:
            cleaned_df.loc[i, ['label']] = "4000000 to 5000000 GBP"
            continue
        if 5000000 <= float(cleaned_df.iloc[i]["price"]) < 7500000:
            cleaned_df.loc[i, ['label']] = "5000000 to 7500000 GBP"
            continue
        if 7500000 <= float(cleaned_df.iloc[i]["price"]) < 10000000:
            cleaned_df.loc[i, ['label']] = "7500000 to 10000000 GBP"
            continue
        if 10000000 <= float(cleaned_df.iloc[i]["price"]):
            cleaned_df.loc[i, ['label']] = "Higher than 10000000 GBP"
            continue
    cleaned_df = cleaned_df.drop(columns=["index"])
    cleaned_df = cleaned_df.drop([cleaned_df.columns[0]], axis=1)
    cleaned_df.to_csv('data/rightmove_london_labeled.csv')

# data_clean()
# parse_address("Lawrie Park Road, London, SE26")
# deal_empty()
# deal_type()
# split_data()

