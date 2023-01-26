# -*- coding: utf-8 -*-
pip install git+https://github.com/JustAnotherArchivist/snscrape.git
#Importing required libraries
import streamlit as st
import pandas as pd
import snscrape.modules.twitter as sntwitter
import pandas as pd
import time

#title of the page
st.title("Twitter Data Scraping:clipboard:")

#Initiating sidebar, input widgets and title
title=st.sidebar.title(":mag_right: Search Bar")

#search keyword or hashtag
#from date, to date 
keyword= st.sidebar.text_input("Search Keyword or hashtag")
f_date=st.sidebar.date_input("From Date")
to_date=st.sidebar.date_input("To Date")
q=f"{keyword} since:{f_date} until:{to_date}"

#select tweet count range
tweet_count=st.sidebar.number_input("Tweet Count to be scraped",min_value=0,max_value=1000)

def convert_df_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
def convert_df_json(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_json().encode('utf-8')

#creating list to append tweet data
tweet_list1=[]

#main block
#dataframe,
#download csc
#download json
#upload data to mongodb
try:
    with st.spinner("Collecting Data..."):
        time.sleep(5)
    #Using twittersearchscrape to scrape data and appemnd tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
        if i>tweet_count:
            break
        tweet_list1.append([tweet.date,tweet.id,tweet.url,tweet.content,tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount])

    tweet_df=pd.DataFrame(tweet_list1,columns=['Datetime','Tweet_id','URL','Text','Username','Reply Count','Retweet Count','Language','Source','Like Count'])
    st.dataframe(tweet_df)
    tweet_df['Datetime'] = tweet_df['Datetime'].astype(str)
    tweet_dic=tweet_df.to_dict('records')
    csv =convert_df_csv(tweet_df)
    json=convert_df_json(tweet_df)
    st.sidebar.title("Download Data")
    csv_button=st.sidebar.download_button(label="Download data as CSV",data=csv,file_name='tweet_data.csv',mime='text/csv')
    if csv_button:
        st.sidebar.success("csv file Downloaded Successfully!")
    json_button=st.sidebar.download_button(label="Download data as json",data=csv,file_name='tweet_data.json',mime='text/json')
    if json_button:
        st.sidebar.success("json file Downloaded Successfully!")
    
    st.sidebar.title("Upload to Mongodb")
    result=st.sidebar.button("Upload")
    if result:
        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["twitterdb"]
        mycol = mydb[q]
        x = mycol.insert_many(tweet_dic)
        dblist = myclient.list_database_names()
        collection_list=mydb.list_collection_names()
        if "twitterdb" in dblist:
          if q in collection_list:
              st.sidebar.success("Uploaded Successfully!")        
          
    
    st.success("The Data has been successfully scrapped!:heart:")
    st.success("You can download or upload scrapped data in the sidebar")

except:
    st.markdown("Please :red[enter] the keyword/Hashtag to scrap")



    

