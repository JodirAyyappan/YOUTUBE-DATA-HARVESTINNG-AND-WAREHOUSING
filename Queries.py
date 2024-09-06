import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np

option = st.selectbox("Select your query", ("1. What are the names of all the videos and their corresponding channels?",
                      "2. Which channels have the most number of videos, and how many videos do they have?",
                      "3. What are the top 10 most viewed videos and their respective channels?",
                      "4. How many comments were made on each video, and what are their corresponding video names?",
                      "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                      "6. What is the total number of likes for each video, and what are their corresponding video names?",
                      "7. What is the total number of views for each channel, and what are their corresponding channel names?",
                      "8. What are the names of all the channels that have published videos in the year 2022?",
                      "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                      "10. Which videos have the highest number of comments, and what are their corresponding channel names?"))

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
)

cursor = mydb.cursor()

if(option == "1. What are the names of all the videos and their corresponding channels?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select c.channelName, v.videoName from channel_details as c inner join video_info as v on c.channelId = v.ChannelId"                    )
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op,columns=["Channel Name", "Video Name"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
   
    
if(option == "2. Which channels have the most number of videos, and how many videos do they have?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select c.channelName, count(v.videoId) from channel_details as c inner join video_info as v on c.channelId =                            v.channelId group by v.channelId order by count(v.videoId) desc limit 1")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Channel Name", "Number of Videos"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    

if(option == "3. What are the top 10 most viewed videos and their respective channels?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select c.channelName , v.videoName from channel_details as c inner join video_info as v on c.channelId = v.channelId order by v.viewCount desc limit 10")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Channel Name", "Video Name"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    
    
if(option == "4. How many comments were made on each video, and what are their corresponding video names?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select videoName, commentCount from video_info")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Video Name", "Number of Comments"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    
    
if(option == "5. Which videos have the highest number of likes, and what are their corresponding channel names?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select c.channelName, v.videoName, v.likeCount from channel_details as c inner join video_info as v on c.channelId=v.ChannelId order by v.likeCount desc limit 10;")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Channel Name", "Video Name", "Number of Likes"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    
    
if(option == "6. What is the total number of likes for each video, and what are their corresponding video names?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select videoName, likeCount from video_info")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Video Name", "Number of Likes"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    
    
if(option == "7. What is the total number of views for each channel, and what are their corresponding channel names?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select c.channelName, sum(viewCount) as Total_Views from channel_details as c inner join video_info as v on                              c.channelId = v.channelId group by c.channelName")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Channel Name", "Total Views"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    
    
if(option == "8. What are the names of all the channels that have published videos in the year 2022?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select distinct c.channelName from channel_details as c inner join video_info as v on c.channelId = v.ChannelId where  extract(year from v.publishedAt) = 2022")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Channel Name"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    

if(option == "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select c.channelName, sec_to_time(avg(time_to_sec(v.Duration))) as Average_Duration from channel_details as c inner                        join video_info as v on c.channelId = v.channelId group by c.channelName")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Channel Name", "Average time of a video"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    
    
if(option == "10. Which videos have the highest number of comments, and what are their corresponding channel names?"):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()
    
    cursor.execute("select c.channelName, max(v.commentCount) as Maximum_Comment from channel_details as c inner join video_info as v on                        c.channelId = v.channelId group by c.channelName")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["Channel Name", "Max Comments"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    


    

    






 
