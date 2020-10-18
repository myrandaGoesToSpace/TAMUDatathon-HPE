# TAMU Datathon - HPE Challenge

# Playing around with streamlit

import streamlit as st
import numpy as np
import pandas as pd
from sklearn import preprocessing
import dash
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@st.cache(allow_output_mutation=True)
def loadData():
    return pd.read_excel("https://urban-data-catalog.s3.amazonaws.com/drupal-root-live/2020/06/08/NHGIS_District_data.xlsx")

def main():


    nav = st.sidebar.radio("Navigation",["Purpose","Visualization","Call to Action"])
    df = loadData()
    if nav == "Call to Action":
        st.write(""" *For low-income students/homes with job instability*:   some of these students relied on school breakfast and lunch programs for food. HPE can help these students by providing meals. *For single-parent homes*: School from home means single parents have to remain at home with their kids or find a babysitter. HPE can help this demographic by investing in child care or providing easier ways for single parents to transition to working from home For no internet access: These students need the internet to complete school. HPE can help set up local hotspots for students or donate technology to schools in need""" )
    if nav == "Purpose":
        st.title("COVID-19 Impact on K-12 Students")
        st.write("All around the world, K-12 students are adapting to the changes put in place by COVID-19. Schools are now conducted online, meaning that students are increasingly reliant on the resources available at home. Students at a significant disadvantage include those from low-income housholds, without access to home internet, with parents suffering from job instability, and in single-parent homes. HPE is committed to making a positive impact on the community and knows firsthand the advantage technology can provide. This data visualization tool uses a dataset from the Urban Institute to compare the percentages of students in each state living in poverty, without internet access, in homes with job instability, and living with a single parent. Each of these targeted communities needs extra support during the pandemic, and HPE has the resources to make a difference.")
        st.header("Why Students Matter to HPE")
        st.write("HPE knows that K-12 students are the next generation of engineers, programmers, creators, and scholars that will impact the world. That's why it's important to invest in these future community members and ensure their success.")
        st.header("Vulnerable Demographics")
        st.write(""" This app identifies four populations that are especially vulnerable due to COVID-19:
- __Students living in poverty__ typically rely on school breakfast and lunch to receive their meals. Now that the students are forced to stay home, they may not always have enough food.

- **Students without access to internet or a computer** cannot complete assignments or attend class online. These students will fall
	behind in school.
- **Students in homes with unstable jobs** have parents or guardians with a job hindered by COVID-19. Reasons for job vulnerability
	include inability to transition to remote work, business closures, and lay-offs.
- **Students in single-parent homes** now require a parent, guardian, sibling, or babysitter to stay home with them. Single parents
	might have difficulty staying home with their child if they cannot work from home.


        """ )
        covid_data = pd.read_csv("https://data.cdc.gov/api/views/9mfq-cb36/rows.csv?accessType=DOWNLOAD")
        cases = covid_data[['submission_date','state','tot_cases']].dropna()
        covid_cases = cases[cases.iloc[:,0] == '10/16/2020'].iloc[:,1:]
        covid_cases = covid_cases.pivot_table(index = 'state').sort_values(by = 'tot_cases', ascending = False)
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2,1)
        df['No_Internet'] = df['Children 5-17 (SAIPE Estimate)']*df['% No Computer or Internet Estimate']
        our_data = df.groupby('State')['No_Internet'].sum()
        our_data = our_data.sort_values(ascending = False)[:10]
        our_data.plot(kind = 'bar', ax = axes[1], figsize = (12,8))
        covid_cases[:10].plot(kind = 'bar',ax = axes[0], figsize = (12,8))
        axes[1].set_ylabel('Vulnerable Students')
        axes[0].set_ylabel('Total Covid Cases')
        st.pyplot(fig)

    # df['Student Vulnerability Index'] = df['% Poverty (SAIPE Estimate)'] * \
    #     df['% HHs With Vulnerable Job Estimate'] * \
    #         df['% No Computer or Internet Estimate']

    if nav == 'Visualization':
        st.title("Visualizations")
        st.header("Choose a state or any variable below")
        min_max_scaler = preprocessing.MinMaxScaler()
        svi = min_max_scaler.fit_transform(df[['% Poverty (SAIPE Estimate)',
        '% HHs With Vulnerable Job Estimate','% No Computer or Internet Estimate']].values).sum(axis = 1)/3
        df['Student Vulnerability Index'] = svi



    # st.write(df)

    # Try out filtering the data and using a checkbox

