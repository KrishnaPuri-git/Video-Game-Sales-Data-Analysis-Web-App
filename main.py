import streamlit as st
import streamlit as st
import pandas as pd
from visualization import *
import plotly.graph_objs as go

def readData():
    Video_Games = pd.read_csv('vgsales.csv')
    Video_Games.rename(columns={'Platform':'Plateform'}, inplace=True)
    Video_Games['Year'] = Video_Games['Year'].fillna(0).astype('int')
    return Video_Games



df = readData()


sidebar = st.sidebar

sidebar.title('User Options')


def introduction():
    st.image('4ff07986208593.5d9a654e92f36.gif', width=None)
    st.markdown("""
        ## Exploratory data analysis and Vizualization of Video Games Sales data

    \nIn this analysis web app, I've tried to perform the analysis on the Video Games Sales dataset. Here, I've used various libraries of Python for visualization of Data. The Dataset which is Used is from Kaggle (https://www.kaggle.com/datasets/gregorut/videogamesales)
    
    \n#### Libraries used :

        \n-Matplotlib: https://matplotlib.org/ 
        \n-Seaborn: https://seaborn.pydata.org/
        \n-Plotly: https://plotly.com/
        \n-Pandas: https://pandas.pydata.org/
        \n-Streamlit: https://streamlit.io/
        
    \n#### Tasks Implemented :

        \n\t-Data Preparation and Cleaning
        \n\t-Exploratory Analysis and Visualization
        \n\t-Observations and Conclusions
    """)

    st.markdown("""###### *switch to Analysis page using selectbox in the sidebar """)    
    c1, c2 = st.columns(2)



def execute():
    st.markdown("""# Analysis""")
    st.dataframe(df)
    
    st.markdown("""## Dataset Insights:""")
    st.markdown("""
       - ##### Total Games by Name: 431
       - ##### Total Games by Genre: 12
       - ##### Total Games by Publisher: 34
       - ##### 500 games are ranked based on their sales in millions
       - ##### Games released between 1980 to 2020""")


    # sales in numbers

    st.markdown("## Sales in Various Regions")
    start, end = st.slider("Double Ended Slider",value=[2005,2008], min_value=1980, max_value=2020)
    selRegion = st.selectbox("Select Region", ['NA_Sales', 'EU_Sales', 'JP_Sales','Other_Sales','Global_Sales'])
    year_count = (i for i in range(start,end))
    count_in_range = df.loc[df['Year'].isin(year_count)] 
    ns = sum(count_in_range[selRegion])
    st.header(round(ns))

    st.markdown(""" 
    - With the help of above slider (in years) and selectbox (in regions):

            \n\t- You can select any time interval (start and end).
            \n\t- Then select any region, and it shows the total no. of sales (in millions) in that region.""")

    # Genre in various regions

    st.markdown("## Top Genre in Various Regions")
    genregion = st.selectbox("Select Regions", ['NA_Sales', 'EU_Sales', 'JP_Sales','Other_Sales','Global_Sales'])
    data = df.groupby('Genre', as_index=False).sum().sort_values('NA_Sales', ascending=False)
    #st.dataframe(data)
    fig = plotBar(data, 'Genre', genregion)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(""" 
    - With the help of above selectbox region(in sales):

            \n\t- Using selectbox when you can select a Region, it shows the top genre from that selcted region.
            \n\t- Action genre is overall most popular in most regions.""")

    # Top 10 Publishers in various regions

    st.markdown("## Top 10 Publishers in Various Regions")
    pubregion = st.selectbox("Select any Regions", ['NA_Sales', 'EU_Sales', 'JP_Sales','Other_Sales','Global_Sales'])
    data = df.groupby('Publisher', as_index=False).sum().sort_values('NA_Sales', ascending=False).head(10)
    
    fig = plotBar(data,'Publisher', pubregion)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(""" 
    - With the help of above selectbox region(in sales):

            \n\t- From dropdown selectbox, you can select any region.
            \n\t- On selecting the region the top Publishers from that selcted region show up.""")


    # No. of games published per year

    st.markdown('## No. of Games Published Per Year')
    data = df[df['Year'] != 0].groupby('Year', as_index=False).count()
    #st.dataframe(data)
    fig = plotLine(data, 'Year', 'Publisher')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    - Observations Based on above linear Graph 

            \n\t- As observed in the graph above, video-game sales peaked in 2005-2010 across the globe.
            \n\t- At its peak, an estimated 1428 million games were sold worldwide.""")


    # Most popular Genre
    st.markdown('## Most Popular Genre Globally')
    data1 = df.groupby('Genre', as_index=False).count()
    fig= px.pie(data1, labels='Genre', values='Rank', names='Genre')

    data3 = df[df['Year']!=0].groupby('Year', as_index=False).sum()
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    - Observations based on above pie chart 

            \n\t- As evident from the graph above, action genre is the highest across the globe.
            \n\t- so its clear that people like action Games more as compared to any other genre.""")

    
    # Various Sales in years according to their Regions
    
    st.markdown('## Sales in Various Regions')
    data = df[df['Year'] != 0].groupby('Year', as_index=False).count()
    px.line(data, 'Year', 'Name')

    fig = go.Figure()
    fig.add_trace(go.Line(x = data3.Year, y = data3.NA_Sales, name="NA Sales"))
    fig.add_trace(go.Line(x = data3.Year, y = data3.EU_Sales, name="EU Sales"))
    fig.add_trace(go.Line(x = data3.Year, y = data3.JP_Sales, name="JP Sales"))
    fig.add_trace(go.Line(x = data3.Year, y = data3.Other_Sales, name="Other Sales"))
    fig.add_trace(go.Line(x = data3.Year, y = data3.Global_Sales, name="Global Sales"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    - Observations based on above linear graph 

            \n\t- In the graph above video-game sales from 1980-2020 across the globe can be seen.
            \n\t- Year 2008 saw the highest sales of all time with 678.9 million.""")



options = ['Introduction', 'Analysis']

selOption = sidebar.selectbox("Select an Option", options)

if selOption == options[0]:
    introduction()
elif selOption == options[1]:
    execute()