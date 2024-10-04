import streamlit as st


def run_page():
    st.set_page_config("Player Info", layout='centered')
    st.header('Player Info')

    player = st.selectbox("Player", (None, 'player1', 'player2', 'player3', 'player4',
                                  'player5', 'player6', 'player7', 'player8', 'player9', 
                                  'player10', 'player11', 'player12', 'player13', 'player14', 
                                  'player15', 'player16', 'player17', 'player18', 'player19', 
                                  'player20', ), index=st.session_state['player1'])

    if player is not None:
        st.text('Stats')
        st.text('Stat 1')
        st.text('Stat 2')
        st.text('Stat 3')
        st.text('Stat 4')
        st.text('Stat 5')
        st.text('Stat 6')

    if st.button("Home"):
        st.switch_page('pages/home_page.py')


run_page()