# TAMU Datathon - HPE Challenge

# Playing around with streamlit

import streamlit as st
import numpy as np
import pandas as pd

@st.cache
def loadData():
    return pd.read_excel("https://urban-data-catalog.s3.amazonaws.com/drupal-root-live/2020/06/08/NHGIS_District_data.xlsx")

def main():
    df = loadData()
    
    st.title("TAMU Datathon")

    st.write(
        "Here is the data: "
        )
    st.write(df)

    # Try out filtering the data and using a checkbox

# Create a list holding all states plus an "All" option
    state_list = list(df.State.unique())
    state_list = ["All"] + state_list

# Make a dropdown select for states
    state_select = st.selectbox("State: ", state_list)

# Filter data using multiselect

    # The columns we're interested in for this project: poverty, access to computer/internet, vulnerable jobs, and single parent
    column_list_short = ["% Poverty (SAIPE Estimate)", "% No Computer or Internet Estimate", "% HHs With Vulnerable Job Estimate","% Single Parent Estimate"]
    column_select = st.multiselect("Variable", column_list_short)

    if state_select == "All":
        cols = ["State","Geographic School District"] + column_select
        st.write(df[cols])
        
        cols2 = ["State"] + column_list_short
        df_state = 100*pd.pivot_table(df[cols2], index = 'State')
        fig = go.Figure(data = [go.Bar(
        x = list(df_state.index),
        y = df_state[ele],
        name = ele
        ) for ele in df_state.columns])
        fig.update_layout(barmode = 'group', width = 1200, height = 600)
        st.plotly_chart(fig)

    else:
        new_df = df[(df.State == state_select)]
        cols = ["Geographic School District"] + column_select
        st.write(new_df[cols])

    
    # Averages for each state using pivot tables
    st.write("Averages for each state:")
    column = st.selectbox("Select Column", column_list_short)
    st.write(pd.pivot_table(df[["State", column]], index="State"))

main() 


