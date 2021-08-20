import streamlit as st
import json
from streamlit_ace import st_ace

st.title("Jupyter Notebook to Streamlit App 🥳")

file = st.file_uploader("Jupyter Notebook file", help=".ipynb extentions only", type='ipynb')

file
if file is not None:
    json_data = json.load(file)

    num_cells = len(json_data["cells"])
    st.write("Your notebook has",num_cells,"cells")

    full_code = ""

    for x in range(num_cells):

        if json_data["cells"][x]["cell_type"] == "markdown":
            for y in range(len(json_data["cells"][x]["source"])):
                st.markdown(json_data["cells"][x]["source"][y])
        elif json_data["cells"][x]["cell_type"] == "code":
            for y in range(len(json_data["cells"][x]["source"])):
                full_code = full_code + json_data["cells"][x]["source"][y]

            #code = st_ace(full_code,wrap=True, font_size=15,theme="dawn",language="python")
            #exec(code)
            st.code(full_code)
            #exec(full_code)
        else:
            st.write("sorry unknown cell type")
            st.write(json_data["cells"][x]["cell_type"])
