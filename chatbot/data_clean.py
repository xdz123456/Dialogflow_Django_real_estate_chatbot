import pandas as pd
import requests

MAP_API_KEY = ""
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
    real_estate_london_df = pd.read_csv("rightmove_london.csv")
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
    for i in range(0, len(real_estate_london_df)):
        lat, lng, formatted_address = parse_address(real_estate_london_df.iloc[i]["address"])
        real_estate_london_df.loc[i, ['lat']] = lat
        real_estate_london_df.loc[i, ['lng']] = lng
        real_estate_london_df.loc[i, ['formatted_address']] = formatted_address

    real_estate_london_df = real_estate_london_df.drop(columns=["index"])
    real_estate_london_df.to_csv('rightmove_london_cleaned.csv')


def deal_empty():
    real_estate_london_df = pd.read_csv("rightmove_london_cleaned.csv")
    real_estate_london_df = real_estate_london_df[~real_estate_london_df["lat"].isin(["empty"])]
    real_estate_london_df = real_estate_london_df.drop([real_estate_london_df.columns[0]], axis=1)
    real_estate_london_df.to_csv('rightmove_london_cleaned.csv')


def deal_type():
    real_estate_london_df = pd.read_csv("rightmove_london_cleaned.csv")

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

    real_estate_london_df.to_csv('rightmove_london_cleaned_final.csv')


# data_clean()
# parse_address("Lawrie Park Road, London, SE26")
# deal_empty()
# deal_type()

