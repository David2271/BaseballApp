import streamlit as st
import statsapi
import team
import player


def main():
    #if 'team1' not in st.session_state:
        #st.session_state['team1'] = None
    #if 'team2' not in st.session_state:
        #st.session_state['team2'] = None
    #if 'player1' not in st.session_state:
        #st.session_state['player1'] = None
    #if 'player2' not in st.session_state:
        #st.session_state['player2'] = None
    if 'allTeams' not in st.session_state:
        st.session_state['allTeams'] = statsapi.get('teams', {'sportId' : 1})['teams']


def run_page():
    st.set_page_config(page_title='Baseball Predictor', layout='wide')

    st.header("Baseball Predictor", False)
    st.write('Use the menu on the left to select to predict the outcome of a Team v. Team Matchup or a Player v. Player Matchup')
    st.divider()
    
    select_prediction = st.sidebar.selectbox('Select Prediction Type',
                                    ['Team v. Team', 'Player v. Player', 'About'])
    st.sidebar.divider()
    
    if select_prediction == 'Team v. Team':
        team.run()
    elif select_prediction == 'Player v. Player':
        player.run()
    else:
        pass


if __name__ == '__main__':
    main()
    run_page()