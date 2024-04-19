import streamlit as st

def authenticate():
    if not st.session_state.get("logged_in"):
        st.error("You must be logged in to access this page.")
        st.experimental_set_query_params(page="login")
        st.stop()
