import streamlit as st
import statsapi
import prediction_models.log5 as lf
import pickle
import datetime
import model_training.data.mlb_data as mlb_data


def run():
    random_forest_model = pickle.load(open('randomforest_model.sav', 'rb'))

    #region Sidebar code
    team1_index = st.sidebar.selectbox('Select Team 1', options=range(0, len(st.session_state['allTeams'])),
                                              format_func=lambda x: st.session_state['allTeams'][x]['name'],
                                              key='team1selectbox', index=1)
    team2_index = st.sidebar.selectbox('Select Team 2', options=range(0, len(st.session_state['allTeams'])),
                                              format_func=lambda x: st.session_state['allTeams'][x]['name'],
                                              key='team2selectbox', index=2)
    st.sidebar.divider()

    prediction_method = st.sidebar.selectbox('Select Prediction Method', options=['Random Forest','log5'])

    st.sidebar.divider()

    st.sidebar.write('<h1>Team Stats<h1>', unsafe_allow_html=True)

    team1 = st.session_state['allTeams'][team1_index]
    team2 = st.session_state['allTeams'][team2_index]
    #endregion

    if prediction_method == 'Random Forest':
        run_randomforest(team1, team2, random_forest_model)
    elif prediction_method == 'log5':
        run_log5(team1, team2)


def run_randomforest(team1, team2, model):
    data = mlb_data.get_team_stats(team1['id'], team2['id'], 10, datetime.datetime.today().date().strftime('%Y-%m-%d'))
    if data is not None:
        inputs = [
            data[0][1], data[0][5], data[0][8], data[0][9], data[0][11], data[0][12], data[0][16], data[0][19], data[0][32],
            data[1][1], data[1][5], data[1][8], data[1][9], data[1][11], data[1][12], data[1][16], data[1][19], data[1][32]
            ]
        prediction = model.predict_proba([inputs])
        team1_win = int(prediction[0][0] * 100)
        team2_win = int(prediction[0][1] * 100)
        st.write('Prediction')
        if team1_win > team2_win:
            st.write(f"{team1_win}% chance {team1['name']} will win.")
        else:
            st.write(f"{team2_win}% chance {team2['name']} will win.")


def run_log5(team1, team2):
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


