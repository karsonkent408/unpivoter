import pandas as pd
import numpy as np
import streamlit as st



def main():
    st.set_page_config(
        page_title="Unpivot your dumb table",
        page_icon="🤡",
        layout="centered",
    )
    with st.container(horizontal_alignment="center", vertical_alignment="center"):
        st.title('Unpivot your dumb table')
        st.write("Why do clients refuse to give us data tables in a format we can use?")
        st.write("No one will ever know, and that will never change.")
        st.write("So here is an app to unpivot your dumb table into a long format")
        st.write("It will also aggregate the data by the id vars and sum the value vars")
        st.divider()

    uploaded_file = st.file_uploader("Upload your dumb table")
    
    if not uploaded_file:
        return
    
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_extension in ("xlsx", "xls"):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Please upload a CSV or Excel file")
        return

    headers = df.columns.tolist()

    id_vars = st.multiselect(
        "Select the id vars", 
        headers, 
        default=[],
        help="Select headers that will be used to identify the rows"
    )

    value_candidates = [header for header in headers if header not in id_vars]

    value_vars = st.multiselect(
        "Select the value vars", 
        value_candidates, 
        default=[],
        help="Select the headers that will be used to aggregate the data"
    )

    value_name = st.text_input("Select the name of the value column", "Value")

    var_name = st.text_input("Select the name of the var column", "Variable")

    if len(id_vars) == 0 or len(value_vars) == 0 or not value_name or not var_name:
        st.error("Please select the id vars, value vars, value name, and var name")
        return

    df_agg = df.groupby(id_vars, as_index=False)[value_vars].sum()

    new_df = df_agg.melt(id_vars=id_vars, value_vars=value_vars, value_name=value_name, var_name=var_name)

    st.write(new_df)

    st.download_button(
        label="Download data as CSV",
        data=new_df.to_csv(index=False),
        file_name="unpivoted_data.csv",
        mime="text/csv",
        type="primary",
        help="Download the unpivoted data as a CSV file",
        disabled=False,
        use_container_width=True,
        key="download_csv",
    )


if __name__ == "__main__":
    main()
