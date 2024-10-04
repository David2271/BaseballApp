import streamlit as st


def teambox(label, index=None):
    team = st.selectbox(label, (None, 'team1', 'team2', 'team3', 'team4',
                                  'team5', 'team6', 'team7', 'team8', 'team9', 
                                  'team10', 'team11', 'team12', 'team13', 'team14', 
                                  'team15', 'team16', 'team17', 'team18', 'team19', 
                                  'team20', ), index=index+1)
    if team is not None:
        with st.expander('STATS'):
            st.text('Stat 1')
            st.text('Stat 2')
            st.text('Stat 3')
            st.text('Stat 4')
            st.text('Stat 5')
            st.text('Stat 6')
        with st.expander('PLAYERS'):
            for _ in range(10):
                if st.button(f"Player {_+1}", key=f"{label}_playerbutton{_}"):
                    st.session_state['player1'] = _+1
                    st.switch_page('pages/player_info_page.py')
    return team


def button_list(label, list):
    for _ in range(len(list)):
        if st.button(f"Player {_}", key=f"{label}.{_}"):
            #st.session_state['player1'] = _
            st.switch_page('pages/player_info_page.py')


def text_list():
    pass