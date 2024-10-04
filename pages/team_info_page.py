import streamlit as st
import components.custom_components as cc


def run_page():
    st.set_page_config("Team Info", layout='centered')
    st.header('Team Info')

    cc.teambox('Team 1', st.session_state['team1'])
    cc.teambox('Team 2', st.session_state['team2'])

    if st.button("Home"):
        st.switch_page('pages/home_page.py')


run_page()