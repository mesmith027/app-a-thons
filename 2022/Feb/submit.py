import streamlit as st
import gspread  # to write data to the DB
import pandas as pd
import pytz
from datetime import datetime

from utils import (
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
    team_name = st.text_input(
        "Team name",
        value=st.session_state.team,
        key="team_name",
        on_change=update_team_name,
    )

    pass_2 = st.text_input(
        "Enter password",
        value=st.session_state.pwd,
        type="password",
        key="password",
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
                    if st.checkbox("Show registration details"):
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

                    # If repo and app exist, ask if they want to update
                    if row.GitHub and row.App:
                        st.write(
                            "Your project is already submitted. Do you want to overwrite it?"
                        )
                        if st.checkbox("Overwrite"):
                            submit_project(row, idx)

                    else:
                        submit_project(row, idx)

                    break

                idx += 1

            if idx == len(rows.fetchall()):
                st.error("Incorrect password or team name")
                st.stop()
