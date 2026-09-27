import requests
import pandas as pd

url = "https://fantasy.premierleague.com/api/bootstrap-static/"   #this is the URL we need to get the data from
response = requests.get(url)  #we asked URL for its data and stored it in response
# print(response.status_code) this is to see if the request was sucessful, 200 indiciates yes
data = response.json() #converts the recieved code into a JSON file
# print(data.keys()) what types of data FPL sent me
players = pd.DataFrame(data["elements"]) #creating a Pandas Dataframe of all players and their data
#print(players)
#print(players.columns.tolist()) all the players and data 
# print(players[["web_name", "now_cost", "total_points", "goals_scored", "assists"]].head(10)), this prints the first 10 players attributes


# player_id = players.iloc[0]["id"] #gets each players ID
# url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/" 
# response = requests.get(url)
# player_data = response.json()
# print(player_data.keys()) 
# history = pd.DataFrame(player_data["history"])
# print(history.head())
# print(history.columns.tolist())
#so far we got player 0s (Rayas) data and we are looking at his past gameweeks
all_history = []
for index, player in players.iterrows():

    player_id = player["id"]

    url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"

    response = requests.get(url)

    player_data = response.json()

    print(player["web_name"], len(player_data["history"]))
    all_history.append(player_data["history"])
    print(len(all_history))

history_df = pd.concat([pd.DataFrame(h) for h in all_history], ignore_index=True) #creates a data frame with each players GW accompanied with stats

print(history_df.shape) #tells us how many rows and columns

history_df.to_csv("fpl_history.csv", index=False)

#so rn we have the 26/27 seasons data, now for the previous season


