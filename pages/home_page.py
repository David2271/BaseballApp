import streamlit as st


def run_page():
    st.set_page_config(page_title='Home', layout='wide')

    st.header("Home", False)
    with st.container():
        if st.button(label='Live Game', use_container_width=True):
            st.switch_page('pages/live_game_page.py')
        if st.button(label='Team Info', use_container_width=True):
            st.switch_page('pages/team_info_page.py')
        if st.button(label='Player Info', use_container_width=True):
            st.switch_page('pages/player_info_page.py')


run_page()