# Create a list holding all states plus an "All" option
        state_list = list(df.State.unique())
        state_list = ["All"] + state_list

# Make a dropdown select for states
        state_select = st.selectbox("State: ", state_list)

# Filter data using multiselect

    # The columns we're interested in for this project: poverty, access to computer/internet, vulnerable jobs, and single parent
        column_list_short = ["% Poverty (SAIPE Estimate)",
        "% No Computer or Internet Estimate", "% HHs With Vulnerable Job Estimate",
        "% Single Parent Estimate"]
        column_list_svi = ["Student Vulnerability Index"] + column_list_short
    #we don't need column select anymore
        #column_select = st.multiselect("Variable", column_list_short)
        import plotly.graph_objects as go
        if state_select == "All":

            #cols = ["State","Geographic School District"] + column_select
        # removed dataframe because the user doesn't need it
            #st.write(df[cols])
            st.text(" \n")
            st.text(" \n")
            st.text(" \n")
            st.text(" \n")
            st.text(" \n")
            st.text(" \n")
            num_or_perc = st.selectbox("Would you like Population Numbers or Percentages?",
            ['Percentage', 'Numbers'])
            cols2 = ["State"] + column_list_short

            st.text(" \n")
            st.write('Click on the legend to select a variable. \n Click and drag on the graph to zoom in.')
            if num_or_perc == 'Percentage':
                df_state = 100*pd.pivot_table(df[cols2], index = 'State')
                fig = go.Figure(data = [go.Bar(
                x = list(df_state.index),
                y = df_state[ele],
                name = ele,
                ) for ele in df_state.columns])
                fig.update_layout(barmode = 'group', width = 1200, height = 600, title=" State vs. Average Percent")

                fig.update_xaxes(title_text='State')
                fig.update_yaxes(title_text='Average Percent')
                st.plotly_chart(fig)

            else:
                df_numbers = df[cols2].groupby('State')[column_list_short].sum()
                fig_num = go.Figure(data = [go.Bar(
                x = list(df_numbers.index),
                y = df_numbers[ele],
                name = ele
                ) for ele in df_numbers.columns])
                fig_num.update_layout(barmode = 'group', width = 1200, height = 600, title=" State vs. Average Population for Demographic")
                fig_num.update_xaxes(title_text='State')
                fig_num.update_yaxes(title_text='Average Population')

                st.plotly_chart(fig_num)

        else:

            st.text(" \n")
            st.write('Click on the legend to select a variable. \n Click and drag on the graph to zoom in.')


            new_df = df[(df.State == state_select)]
            #cols = ["Geographic School District"] + column_select
            #st.write(new_df[cols])
            st.text(" \n")
            st.text(" \n")

        #A lot of datapoints in the bar plot
            fig1 =  go.Figure(data = [go.Bar(
            x = new_df["Geographic School District"],
            y = 100*new_df[ele],
            name = ele
            ) for ele in column_list_short])
            fig1.update_layout(barmode = 'group', width = 1200, height = 600)
            st.plotly_chart(fig1)

            fig2 = go.Figure()
            for i in range(4):
                fig2.add_trace(go.Box(
                y = 100*new_df[column_list_short[i]],
                name = column_list_short[i],
                boxmean = True
                ))
            fig2.update_layout(barmode = 'group', width = 1200, height = 600)
            st.plotly_chart(fig2)


    # Student Vulnerability Index
        st.text(" \n")
        st.text(" \n")
        st.text(" \n")
        st.text(" \n")
        st.text(" \n")
        st.text(" \n")
        st.write("## Student Vulnerability Index:")
        st.write("These are the districts with the highest needs right now. The SVI is a value scaled on the percentages across each vulnerable demographic, ranging 0 (no needs) to 1 (high needs).")
        #column = st.selectbox("Choose Demographic", column_list_svi)
        st.write(pd.pivot_table(df[['Geographic School District', "Student Vulnerability Index"]], index='Geographic School District').sort_values(by="Student Vulnerability Index", ascending=False))

main()