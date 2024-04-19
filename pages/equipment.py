import streamlit as st
from authentication import authenticate

def equipment_page():
    authenticate()
    st.title("Equipment Page")
    # Add equipment page content here

if __name__ == "__main__":
    equipment_page()
