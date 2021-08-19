import streamlit as st

st.title("Jupyter Notebook to Streamlit App")

file = st.file_uploader("Jupyter Notebook file", help=".ipynb extentions only")
