import streamlit as st
import requests
from datetime import datetime


def run():
    st.title("Lookup Teams by Date")
    #use calender for user to set date
    date_input = st.date_input("Please Select Game Date", value=datetime.today())

    if st.button("Get Teams"):
        date = datetime.strptime(str(date_input), '%Y-%m-%d')
        game_pks = get_game_pks(date)
    
        if game_pks:
            #get team info for the retrieved game PKs
            teams_info = []
            #initialize teams_info list
            for game_pk in game_pks:
                home_team, away_team = get_game_details(game_pk)
                if home_team and away_team:
                    #append list if results are found
                    teams_info.append(f"Game PK {game_pk}, HOME - {home_team}, AWAY - {away_team}")
                else:
                    #append list if results are not found
                    teams_info.append(f"Game PK {game_pk}: No game found or error when attempting to get details.")
    
            st.subheader("Teams Information:")
            for info in teams_info:
                st.write(info)
        else:
            st.write(f"No games found for {date.strftime('%Y-%m-%d')}.")
    

#function to get gamePK's given a specific date
def get_game_pks(date):
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date.strftime('%Y-%m-%d')}"
    response = requests.get(url)
    #200 means successful response
    if response.status_code == 200:
        games = response.json().get('dates', [])
        game_pks = []
        #initialize game_pks list
        for date_info in games:
            for game in date_info.get('games', []):
                game_pks.append(game['gamePk'])
                #append found gamePk to list
        return game_pks
    return []

#function to get game details by gamePk
def get_game_details(game_pk):
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    response = requests.get(url)
    #200 means successful response
    #set variables based on website results
    if response.status_code == 200:
        game_data = response.json()
        game_info = game_data.get('gameData', {})
        teams = game_info.get('teams', {})
        
        home_team = teams.get('home', {}).get('name', 'N/A')
        away_team = teams.get('away', {}).get('name', 'N/A')
        
        return home_team, away_team
    else:
        return None, None

