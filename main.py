import streamlit as st


def main():
    if 'team1' not in st.session_state:
        st.session_state['team1'] = 0
    if 'team2' not in st.session_state:
        st.session_state['team2'] = 0
    if 'player1' not in st.session_state:
        st.session_state['player1'] = 0
    if 'player2' not in st.session_state:
        st.session_state['player2'] = 0

    st.switch_page('pages/home_page.py')


if __name__ == '__main__':
    main()