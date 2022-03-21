import streamlit as st

def home_page(rows):
    st.title(":atom_symbol: Quantum-Apps Hackathon :atom_symbol:")
    st.markdown(
        """This hackathon is aimed at students of the Faculty of Chemical
    Sciences of the Autonomous University of Chihuahua, but also at students of
    related areas in other faculties of the same university.

### :books: Requirements:
- Enrolled students or recent graduates (no more than six months after graduation) may participate.
- Register by filling out the fields on this page.

### :1234: Rules:
- Teams of up to 4 contestants are allowed.
- The same person cannot be in more than one team.
- Participants can have a mentor (optional), who must be registered.
- Each Team needs a unique name and password that all the team members know and
    have access to. The Team name and password will be used to enter, modify and submit the hackathon project.
"""
    )
