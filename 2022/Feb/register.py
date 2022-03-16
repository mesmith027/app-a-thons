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

repo = ""
app = ""


def register_page(rows):
    st.title(":atom_symbol: Quantum-Apps Hackathon :atom_symbol:")
    st.subheader("Register your team here:")
    st.write(
        """Your team name cannot have any spaces, if you wish you can use an underscore (_) or
    dash (-) to separate words.

For example: if your team name is "The A team", **The_A_team** OR **The-A-team** are acceptable.

If the team name you have chosen is taken already, please choose a different name to make sure there
    there is no confusion when winners are announced! """
    )

    # choosing a team name
    team_name = st.text_input(
        "Team name",
        value=st.session_state.team,
        key="team_name",
        on_change=update_team_name,
    )

    if len(team_name) > 0:
        # make sure there are no spaces
        if " " in team_name:
            st.warning("Please remove spaces in your team name")
            st.stop()
        # remove dashes and underscores and case sensitivity for comparing
        # makes case insensitive (A-team = a-team)
        team_short = team_name.replace("-", "").replace("_", "").casefold()

        # compare team name to those in database
        for row in rows:
            row_short = row.Team.replace("-", "").replace("_", "").casefold()
            if row_short == team_short:  # makes case insensitive (A-team = a-team)
                st.warning("That name is taken, please choose a different team name")
                st.stop()

        # if team name is valid, continue to making a password
        st.info("Team name available, please continue")
        st.write(f"You have chosen a team name of: **`{team_name}`**")
        st.button("Continue with this team name?", on_click=team_chosen)

    # create password for team
    if st.session_state["team_chosen"]:
        # password field
        pass_1 = st.text_input(
            "Team Password", value=st.session_state.pwd, type="password"
        )
        # double check that its not a typo
        pass_2 = st.text_input(
            "Confirm password",
            value=st.session_state.pwd,
            type="password",
            key="password",
        )

        if pass_1 and pass_2:
            # if they dont match warn the user
            if pass_1 != pass_2:
                st.warning("Passwords do not match!")
                st.stop()
            else:
                # if they do, save the password
                update_password()
                st.write(f"Your team password is **`{pass_1}`**")
                st.write(
                    "❗ Be sure to remember your team name and password, they will be used to edit and submit your project"
                )
                st.write("---")

    # once a password is saved in state, the team details can be entered
    if st.session_state.pwd:
        # if the team has a mentor they can enter their name here
        with st.expander("If your team has a Mentor enter details here:"):
            mentor_name = st.text_input(
                "Enter mentor name",
                value=st.session_state.mentor,
                key="mentor_name",
                on_change=update_mentor,
            )

        # a number input controls the number of text fields
        team_count = st.number_input(
            "Number of people on the team:",
            1,
            4,
            value=st.session_state.num_teams,
            key="team_count",
            on_change=update_team_count,
        )
        st.write("Enter the full name of all participants on your team:")

        # create correct number of input fields for members names
        member_list = []
        for x in range(1, int(team_count + 1)):

            if f"team_member_{x}" not in st.session_state:
                st.session_state[f"team_member_{x}"] = ""

            member = st.text_input(
                f"Name of team member {x}",
                value=st.session_state[f"team_member_{x}"],
                key=f"team_member_name_{x}",
                on_change=update_team_member,
                args=(x,),
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
        category = st.radio(
            "Choose your category:",
            category_dict.keys(),
            index=st.session_state.category_index,
            key="category",
            on_change=update_category,
            args=(category_dict,),
        )
        st.write("---")

        # add details to session state
        st.session_state.members = str(member_list)
        # st.session_state.category = category

        # review entry and submit to google sheet
        st.write("Review and confirm your entry:")
        st.write(f"**Team name: `{st.session_state.team_name}`**")
        st.write(f"**Team Member(s): `{st.session_state.members}`**")
        st.write(f"**Category: `{st.session_state.category}`**")
        st.write(f"**Password: `{st.session_state.password}`**")

        if len(mentor_name) > 1:
            st.write(f"**Mentor: `{st.session_state.mentor}`**")

        submit = st.button("Confirm team entry", on_click=team_chosen)

        if submit:
            # send to google sheet
            ## write results to google sheets
            gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
            sheet_url = st.secrets["private_gsheets_url"]
            data = gc.open_by_url(sheet_url).sheet1
            data.append_row(
                [
                    st.session_state.team_name,
                    st.session_state.password,
                    st.session_state.members,
                    st.session_state.mentor_name,
                    st.session_state.category,
                    repo,
                    app,
                    str(datetime.now(tz=pytz.utc)),
                ]
            )

            st.info("Team information submitted")
            st.balloons()
            registration = pd.DataFrame(
                {
                    "Team name": [st.session_state.team_name],
                    "Password": [st.session_state.password],
                    "Members": [st.session_state.members],
                    "Mentor": [st.session_state.mentor_name],
                    "Category": [st.session_state.category],
                }
            )
            download = st.download_button(
                label="Download registration details",
                data=registration.to_csv(index=False).encode("utf-8"),
                file_name=f"{st.session_state.team_name}_registration_details.csv",
                mime="text/csv",
                on_click=reset,
            )
