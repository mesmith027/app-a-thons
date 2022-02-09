import streamlit as st
from gsheetsdb import connect
from google.oauth2 import service_account

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
#@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

if 'team_chosen' not in st.session_state:
    st.session_state.team_chosen = False
    st.session_state.members = []
    st.session_state.mentor = ""
    st.session_state.category = ""

def team_chosen():
    st.session_state["team_chosen"] = True
    return

st.title("Quantum-Apps Hackathon")
with st.sidebar:
    page = st.radio("Page", ["Home", "Register", "Submit", "Statistics"])

if page == "Home":

    st.markdown("""This hackathon is aimed at students of the Faculty of Chemical
    Sciences of the Autonomous University of Chihuahua, but also at students of
    related areas in other faculties of the same university.

### Requirements:
- Enrolled students or recent graduates (no more than six months after graduation) may participate.
- Register by filling out the fields on this page.

### Rules:
- Teams of up to 4 contestants are allowed.
- The same person cannot be in more than one team.
- Participants can have a mentor (optional), who must be registered.
- Each Team needs a unique name and password that all the team members know and
    have access to. The Team name and password will be used to enter, modify and submit the hackathon project.
""")

elif page == "Register":
    st.subheader("Register your team here:")
    st.write("""Your team name cannot have any spaces, if you wish you can use an underscore (_) or
    dash (-) to separate words.

For example: if your team name is "The A team", **The_A_team** OR **The-A-team** are acceptable.

If the team name you have chosen is taken already, please choose a different name to make sure there
    there is no confusion when winners are announced! """)

    # choosing a team name
    team_name = st.text_input("Team name", key="team_name")

    if len(team_name) > 0:
        # make sure there are no spaces
        if ' ' in team_name:
            st.warning("Please remove spaces in your team name")
            st.stop()
        #remove dashes and underscores and case sensitivity for comparing
        #makes case insensitive (A-team = a-team)
        team_short = team_name.replace("-", "").replace("_", "").casefold()

        #compare team name to those in database
        for row in rows:
            row_short = row.Team.replace("-", "").replace("_", "").casefold()
            if row_short == team_short: #makes case insensitive (A-team = a-team)
                st.warning("That name is taken, please choose a different team name")
                st.stop()

        # if team name is valid, continue to making a password
        st.info("Team name available, please continue")
        st.write(f'You have chosen a team name of: **{team_name}**')
        st.button("Continue with this team name?", on_click=team_chosen)

# create password for team
    if st.session_state["team_chosen"]:
        #password field
        pass_1 = st.text_input("Team Password",type="password")
        #double check that its not a typo
        pass_2 = st.text_input("Confirm password",type="password")

        #if they dont match warn the user
        if pass_1 != pass_2:
            st.warning("Passwords do not match!")
            st.stop()
        else:
        # if they do, save the password
            st.session_state.password = pass_1
            st.write(f'Your team password is **{pass_1}**')
            st.write("Be sure to remember your team name and password, they will be used to edit and submit your project")
            st.write("---")

# once a password is saved in state, the team details can be entered
    if "password" in st.session_state:
        #if the team has a mentor they can enter their name here
        with st.expander("If your team has a Mentor enter details here:"):
            mentor_name = st.text_input("Enter mentor name")
            st.write(mentor_name)

        #a number input controls the number of text fields
        team_count = st.number_input("Number of people on the team:", 1, 4)
        st.write("Enter the full name of all participants on your team:")

        #create correct number of input fields for members names
        member_list = []
        for x in range(1,int(team_count+1)):
            member = st.text_input(f'Name of team member {x}')
            member_list.append(member)

        st.write("Your member list", member_list)

        #Choose the category you want to make you app for
        category_list = ["Quantum Phenomena","Water care and food sustainability",
        "Visualization and management of data for the conservation of the environment",
        "Use of artificial intelligence and data science in Chemistry",
        "Fight emerging diseases","Chemistry teaching"]
        category = st.radio("Choose your category:", category_list)
        st.write("---")

        #add details to session state
        st.session_state.members = member_list
        st.session_state.mentor = mentor_name
        st.session_state.category = category

        #review entry and submit to google sheet
        st.write("Review and confirm your entry:")
        st.write(f'**Team name:** {st.session_state.team_name}')
        st.write(f'**Team Member(s):** {st.session_state.members}')
        st.write(f'**Category:** {st.session_state.category}')
        if len(mentor_name) > 1:
            st.write(f'**Mentor:** {st.session_state.mentor}')
        submit = st.button("Confirm team entry")
        if submit:
            #send to google sheet
            st.balloons()

elif page == "Submit":
    st.write("underconstruction")
else:
    # Print results.
    for row in rows:
        st.write(type(row))
        st.write(row)
