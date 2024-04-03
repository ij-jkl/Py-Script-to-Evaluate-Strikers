import pandas as pd

# Be careful using more than 150 players since Excel can't hold that much data correctly, that's why im looking forward to implement DataBases to this code
file_path = "strikersRawData.xlsx"
df = pd.read_excel(file_path)

relevant_columns = [
    "Name", "Position", "Club", "Nat", "Height", "Weight", "Preferred Foot", "Age",
    "Apps", "Starts", "Mins", "Gls", "Shots", "ShT", "Ast", "K Pas", "Ps C", "Transfer Value",
    "Drb"  
]

processed_players = []

# Looping by rows
for index, row in df.iterrows():
    # Storing the players Data that we are going to use
    player_data = {
        "Name": row["Name"],
        "Position": row["Position"],
        "Club": row["Club"],
        "Nationality": row["Nat"],
        "Height": row["Height"],
        "Weight": row["Weight"],
        "Preferred Foot": row["Preferred Foot"],
        "Age": row["Age"],
        "Appearances": row["Apps"],
        "Starts": row["Starts"],
        "Minutes Played": row["Mins"],
        "Goals": row["Gls"],
        "Shots": row["Shots"],
        "Shots on Target": row["ShT"],
        "Assists": row["Ast"],
        "Key Passes Created": row["K Pas"],
        "Passes Completed": row["Ps C"],
        "Market Value": row["Transfer Value"],
        "Dribbles Made": row["Drb"]
    }

    # I calculate the stats per 90 minutes since the original excel sometimes gives wrong calculations
    player_data["Goals per 90"] = player_data["Goals"] / (player_data["Minutes Played"] / 90)
    player_data["Shots on Target per 90"] = player_data["Shots on Target"] / (player_data["Minutes Played"] / 90)
    player_data["Assists per 90"] = player_data["Assists"] / (player_data["Minutes Played"] / 90)
    player_data["Key Passes Created per 90"] = player_data["Key Passes Created"] / (player_data["Minutes Played"] / 90)
    player_data["Passes Completed per 90"] = player_data["Passes Completed"] / (player_data["Minutes Played"] / 90)
    player_data["Conversion Rate"] = (player_data["Goals"] / player_data["Shots"]) * 100
    player_data["Shot Accuracy"] = (player_data["Shots on Target"] / player_data["Shots"]) * 100
    player_data["Goal Involvement per 90"] = (player_data["Goals"] + player_data["Assists"]) / (player_data["Minutes Played"] / 90)

    # The total score we are going to be giving, you can change the final value depending on the things you are interested.
    player_data["Rating"] = (
        (player_data["Goals per 90"] * 0.2) +
        (player_data["Assists per 90"] * 0.2) +
        (player_data["Shot Accuracy"] * 0.2) +
        (player_data["Conversion Rate"] * 0.1) +
        (player_data["Key Passes Created per 90"] * 0.15) +
        (player_data["Passes Completed per 90"] * 0.15)
    ) * 10

    # Adding the already processed players to the new data
    processed_players.append(player_data)

# Passing the list to a DataFrame
processed_df = pd.DataFrame(processed_players)

# We use scaling to obtain a score ranging from 1 to 10.
min_rating = processed_df["Rating"].min()
max_rating = processed_df["Rating"].max()
processed_df["Normalized Rating"] = ((processed_df["Rating"] - min_rating) / (max_rating - min_rating)) * 9 + 1

# Converting the DataFrame to the new excel 
# StrikersRating its going to be the new excel file generated
output_file_path = "strikersRating.xlsx"
processed_df.to_excel(output_file_path, index=False)

print(f"Processed player data with normalized ratings has been exported to '{output_file_path}'.")
