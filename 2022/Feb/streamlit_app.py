import streamlit as st
from gsheetsdb import connect  # to connect and look at data
from google.oauth2 import service_account
import gspread  # to write data to the DB
import plotly.express as px
import pandas as pd
import pytz
from datetime import datetime

import home
import register
import submit
import stats

st.set_page_config(page_title="Quantum-Apps Hackathon", page_icon="⚛️")

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows


sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

if "team_chosen" not in st.session_state:
    st.session_state.team_chosen = False
    st.session_state.members = []
    st.session_state.mentor = ""
    st.session_state.category_index = 0

if "team" not in st.session_state:
    st.session_state["team"] = ""

if "pwd" not in st.session_state:
    st.session_state["pwd"] = ""

if "num_teams" not in st.session_state:
    st.session_state["num_teams"] = 1


title_to_app = {
    "Home": home.home_page,
    "Register": register.register_page,
    "Submit": submit.submit_page,
    "Statistics": stats.stats_page,
}

query_params = st.experimental_get_query_params()
if "page" in query_params:
    page_url = query_params["page"][0]
    if page_url in title_to_app.keys():
        st.session_state["page_selector"] = page_url


def change_page_url():
    st.experimental_set_query_params(page=st.session_state["page_selector"])


titles = list(title_to_app.keys())
selected_page = st.sidebar.radio(
    "Pages:",
    titles,
    key="page_selector",
    on_change=change_page_url,
)
title_to_app[selected_page](rows)
