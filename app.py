import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import helper, preprocessor
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympic Analysis")
st.sidebar.image('https://stillmed.olympics.com/media/Images/OlympicOrg/IOC/The_Organisation/The-Olympic-Rings/Olympic_rings_TM_c_IOC_All_rights_reserved_1.jpg')
#Showing the side bar options and assigning the name to user_menu
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

# Showing the preprocessed dataframe
# st.dataframe(df)

#Medal Tally Option
#Showing the medal tally as per the region only when Medal Tally is selected
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df) #drop down list

    selected_year = st.sidebar.selectbox("Select Year", years)  #sidebox stands for drop down list
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_country,selected_year)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' performance in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)


#Overall Analysis Option
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Cities")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Athletes")
        st.title(athletes)

    with col3:
        st.header("Nations")
        st.title(nations)

    st.title("Participating Nations over Time")
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Editions', y="region")
    st.plotly_chart(fig)

    st.title("Events over Time")
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='Editions', y="Event")
    st.plotly_chart(fig)

    st.title("Athletes over Time")
    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x='Editions', y="Name")
    st.plotly_chart(fig)

    st.title("No. of Events over Time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns = 'Year',values = 'Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)

    x = helper.most_successful(df, selected_sport)
    st.table(x)

#Country wise Analysis
if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + "Country-wise Medal Tally per year")
    st.plotly_chart(fig)

    st.title(selected_country + "excels in the following sports")
    fig,ax = plt.subplots(figsize=(20,20))
    new_df = helper.country_event_heatmap(df,selected_country)
    ax = sns.heatmap(new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0),annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

#Athlete wise Analysis

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()  # All the ages
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()  # Ages only of athletes with Gold Medal
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()  # Ages only of athletes with Silver Medal
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()  # Ages only of athletes with Broze Medal

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age', 'Gold Medallist', 'Silver Medallist', 'Bronze Medallist'], show_hist=False,
                             show_rug=False)
    fig.update_layout(autosize=False,width=800,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    Age_dist = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting',
                     'Hockey', 'Rowing', 'Shooting', 'Boxing', 'Cycling', 'Diving', 'Tennis', 'Golf', 'Archery',
                     'Volleyball', 'Table Tennis', 'Baseball', 'Triathlon',
                     'Rugby', 'Polo', 'Ice Hockey']


    def Medal_type(medal):
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            Age_dist.append(temp_df[temp_df['Medal'] == medal]['Age'].dropna())
            name.append(sport)
        return Age_dist, name


    st.title("Distribution of Age for each Sport")
    medal_list = ['Gold','Silver'] #Lets focus on only Gold and Silver Medals
    selected_medal = st.selectbox('Select Medal', medal_list)
    Age_dist, name = Medal_type(selected_medal)

    fig = ff.create_distplot(Age_dist, name, show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    st.title("BMI of each Athlete for each Sport")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_height(df,selected_sport)
    # plt.figure(figsize=(10, 10))
    fig,ax = plt.subplots(figsize = (20,20))
    ax = sns.scatterplot(data = temp_df,x='Weight',y='Height', hue = temp_df['Medal'],style = temp_df['Sex'],s=100)
    st.pyplot(fig)


    Male = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    Female = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = Male.merge(Female, on='Year')
    final.head()
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    st.title("Gender-wise Participation over the Years")
    fig = px.line(final, x='Year',y=['Male','Female'])
    st.plotly_chart(fig)