import pandas as pd
import json
import os
import botometer


raw_dataset_dir = "./raw_data/"
output_dir = "./dataset/"


# utils

def writeTofile(file_data, file_name):
    print("File written successfully!")
    with open(file_name, 'w') as outfile:
        data = json.dumps(file_data,separators=(',', ':'))
        outfile.write(data)

def classifyBot(botometer_data):
    classification = "blank"
    baseline_score = 0;
    classifications = ["astroturf","fake_follower","financial","other","self_declared","spammer"]
    
    if "display_scores" in botometer_data:

        for bot_type in classifications:
            bx = botometer_data["display_scores"]["english"][bot_type]
            if baseline_score < bx:
                classification = bot_type
    
    return classification

# botometer API

rapidapi_key = "d9fa466601msh8b4786e05eda027p1d321bjsnef6f552e3278"
twitter_app_auth = {
    'consumer_key': '8d2J3nLhNpWyBlizFtidvoQyB',
    'consumer_secret': 'i3diRmOQVT74wWSPeRatDvEoijnTfNeRrjOUOXmNWl8T6815SY',
    'access_token': '1418799546583429122-83GskPvSAyL6y676F23nnedvoAl0jd',
    'access_token_secret': 'gx9ssHgKhi34P5PTCEGa2uworOs0DU2ZkZ2fT4aO5ugpZ'
  }

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)    


# dataset files

raw_data = os.listdir(raw_dataset_dir)

# full data
full_data = pd.DataFrame()


print("====================================")
print("Correlating Hoaxy CSV Data data...")
print("====================================")

# merge all data

for datafile in raw_data:
    print("Prcessing ===> ",datafile)
    csv_to_df = pd.read_csv(raw_dataset_dir+datafile)
    full_data = pd.concat([full_data,csv_to_df])


# begin preprocessing


# remove empty columns
full_data = full_data.dropna(how='all' , axis=1, inplace=False)
# remove duplicate rows
full_data = full_data.drop_duplicates(subset=["from_user_id","to_user_id"])

# data botometer type columns
full_data.insert(0, "from_user_bot_type", "", False)
full_data.insert(0, "to_user_bot_type", "", False)

# add columns for user types
full_data.insert(0,"from_user_type","human", False)
full_data.insert(0,"to_user_type","human", False)


# TODO: classify which are bots and which are not bots & bot type with botometer

all_bots = {}

for index, row in full_data.iterrows():
    
    if  row["from_user_botscore"] >= 0.43:
        full_data.at[index,"from_user_type"] = "bot"
        
        if "@"+row["from_user_screen_name"] not in all_bots:
            all_bots["@"+row["from_user_screen_name"]] = "blank"


    if  row["to_user_botscore"] >= 0.43:
        full_data.at[index,"to_user_type"] = "bot"  
        if "@"+row["to_user_screen_name"] not in all_bots:
            all_bots["@"+row["to_user_screen_name"]] = "blank"
        

# loop through all bots for botometer classification

for i,bot in enumerate(all_bots):

    try:
        result = bom.check_account(bot)
        bc = classifyBot(result)
        all_bots[bot] = bc
        print(bot,"===>",bc)
        print(i,"/",len(all_bots))
    except:
        print("Protected tweeter account, skipping:", bot)
        all_bots[bot] = "private_account"

writeTofile(all_bots,"bots_data.json")

for index, row in full_data.iterrows():

    to_user_name = "@"+row["to_user_screen_name"]
    from_user_name = "@"+row["from_user_screen_name"]

    if  from_user_name in all_bots:
        full_data.at[index,"from_user_bot_type"] = all_bots[from_user_name] 

    if  to_user_name in all_bots:
        full_data.at[index,"to_user_bot_type"] = all_bots[to_user_name] 





# output correlated data
print(full_data)
print("=============================")
print("Data preprocessing complete!")
full_data.to_csv(output_dir+"core_data.csv")
