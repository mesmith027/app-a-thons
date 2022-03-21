import streamlit as st
from gsheetsdb import connect  # to connect and look at data
from google.oauth2 import service_account
import gspread  # to write data to the DB
import plotly.express as px
import pandas as pd
import pytz
from datetime import datetime


def team_chosen():
    st.session_state["team_chosen"] = not st.session_state.team_chosen


def update_team_name():
    st.session_state["team"] = st.session_state.team_name


def update_password():
    st.session_state["pwd"] = st.session_state.password


def update_mentor():
    st.session_state["mentor"] = st.session_state.mentor_name


def update_team_count():
    st.session_state["num_teams"] = st.session_state.team_count


def update_team_member(x):
    st.session_state[f"team_member_{x}"] = st.session_state[f"team_member_name_{x}"]


def update_category(category_dict):
    st.session_state["category_index"] = category_dict[st.session_state.category]

def disable_widgets():
    st.session_state["disabled"] = True

def reset():
    for key in st.session_state.keys():
        if key != "page_selector" and key != "disabled":
            del st.session_state[key]
    return


def submit_project(row, idx):
    
    github_url = st.text_input("Enter your GitHub repo URL", disabled=st.session_state.disabled)
    app_url = st.text_input("Enter your Streamlit Cloud app URL", disabled=st.session_state.disabled)

    if github_url and app_url:
        if "github.com" not in github_url:
            st.warning("Please enter a valid GitHub repo URL")
            st.stop()

        if "share.streamlit.io" not in app_url:
            st.warning("Please enter a valid Streamlit Cloud app URL")
            st.stop()

        submit = st.button("Submit project")
        if submit:
            gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
            sheet_url = st.secrets["private_gsheets_url"]
            data = gc.open_by_url(sheet_url).sheet1
            data.update(f"C{idx+2}", st.session_state.members)
            data.update(f"E{idx+2}", st.session_state.category)
            data.update(f"F{idx+2}", github_url)
            data.update(f"G{idx+2}", app_url)
            data.update(f"H{idx+2}", str(datetime.now(tz=pytz.utc)))

            st.success("Project submitted")
            st.balloons()
            st.info("Reload the page to make further changes")
            disable_widgets()
            st.stop()
