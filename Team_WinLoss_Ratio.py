import streamlit as st
import statsapi


def run():
    #title of site
    st.title("Team Win-Loss Rate")

    #user input for team and season
    team_name = st.text_input("Enter the team name (Not case-sensitive, ex: boston red sox / BOStoN ReD Sox / BOSTON RED SOX) Note: older seasons may not work.")
    season = st.text_input("Enter the season year (ex: 2024)")

    #streamlit button funcitionality to get win-loss rate
    if st.button("Get Win-Loss Rate"):
        if team_name and season:
            wins, losses, win_loss_rate = get_team_win_loss_rate(team_name, season)
            if wins is not None:
                #show the wins, losses, and win-loss rate for user
                st.write(f"**{team_name} ({season})**")
                st.write(f"- **Wins**: {wins}")
                st.write(f"- **Losses**: {losses}")
                st.write(f"- **Win-Loss Rate**: {win_loss_rate:.3f}")
            else:
                #if no data found for team and season
                st.warning(f"No data found for team '{team_name}' in season {season}.")
        else:
            #if user doesn't input correctly
            st.warning("Please enter both team name and season.")

def get_team_win_loss_rate(team_name, season):
    try:
        #search data froms standings with given season, 103 is American League, 104 is National League
        standings = statsapi.get('standings', {'season': season, 'leagueId': '103,104'})
        #loop through records in standings
        for record in standings['records']:
            #loop through teamRecords
            for team_record in record['teamRecords']:
                #using lower function so it isn't case-sensitive
                if team_record['team']['name'].lower() == team_name.lower():
                    wins = team_record['wins']
                    losses = team_record['losses']
                    win_loss_rate = wins / (wins + losses) if (wins + losses) > 0 else 0

                    return wins, losses, win_loss_rate
    #if something happens, show error
    except Exception as e:
        st.error(f"Error fetching standings data: {e}")
        return None, None, None
    return None, None, None

