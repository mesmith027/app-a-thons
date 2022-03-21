import streamlit as st
import gspread  # to write data to the DB
import pandas as pd
import pytz
from datetime import datetime

from .utils import (
    team_chosen,
    update_team_name,
    update_password,
    update_mentor,
    update_team_count,
    update_team_member,
    update_category,
    reset,
    submit_project,
)


def submit_page(rows):
    st.title(":atom_symbol: Quantum-Apps Hackathon :atom_symbol:")

    if st.session_state["disabled"]:
        st.info("Please reload this page to enable submission")
    
    team_name = st.text_input(
        "Team name",
        value=st.session_state.team,
        key="team_name",
        on_change=update_team_name,
        disabled=st.session_state.disabled
    )

    pass_2 = st.text_input(
        "Enter password",
        value=st.session_state.pwd,
        type="password",
        key="password",
        disabled=st.session_state.disabled
    )

    if team_name and pass_2:
        update_password()
        if len(team_name) > 0:
            # make sure there are no spaces
            if " " in team_name:
                st.warning("Please remove spaces in your team name")
                st.stop()
            # remove dashes and underscores and case sensitivity for comparing
            # makes case insensitive (A-team = a-team)
            team_short = team_name.replace("-", "").replace("_", "").casefold()

            # compare team name to those in database
            idx = 0
            for row in rows:
                if {team_short: pass_2} == {
                    row.Team.replace("-", "").replace("_", "").casefold(): row.Password
                }:
                    st.write(
                        f"Welcome back **`{team_name}`**. You can now edit your project and submit it to the competition."
                    )
                    if st.checkbox("Show registration details", disabled=st.session_state.disabled):
                        st.write(
                            {
                                "Team name": row.Team,
                                "Password": row.Password,
                                "Team Members": row.Participants,
                                "Mentor": row.Mentor,
                                "Category": row.Category,
                                "GitHub Repo": row.GitHub,
                                "App URL": row.App,
                            }
                        )
                    
                    # Count existing members from Google Sheet and add the count to session state
                    member_list = [member.strip('[]').replace("'","").replace("'","").strip() for member in row.Participants.split(",")]
                    st.session_state.num_teams = len(member_list)

                    # a number input controls the number of text fields
                    team_count = st.number_input(
                        "Number of people on the team:",
                        1,
                        4,
                        value=st.session_state.num_teams,
                        key="team_count",
                        on_change=update_team_count,
                        disabled=st.session_state.disabled
                    )
                    st.write("Enter the full name of all participants on your team:")

                    # Get existing members from Google Sheet and add them to session state
                    for x in range(1, int(len(member_list)+1)):
                        st.session_state[f"team_member_{x}"] = member_list[x-1]

                    # Create text input for each team member
                    member_list = []
                    for x in range(1, int(team_count + 1)):

                        if f"team_member_{x}" not in st.session_state.keys():
                            st.session_state[f"team_member_{x}"] = ""

                        member = st.text_input(
                            f"Name of team member {x}",
                            value=st.session_state[f"team_member_{x}"],
                            key=f"team_member_name_{x}",
                            on_change=update_team_member,
                            args=(x,),
                            disabled=st.session_state.disabled
                        )
                        member_list.append(member)

                    # Choose the category you want to make you app for
                    category_dict = {
                        "Quantum Phenomena": 0,
                        "Water care and food sustainability": 1,
                        "Visualization and management of data for the conservation of the environment": 2,
                        "Use of artificial intelligence and data science in Chemistry": 3,
                        "Fight emerging diseases": 4,
                        "Chemistry teaching": 5,
                    }

                    # Get existing category from Google Sheet and add it to session state
                    st.session_state.category_index = category_dict[row.Category]

                    category = st.radio(
                        "Choose your category:",
                        category_dict.keys(),
                        index=st.session_state.category_index,
                        key="category",
                        on_change=update_category,
                        args=(category_dict,),
                        disabled=st.session_state.disabled
                    )

                    # add details to session state
                    st.session_state.members = str(member_list)

                    # If repo and app exist, ask if they want to update
                    if row.GitHub and row.App:
                        st.write(
                            "Your project is already submitted. Do you want to overwrite it?"
                        )
                        if st.checkbox("Overwrite", disabled=st.session_state.disabled):
                            submit_project(row, idx)

                    else:
                        submit_project(row, idx)

                    break

                idx += 1

            if idx == len(rows.fetchall()):
                st.error("Incorrect password or team name")
                st.stop()
