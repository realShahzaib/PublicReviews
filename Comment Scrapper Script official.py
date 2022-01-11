from apiclient.discovery import build
import json
from csv import writer
from apiclient.discovery import build
from urllib.request import urlopen
from urllib.parse import urlencode


def build_service():
#You should access to YoutubeApi to obtain the key
    key = "AIzaSyATHDMtQktlGtOzb94ObrGB75p32RUjv1o"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    return build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=key)


    
#example youtube video : https://www.youtube.com/watch?v=t0UmUGGVgsU
def get_comments(part='snippet', 
                 maxResults=100, 
                 textFormat='plainText',
                 order='time',
                 videoId='heHbWNE-8x0',
                 csv_filename="data"):

    #3 create empty lists to store desired information
    comments = []
    authors =  [] 
    sources =  []
    dates  =   []
    # build our service from path/to/apikey
    service = build_service()
    
    #4 make an API call using our service
    response = service.commentThreads().list(part=part, maxResults=maxResults, textFormat=textFormat, order=order, videoId=videoId).execute()
                 
    while response: # this loop will continue to run until you max out your quota
                 
        for item in response['items']:
            #4 index item for desired data features
            comment1 = item['snippet']['topLevelComment']['snippet']
            comment = comment1['textDisplay'].replace('\n', '')
            author = comment1['authorDisplayName']
            date = comment1['publishedAt']
            source = comment1['videoId']
            
            #4 append to lists
            comments.append(comment)
            authors.append(author)
            sources.append(source)
            dates.append(date)
         

            #7 write line by line
            with open('data.csv','a+',encoding='utf-8-sig') as f:
                # write the data in csv file with colums(source, date, author, text of comment)
                csv_writer = writer(f)
                csv_writer.writerow([source,date,author,comment])
                
             #8 check for nextPageToken, and if it exists, set response equal to the JSON response
        if 'nextPageToken' in response:
            response = service.commentThreads().list(
                part=part,
                maxResults=maxResults,
                textFormat=textFormat,
                order=order,
                videoId=videoId,
                pageToken=response['nextPageToken']
            ).execute()
        else:
            break
        

    #9 return our data of interest
    return {
        'Sources' : sources,
        'Date': dates,
        'Author name': authors,
        'Comments': comments,
    }



get_comments()