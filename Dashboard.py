#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import os
from streamlit_folium import folium_static
import folium
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def summary_poster(pie_df):
     #MAKE SUBPLOTS
    fig = make_subplots(
        specs=[[{"type": "pie"}],],
        subplot_titles=('Over 25 - Education Breakdown'))
    pie_data = pie_df
    fig.add_trace(go.Pie(labels = pie_data.index,
                                values = pie_data.values,
                                hole = 0.4,
                                legendgroup = 'grp1',
                                showlegend=True),
                                row = 1, col = 1)
    fig.update_traces(hoverinfo = 'label+percent',
                            textinfo = 'value+percent',
                            textfont_color = 'white',
                            marker = dict(#colors = pie_data.index.map(color_dict),
                                        line=dict(color='white', width=1)),
                            row = 1, col = 1)                           
    return fig


def map_markets(market_ind):

    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    if market_ind == 'Both':
        df_map = pd.read_csv('Capstone Cencus Data - data_table.csv').set_index('city_name')
    elif market_ind == 'NFL':
        df_map = df.loc[df['target_city'] != 'x']
    elif market_ind == 'Target':
        df_map = df.loc[df['target_city'] == 'x']

    #iterate through dataframe
    for index, row in df_map.iterrows():
        city_name = row.city_name2
        team_name = row.team_name
        location = (row.lat,row.lon)
        pop2021 = "{:,}".format(row.pop2021)
        pop2010 = row.pop2010
        pop_change = row.growth_10 * 100
        pop_change_format = "{:.2f}".format(pop_change)
        density = "{:,}".format(row.density)
        num_teams = row.pro_teams
        stadiums = row.stadium_count
        income = "{:,}".format(row.per_capita_income)
        avg_household_size = row.avg_household_size
        
        #create marker pop-up html
        city_html = folium.Html(f"""<p style="text-align: Center;"><strong><span style="font-family: Didot, serif; font-size: 18px;">{team_name}</span></strong></p>
        <p style="text-align: Left;"><span style="font-family: Didot, serif; font-size: 15px;">2021 Population: {pop2021}<br>
        Pop. Change since 2010: {pop_change_format}%<br>
        Pop. Density per sq. mile: {density}<br>
        Per Capita Income: ${income}<br>
        # of Professional Teams: {num_teams}<br>
        # of Stadiums: {stadiums}</span></p>
        """, script=True)

        # add marker for city locations
        tooltip = city_name
        
        #set popup width
        popup = folium.Popup(city_html,
                         min_width=100,
                         max_width=250)
    
        folium.Marker(
            location=location, 
            #popup=team_name, 
            popup=popup,
            tooltip=tooltip
        ).add_to(m)
    
    # call to render Folium map in Streamlit
    folium_static(m)

st.set_page_config(page_title = "Buffalo Bills Relocation Dashboard", layout="wide")

os.chdir('C:/Users/ejl9900/Desktop/Data Science/MSDS498/Data')

#get data for map
df = pd.read_csv('Capstone Cencus Data - data_table.csv').set_index('city_name')

#banner
banner = Image.open("./Images/Buffalo-Bills-banner.jpg")
st.image(banner)

# dashboard title
st.title('Buffalo Bills Market Relocation Dashboard')

st.markdown('Target Market Comparison')

#get target market data
#dataframe for first drop down
df_tm1 = df.loc[(df['target_city'] == 'x')]
#dataframe for second drop down
df_tm2 = df.loc[(df['target_city'] == 'x')]

#st.write(df_tm)

st.write('Select two of the target markets from the drop down menus to compare demographics and rankings :football:')
select_market1 = []
select_market2 = []

#display drop downs
col1, col2 = st.columns(2)
select_market1.append(col1.selectbox('First Market', df_tm1))
select_market2.append(col2.selectbox('Second Market', df_tm2))

#Filter df1 based on selection
market_df1 = df_tm1[df_tm1['city_name2'].isin(select_market1)]
tm_pop_change1 = market_df1.iloc[0]['growth_10'] * 100
tm_growth_rank1 = str(market_df1.iloc[0]['growth_rank'])
tm_income1 = market_df1.iloc[0]['per_capita_income']

#Filter df2 based on selection
market_df2 = df_tm2[df_tm2['city_name2'].isin(select_market2)]
tm_pop_change2 = market_df2.iloc[0]['growth_10'] * 100
tm_growth_rank2 = str(market_df2.iloc[0]['growth_rank'])
tm_income2 = market_df2.iloc[0]['per_capita_income']

#display images
nm1 = str(market_df1.iloc[0]['city_name2'])
nm2 = str(market_df2.iloc[0]['city_name2'])
#If df_tm1 = 
col1, col2 = st.columns(2)

if nm1 == 'San Antonio':
    image1 = Image.open("./plots/SA_skyline.jpg")
elif nm1 == 'Austin':
    image1 = Image.open("./plots/Austin.png")
