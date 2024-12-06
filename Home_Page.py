import streamlit as st
import statsapi
import team
import Roster_Lookup
import Team_WinLoss_Ratio
import Lookup_by_Date


def main():
    if 'allTeams' not in st.session_state:
        st.session_state['allTeams'] = statsapi.get('teams', {'sportId' : 1})['teams']


def run_page():
    st.set_page_config(page_title='Baseball Predictor', layout='wide')

    st.header("Baseball Predictor", False)
    st.write('Use the menu on the left to select to predict the outcome of a Team v. Team Matchup, see the Win-Loss Ratio of a team, lookup a team\'s roster, or lookup a match by date.')
    st.divider()
    
    select_prediction = st.sidebar.selectbox('Select Functionality',
                                    ['Team v. Team', 'Win-Loss Ratio', 'Roster Lookup', 'Game Lookup', 'About'])
    st.sidebar.divider()
    
    if select_prediction == 'Team v. Team':
        team.run()
    elif select_prediction == 'Win-Loss Ratio':
        Team_WinLoss_Ratio.run()
    elif select_prediction == 'Roster Lookup':
        Roster_Lookup.run()
    elif select_prediction == 'Game Lookup':
        Lookup_by_Date.run()
    else:
        pass


if __name__ == '__main__':
    main()
    run_page()