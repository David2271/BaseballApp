import streamlit as st
import pickle
import datetime
import model_training.data.mlb_data as mlb_data


def run():
    random_forest_model = pickle.load(open('randomforest_model.sav', 'rb'))
    team1_index = st.sidebar.selectbox('Select Team 1', options=range(0, len(st.session_state['allTeams'])),
                                              format_func=lambda x: st.session_state['allTeams'][x]['name'],
                                              key='team1selectbox', index=1)
    team2_index = st.sidebar.selectbox('Select Team 2', options=range(0, len(st.session_state['allTeams'])),
                                              format_func=lambda x: st.session_state['allTeams'][x]['name'],
                                              key='team2selectbox', index=2)
    st.sidebar.divider()
    team1 = st.session_state['allTeams'][team1_index]
    team2 = st.session_state['allTeams'][team2_index]
    run_randomforest(team1, team2, random_forest_model)


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

        stat_size = int(len(inputs) / 2)    
        team_stat_block(team1['name'], inputs[:stat_size])
        team_stat_block(team2['name'], inputs[stat_size:])
        st.header('Prediction')
        if team1_win > team2_win:
            st.info(f"{team1_win}% chance {team1['name']} will win.")
        else:
            st.info(f"{team2_win}% chance {team2['name']} will win.")


def team_stat_block(team, inputs):
    st.header(f"{team} Stats:")
    st.write("(Average stats from last 10 games)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"\tBatting Avg:\t {inputs[0]}")
        st.write(f"\tHome Runs:\t {inputs[1]}")
        st.write(f"\tOPS:\t {inputs[2]}")
    with col2:
        st.write(f"\tRBI:\t {inputs[3]}")
        st.write(f"\tSLG:\t {inputs[4]}")
        st.write(f"\tStolen Bases:\t {inputs[5]}")
    with col3:
        st.write(f"\tBase on Balls:\t {inputs[6]}")
        st.write(f"\tERA:\t {inputs[7]}")
        st.write(f"\tWin Rate:\t {inputs[8] * 100}%")
    st.write()
