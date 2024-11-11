import streamlit as st
import statsapi
import prediction_models.log5 as lf


def run():
    #region Sidebar code
    team1_index = st.sidebar.selectbox('Select Team 1', options=range(0, len(st.session_state['allTeams'])),
                                              format_func=lambda x: st.session_state['allTeams'][x]['name'],
                                              key='team1selectbox')
    team2_index = st.sidebar.selectbox('Select Team 2', options=range(0, len(st.session_state['allTeams'])),
                                              format_func=lambda x: st.session_state['allTeams'][x]['name'],
                                              key='team2selectbox')
    st.sidebar.divider()

    st.sidebar.write('<h1>Team Stats<h1>', unsafe_allow_html=True)

    team1 = st.session_state['allTeams'][team1_index]
    team2 = st.session_state['allTeams'][team2_index]

    st.sidebar.write('<h3>Games Played</h3>', unsafe_allow_html=True)
    team1_gamesplayed = statsapi.schedule(team=team1['id'], start_date='01/01/2023', end_date='12/31/2023')
    team1_gameswon = sum(1 for x in team1_gamesplayed if x.get('winning_team','')==team1['name'])
    team1_gamesplayed_slider = st.sidebar.slider(f"{team1['name']} ({len(team1_gamesplayed)} default)",
                                                  min_value=0, max_value=300, value=len(team1_gamesplayed),
                                                  key='team1_gamesplayed_slider')
    team2_gamesplayed = statsapi.schedule(team=team2['id'], start_date='01/01/2023', end_date='12/31/2023')
    team2_gameswon = sum(1 for x in team2_gamesplayed if x.get('winning_team','')==team2['name'])
    team2_gamesplayed_slider = st.sidebar.slider(f"{team2['name']} ({len(team2_gamesplayed)} default)",
                                                  min_value=0, max_value=300, value=len(team2_gamesplayed),
                                                  key='team2_gamesplayed_slider')
    st.sidebar.write('<h3>Games Won</h3>', unsafe_allow_html=True)
    team1_gameswon_slider = st.sidebar.slider(f"{team1['name']} ({team1_gameswon} default)",
                                                  min_value=0, max_value=team1_gamesplayed_slider,
                                                  value=min(team1_gameswon, team1_gamesplayed_slider),
                                                  key='team1_gameswon_slider')
    team2_gameswon_slider = st.sidebar.slider(f"{team2['name']} ({team2_gameswon} default)",
                                                  min_value=0, max_value=team2_gamesplayed_slider,
                                                  value=min(team2_gameswon, team2_gamesplayed_slider),
                                                  key='team2_gameswon_slider')
    #endregion

    #region Body Code
    st.write("This section will display a visual model of the stats of each team, before providing a report on the prediction of which team would win the match.")

    st.header('Prediction Results')
    wp1 = team1_gameswon_slider / team1_gamesplayed_slider
    wp2 = team2_gameswon_slider / team2_gamesplayed_slider
    team1_winchance = int(lf.log_five_prediction(wp1, wp2)*100)
    team1_win = True
    if team1_winchance < 50:
        team1_win = False
    if team1_win:
        st.write(f"{team1['name']} has a {team1_winchance}% chance to win.")
    else:
        st.write(f"{team2['name']} has a {100 - team1_winchance}% chance to win.")
    
    st.divider()
    st.write('Currently the prediction implements the log5 method developed in 1981 by Bill James.')
    st.write('The log5 method only uses the win percentage of each competing team in it\'s calculations.')
    st.write('We are working towards finding a better approach that will factor in a wider array of variables.')
    #endregion




