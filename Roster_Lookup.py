import streamlit as st
import statsapi
import requests


def run():
    st.title("Team Roster Lookup by Season")

    #user input for team name and season
    team_name = st.text_input("Please Enter a Team Name (Not case-sensitive. ex: NEW YORK METS / New York Mets / new york mets)")
    #1901 is first mlb season, default set to 2024
    season = st.number_input("Please Enter a Season (Can be from 1901 to present. ex: 2024)", min_value=1901, max_value=2200, value=2024)

    #streamlit button functionality to show the roster for a given team and season
    if st.button("Get Roster"):
        if team_name:
            team_id, full_team_name = get_team_id(team_name)
            if team_id:
                players = get_team_players_for_season(team_id, season)
                if players:
                    #Streamlit header to display roster
                    st.header(f"{full_team_name} Players for {season}")
                    #loop to go through players and set name and position
                    for player in players:
                        player_name = player['person']['fullName']
                        position = player['position']['name']
                        #Streamlit write out player and position
                        st.write(f"{player_name} - Position: {position}")
                else:
                    st.write(f"No players could be found for {full_team_name} in {season}.")
            else:
                st.write(f"Team name '{team_name}' could not be found.")
        else:
            st.write("Please enter a valid team name.")

#get team ID by name from mlbstats site
def get_team_id(team_name):
    url = "https://statsapi.mlb.com/api/v1/teams"
    response = requests.get(url)
    #200 means successful request
    if response.status_code == 200:
        teams = response.json().get('teams', [])
        for team in teams:
            #using lower function to make it not-case sensitive
            if team_name.lower() in team['name'].lower():
                return team['id'], team['name']
    return None, None

#get team roster or players who have played in a specific season for the team
def get_team_players_for_season(team_id, season):
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster/history?season={season}"
    response = requests.get(url)
    #200 means successfull request
    if response.status_code == 200:
        player_data = response.json().get('roster', [])
        return player_data
    return []

