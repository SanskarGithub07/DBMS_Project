import streamlit as st
from authentication import authenticate

def coach_page():
    authenticate()
    st.title("Coach Page")
    # Add coach page content here

if __name__ == "__main__":
    coach_page()
