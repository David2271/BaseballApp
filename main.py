import streamlit as st


def main():
    if 'team1' not in st.session_state:
        st.session_state['team1'] = 'None'
    if 'team2' not in st.session_state:
        st.session_state['team2'] = 'None'
    if 'player1' not in st.session_state:
        st.session_state['player1'] = 'None'
    if 'player2' not in st.session_state:
        st.session_state['player2'] = 'None'

    st.switch_page('pages/home_page.py')


if __name__ == '__main__':
    main()