import pandas as pd
def preprocess(df, region_df):
    #Filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    #merging with region dataframe
    df = df.merge(region_df, on='NOC', how='left')
    #removing duplicate rows
    df.drop_duplicates(inplace=True)
    #one hot encoding medals
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df


