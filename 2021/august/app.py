import streamlit as st
import json

st.title("Jupyter Notebook to Streamlit App 🥳")

file = st.file_uploader("Jupyter Notebook file", help=".ipynb extentions only", type='ipynb')

if file is not None:
    json_data = json.load(file)
    #st.write(json_data["metadata"], len(json_data))
    #st.write(json_data.keys())

    #st.write(json_data["cells"])

    num_cells = len(json_data["cells"])
    st.write("Your notebook has",num_cells,"cells")

    for x in range(num_cells):
        st.write(x)
        #st.write(json_data["cells"][x])

        if json_data["cells"][x]["cell_type"] == "markdown":
            #st.write(len(json_data["cells"][x]["source"]))
            for y in range(len(json_data["cells"][x]["source"])):
                st.markdown(json_data["cells"][x]["source"][y])
        elif json_data["cells"][x]["cell_type"] == "code":
            st.write(len(json_data["cells"][x]["source"]))
            for y in range(len(json_data["cells"][x]["source"])):
                with st.echo():
                    json_data["cells"][x]["source"][y]
        else:
            st.write("unknown cell type")
            st.write(json_data["cells"][x]["cell_type"])
