import streamlit as st


def run_page():
    st.set_page_config("Live Games", layout='centered')
    st.header('Live Game')
    for _ in range(10):
        if st.button(f"Team {_*2+1} vs Team {_+_+2}", key=f"livegamebutton{_}"):
            st.switch_page('pages/home_page.py')


run_page()