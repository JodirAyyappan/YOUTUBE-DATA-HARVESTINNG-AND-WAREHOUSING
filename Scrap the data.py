import streamlit as st
import mysql.connector
import pandas as pd
import googleapiclient.discovery
import re
import numpy as np


id_input = st.text_input("Enter the Channel Id", "Channel Id")
scrap = st.button("Scrap Data")


if scrap:
    
    api_service_name = "youtube"
    api_version = "v3"
    
    api_key = "AIzaSyA8Hn7S3E5BcfpNvX13TjBosf5xh8pnl4Y"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
   
    def channel_data(channel_id):
        request = youtube.channels().list(part="snippet,contentDetails,statistics",
                                          id=channel_id)
        response = request.execute()

        for item in response['items']:
            data = dict(channelName=item['snippet']['title'],
                        channelId=item['id'],
                        channelDescription=item['snippet']['description'],
                        channelPub=item['snippet']['publishedAt'],
                        channelPlaylistId=item['contentDetails']['relatedPlaylists']['uploads'],
                        channelViewcount=item['statistics']['viewCount'],
                        channelSubcount=item['statistics']['subscriberCount'],
                        channelVidcount=item['statistics']['videoCount'])
        return data

    def video_ids(channel_id):
        video_id = []

        request = youtube.channels().list(part="contentDetails",
                                              id=channel_id)
        response = request.execute()

        play_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        #correct playlistid

        request = youtube.playlistItems().list(
                part="snippet",
                playlistId=play_id,
                maxResults=50
        )
        response = request.execute()

        for item in response['items']:
            video_id.append(item['snippet']['resourceId']['videoId'])

        next_Page_Token = response.get('nextPageToken')

        while next_Page_Token is not None:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=play_id,
                maxResults=50,
                pageToken=next_Page_Token
            )
            response = request.execute()

            for item in response['items']:
                video_id.append(item['snippet']['resourceId']['videoId'])

            next_Page_Token = response.get('nextPageToken')
        return video_id



    # converting pt format of x into timestamp.
    def ptformat(i):
        x=re.findall('\d+', i)

        if(len(x)==2):
            if(len(x[0])==2 and len(x[1])==2):
                s=f"00:{x[0]}:{x[1]}"

            elif(len(x[0])==1 and len(x[1])==1):
                s=f"00:0{x[0]}:0{x[1]}"

            elif(len(x[0])==1 and len(x[1])==2):
                s=f"00:0{x[0]}:{x[1][0]}{x[1][1]}"

            elif(len(x[0])==2 and len(x[1])==1):
                s=f"00:{x[0][0]}{x[0][1]}:0{x[1][0]}"


        elif(len(x)=='3'):
            if(len(x[0])==2 and len(x[1])==2 and len(x[2])==2):
                s=f"{x[0]}:{x[1]}:{x[2]}"

            elif(len(x[0])==1 and len(x[1])==1 and len(x[2])==1):
                s=f"0{x[0]}:0{x[1]}:0{x[2]}"

            elif(len(x[0])==1 and len(x[1])==1 and len(x[2])==2):
                s=f"0{x[0]}:0{x[1]}:{x[2]}"

            elif(len(x[0])==1 and len(x[1])==2 and len(x[2])==1):
                s=f"{x[0]}:{x[1]}:0{x[2]}"

            elif(len(x[0])==1 and len(x[1])==2 and len(x[2])==2):
                s=f"{x[0]}:{x[1]}:{x[2]}"

            elif(len(x[0])==2 and len(x[1])==1 and len(x[2])==1):
                s=f"{x[0]}:0{x[1]}:0{x[2]}"

            elif(len(x[0])==2 and len(x[1])==1 and len(x[2])==2):
                s=f"{x[0]}:0{x[1]}:{x[2]}"

            elif(len(x[0])==2 and len(x[1])==2 and len(x[2])==1):
                s=f"{x[0]}:{x[1]}:0{x[2]}"


        else:
            if(len(x[0])==1):
                s=f"00:00:0{x[0]}"

            elif(len(x[0])==2):
                s=f"00:00:{x[0]}"


        return s


    def video_info(video_id):
        video_data = []
        for video in video_id:
            request = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=video
                )
            response = request.execute()
            for item in response['items']:
                data = dict(videoId=item['id'],
                            channelId=item['snippet'].get('channelId'),
                            #Channel_Name=item['snippet']['channelTitle'],
                            videoName = item['snippet']['title'],
                            videoDescription = item.get('description'),

                            #Tags = item['snippet'].get('tags'),
                            publishedAt=item['snippet'].get('publishedAt'),
                            viewCount=item['statistics'].get('viewCount'),
                            likeCount=item['statistics'].get('likeCount'),
                            favouriteCount=item['statistics'].get('favoriteCount'),
                            commentCount=item['statistics'].get('commentCount'),
                            Duration=ptformat(item['contentDetails'].get('duration')),


                            #Thumbnail=item['snippet'].get('thumbnails'),
                            captionStatus=item['contentDetails'].get('caption')
                   )
                video_data.append(data)
        return video_data



    def comment_info(video_id):
        comment_data = []

        try:
            for video_id in video_id:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100
                )
                response = request.execute()

                for item in response['items']:
                    data = dict(commentId=item['snippet']['topLevelComment']['id'],
                                videoId=item['snippet']['topLevelComment']['snippet']['videoId'],
                                commentText=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                                commentAurthor=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                commentPublishedAt=item['snippet']['topLevelComment']['snippet']['publishedAt'])

                    comment_data.append(data)
        except:
            None

        return comment_data
    
    def youtube_channel(channel_id):
        channelData = channel_data(channel_id)
        videoIds = video_ids(channel_id)
        videoInfo = video_info(videoIds)
        commentInfo = comment_info(videoIds)
        return channelData, videoIds, videoInfo, commentInfo

    output=youtube_channel(id_input)
        
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ScienceBase%5",
        database="YOUTUBE_DHW"
    )

    cursor = mydb.cursor()

    # creating channel details
    try:

        cursor.execute("create table channel_details(channelName varchar(255), channelId varchar(255), channelDescription text, channelPub varchar(255) , channelPlaylistId varchar(255), channelSubcount int, channelViewcount int, channelVidcount int, primary key(channelId))")
        mydb.commit()

    except:
        print("channel_details table already exists!")
        
    #inserting channel values

    try:
        query = "insert into channel_details(channelName, channelId, channelDescription, channelPub, channelPlaylistId, channelSubcount, channelViewcount, channelVidcount) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        value = tuple(output[0].values())
        cursor.execute(query,value)
        mydb.commit()
    except:
        print("Duplicate entry!")
    
    # display channel values
    cursor.execute("select * from channel_details")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["channelName", "channelId", "channelDescription", "channelPub", "channelPlaylistId",
                                        "channelSubcount", "channelViewcount", "channelVidcount"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    
    # create video table
    try:
        cursor.execute("create table video_info(videoId varchar(255),channelId varchar(255), videoName varchar(255),videoDescription text,publishedAt varchar(255),viewCount int,likeCount int,favouriteCount int,commentCount int,Duration varchar(255),captionStatus varchar(255),primary key(videoId),foreign key(channelId) references channel_details(channelId))")
        mydb.commit()
    except:
        print("video_info table already exist!")
      
    # insert video information

    try:
        query = "insert into video_info(videoId, channelId, videoName, videoDescription, publishedAt, viewCount, likeCount,favouriteCount, commentCount, Duration, captionStatus) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for i in range(len(output[1])):
            value = tuple(output[2][i].values())
            cursor.execute(query,value)
            mydb.commit()
    except:
        print("Duplicate entry!")

    # display video information
    cursor.execute("select * from video_info")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["videoId", "channelId", "videoName", "videoDescription", "publishedAt", "viewCount", "likeCount",
                                        "favouriteCount", "commentCount", "Duration", "captionStatus"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail
    
    
    # create comment table
    try:
        cursor.execute("create table comment_info(commentId varchar(255),videoId varchar(255),commentText text,commentAurthor varchar(255),commentPublishedAt varchar(255), foreign key (videoId) references video_info(videoId))")
        mydb.commit()
    except:
        print("comment_info table already exist")
    
    # insert comment information

    try:
        query = "insert into comment_info(commentId,videoId,commentText,commentAurthor,commentPublishedAt) values(%s,%s,%s,%s,%s)"
        for i in range(len(output[3])):
            value = tuple(output[3][i].values())
            cursor.execute(query,value)
            mydb.commit()
    except:
        print("Duplicate entry!")
        
    # display comment information
    cursor.execute("select * from comment_info")
    op=cursor.fetchall()
    ch_detail=pd.DataFrame(op, columns=["commentId", "videoId", "commentText", "commentAurthor", "commentPublishedAt"])
    ch_detail.index=np.arange(1, len(ch_detail)+1)
    ch_detail

    
    st.success("Data Scrapped Successfully!")
    


