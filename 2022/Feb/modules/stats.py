import streamlit as st
import plotly.express as px
import pandas as pd

def stats_page(rows):
    st.title(":atom_symbol: Quantum-Apps Hackathon :atom_symbol:")
    st.subheader("Take a look at the current teams!")

    team_number = 0
    team_members = []
    team_size = []
    team_hist = {1: 0, 2: 0, 3: 0, 4: 0}
    category = {
        "Quantum Phenomena": 0,
        "Water care and food sustainability": 0,
        "Visualization and management of data for the conservation of the environment": 0,
        "Use of artificial intelligence and data science in Chemistry": 0,
        "Fight emerging diseases": 0,
        "Chemistry teaching": 0,
    }
    for row in rows:
        team_number += 1
        team_size.append(len(row.Participants.split(",")))
        team_hist[team_size[-1]] += 1
        category[row.Category] += 1
        # st.write(row)

    st.write(f"**There are currently {team_number} teams participating!** :tada:")
    st.write("Lets take a look at some of the statistics of the teams participating!")

    st.subheader("Distribution of Teams:")

    team_hist_list = list(team_hist.items())
    df_team_hist = pd.DataFrame(
        team_hist_list, columns=["Number of Participants per Team", "Count"]
    )
    fig = px.bar(df_team_hist, x="Number of Participants per Team", y="Count")
    st.plotly_chart(fig)

    st.subheader("Teams per Category:")
    category_list = list(category.items())
    df_category = pd.DataFrame(category_list, columns=["Category", "Number of Teams"])
    fig = px.bar(df_category, x="Category", y="Number of Teams")
    st.plotly_chart(fig)
