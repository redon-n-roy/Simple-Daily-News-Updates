import json
import requests
from datetime import datetime
import boto3
import os
from botocore.exceptions import ClientError

URL = "https://newsdata.io/api/1/news?apikey="+os.environ['KEY']

def politicalNews():
    temp = requests.get(URL+'&country=in&category=politics').json()['results']
    data = "\n".join(interData["title"] for interData in temp)
    return(data +".")

def topNews():
    temp = requests.get(URL+'&country=in&domain=thehindu,indianexpress,ndtv,hindustantimes,theindiatimes&category=top').json()['results']
    data = "\n".join(interData["title"] for interData in temp)
    return(data +".")

def localNews():
    temp = requests.get(URL+'&country=in&q=kerala%20OR%20kottayam').json()['results']
    data = ".\n".join(interData["title"] for interData in temp)
    return(data +".")

def sportsNews():
    temp = requests.get(URL+'&country=in&category=sports').json()['results']
    data = "\n".join(interData["title"] for interData in temp)
    return(data +".")

def worldNews():
    temp = requests.get(URL+'&category=world').json()['results']
    data = "\n".join(interData["title"] for interData in temp)
    return(data +".")

def lambda_handler(event, context):
    SENDER = "FROM ADDRESS"
    RECIPIENT = "TO ADDRESS(can be a list)"
    AWS_REGION = "YOUR REGION"
    SUBJECT = "Daily News Update - ("+datetime.today().strftime('%d-%m-%Y')+")"
    BODY_TEXT = "Top News\n\n"+topNews()+"\n\nLocal News\n\n"+localNews()+"\n\nPolitical News\n\n"+politicalNews()+"\n\nWorld News\n\n"+worldNews()+"\n\nSports News\n\n"+sportsNews()             
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Email sent!')
    }