elif nm1 == 'Louisville':
    image1 = Image.open("./plots/Louisville.png")
elif nm1 == 'Oklahoma City':
    image1 = Image.open("./plots/OKC.png")
elif nm1 == 'Portland':
    image1 = Image.open("./plots/Portland.png")
elif nm1 == 'Buffalo':
    image1 = Image.open("./plots/Buffalo.jpeg")
    
if nm2 == 'San Antonio':
    image2 = Image.open("./plots/SA_skyline.jpg")
elif nm2 == 'Austin':
    image2 = Image.open("./plots/Austin.png")
elif nm2 == 'Louisville':
    image2 = Image.open("./plots/Louisville.png")
elif nm2 == 'Oklahoma City':
    image2 = Image.open("./plots/OKC.png")
elif nm2 == 'Portland':
    image2 = Image.open("./plots/Portland.png")
elif nm2 == 'Buffalo':
    image2 = Image.open("./plots/Buffalo.jpeg")

col1.image(image1)
col2.image(image2)

#create columns for row 2
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
col1.metric(label = "Overall Rank", value = str(market_df1.iloc[0]['rank']))
col2.metric(label = "2010 Population", value = str("{:,}".format(market_df1.iloc[0]['pop2010'])))
col3.metric(label = "2021 Population", value = str("{:,}".format(market_df1.iloc[0]['pop2021'])), 
                    delta = str("{:.2f}".format(tm_pop_change1)) + '% since 2010')
col4.metric(label = "Population Growth Rank", value = tm_growth_rank1.replace('.0',''))
        
col5.metric(label = "Overall Rank", value = str(market_df2.iloc[0]['rank']))
col6.metric(label = "2010 Population", value = str("{:,}".format(market_df2.iloc[0]['pop2010'])))
col7.metric(label = "2021 Population", value = str("{:,}".format(market_df2.iloc[0]['pop2021'])), 
                    delta = str("{:.2f}".format(tm_pop_change2)) + '% since 2010')                   
col8.metric(label = "Population Growth Rank", value = tm_growth_rank2.replace('.0',''))


#create columns for row 3                   
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)                 
col1.metric(label = "Per Capita Income", value = ("$" + str("{:,}".format(tm_income1))))
col2.metric(label = "# Pro Sports Teams:", value = str(market_df1.iloc[0]['pro_teams']))
col3.metric(label = "# Stadiums (seats > 25K)", value = str(market_df1.iloc[0]['stadium_count']))

col5.metric(label = "Per Capita Income", value = ("$" + str("{:,}".format(tm_income2))))
col6.metric(label = "# Pro Sports Teams:", value = str(market_df2.iloc[0]['pro_teams']))
col7.metric(label = "# Stadiums (seats > 25K)", value = str(market_df2.iloc[0]['stadium_count']))

#respective education population
pie_values1 = (market_df1.iloc[0][74:78])
pie_values2 = (market_df2.iloc[0][74:78])

#insert horizontal line
st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.markdown("### ** Education breakdown **") 
col2.markdown("### ** Education breakdown **")

#create columns for pie charts
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)  

fig = summary_poster(pie_values1)
col1.write(fig)

fig = summary_poster(pie_values2)
col5.write(fig)

#insert horizontal line
st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.write("")

#Market comparison section
st.markdown("### ** Target Market Comparisons **")
st.write('Select one or more of the target markets to see how they compare:')
select_market = []

#build multi-select drop down
cities = st.multiselect("Choose Cities", list(df_tm1.index),["Austin","San Antonio","Louisville","Portland","Oklahoma City","Buffalo"])

if not cities:
    st.error("Please select at least one city.")

#build income chart
#else:
    df_inc = df_tm1.loc[cities, 'per_capita_income']
    df_21pop = df_tm1.loc[cities, 'pop2021']
    df_pop_growth = df_tm1.loc[cities, 'growth_10']
    col1, col2, col3, col4 = st.columns(4)
    col1.subheader('Per Capita Income')
    col1.bar_chart(df_inc)
    col2.subheader('2021 Population')
    col2.bar_chart(df_21pop)
    col3.subheader('% Population Growth Since 2010')
    col3.bar_chart(df_pop_growth)

st.write("")

#insert horizontal line
st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

#build map section
st.markdown("### ** NFL & Target City Markets **")

#create filter buttons for map
st.write('Select a filter for the map, then click on the markers to see demographic info:')

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)  
if col1.button('NFL Markets Only'):
    map_filter= 'NFL'
    map_markets(map_filter)
if col2.button('Target Markets Only'):
    map_filter = 'Target'
    map_markets(map_filter)
if col3.button('NFL and Target Markets'):
    map_filter = 'Both'
    map_markets(map_filter)


#<p style="text-align: center;"><iframe src={logo}embed width="240" height="290" frameborder="0" scrolling="auto" allowtransparency="true"></iframe>
