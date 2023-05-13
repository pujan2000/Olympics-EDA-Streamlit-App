import numpy as np

#Getting a dataframe with regions and medal types
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

#function to get the list of countries and years to put inside the drop down list.
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def fetch_medal_tally(df,country,year):
    medal_df = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)

    return x

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates([col,'Year'])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index':'Editions','Year':col}, inplace = True)
    return nations_over_time

#Getting most successful athletes sportswise
def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal']) # We donot need athletes without any medal
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport] #filtering data with sports
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'}, inplace=True)
    return x


# Country Wise Analysis

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])  # Removing Nan Values
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    final_df = temp_df[temp_df['region'] == country].groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])  # Removing Nan Values
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    return new_df

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal']) # We donot need athletes without any medal
    temp_df = temp_df[temp_df['region'] == country] #filtering data with sports

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on = 'index',right_on = 'Name',how = 'left')[['index','Name_x','Sport']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'}, inplace = True)
    return x

# Athlete wise Analysis

def weight_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna("No Medal", inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


