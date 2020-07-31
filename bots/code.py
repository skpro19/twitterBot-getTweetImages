import tweepy
import json
import sys
import urllib.request
import configparser
import re
import os
from shutil import rmtree
from four import sendMailWithAttachments
import time
import logging


def getAttachedImageUrls(tweet):
    
    img_urls = []

    tweet_json = tweet._json

    for key in tweet_json:
        if key == "extended_entities":
            #print("key: ", key)
            #print("type(val):\n\n ", type(tweet_json[key]))
            
            
            media_dict = tweet_json[key]["media"]
            
           # print("type(media_dict): ", type(media_dict))
            
            for media in media_dict:
               # print(media)
                #print("\n\n")
                img_urls.append(media['media_url'])

    return img_urls  


#Have removed the following keys due to security reasons
consumer_key= "####"
consumer_secret_key = "####"
access_token = "##############"
access_token_secret = "#########"





def extractEmail(text):

    a= re.search(r'[a-z0-9]+@[a-z]+\.com', text)
    return a.group()



def check_mentions(api, since_id):
   
    cnt = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
        
        cnt=  max(cnt, tweet.id)        

        print(f'tweet_id: {tweet.id}')

        if tweet.in_reply_to_status_id is None:
           #print("This looks like an original tweet --- SKIPPING")
           continue
       
        parent_id = tweet.in_reply_to_status_id
        
        parent_tweet = None

        try:
            parent_tweet = api.get_status(id = parent_id , tweet_mode= 'extended')
        
        except Exception as e:
            print ("Excpetion in getting parent tweet")
            
            
        if parent_tweet is None:
            continue
    
        img_urls_list = getAttachedImageUrls(parent_tweet)
            
        img_count = len(img_urls_list)
        
        if img_count < 1:
            continue
            
        emailAddress = -1

        try: 
           emailAddress = extractEmail(tweet.text.lower())
        except:
            print('No valid email found')

        if emailAddress == -1:
            continue
        
        attachments = []
            
        curr_dir = os.getcwd()

        final_dir = os.path.join(curr_dir, r'images')
            
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        for idx, url in enumerate(img_urls_list):
                
            loc = f'images/{idx}.jpg'
            urllib.request.urlretrieve(url, loc)
            attachments.append(loc)
            
        receiver = emailAddress
        print("receiver: " , receiver)
        emailStatus = False
        emailStatus = sendMailWithAttachments(receiver, attachments, parent_tweet._json['full_text'])

        if emailStatus == True:

            print('Mission Accomplished')
            
            try:

                api.update_status(status = f'Images sent successfully to  {emailAddress}' , in_reply_to_status_id = tweet.id)
            
            except Exception as e:
                print(f'Exception -> {e}')
        
        else:

            print('Oh, crap!')

        rmtree(final_dir)
    
    #return since_id
    return cnt

def getVal(filename, section, key):

    config = configparser.ConfigParser()
    config.read(filename)
    return config[section][key]

def setVal(filename, section, key,  val):
    
    config = configparser.ConfigParser()
    config[section] = {}
    config[section][key] = val
    
    with open(filename, 'w') as configfile:
        config.write(configfile)

def main():
    
    filename = 'config.ini'
   
    #initializeCredentials(filename, 'tweepy')
   
    since_id = int(getVal(filename, 'tweepy' ,'since_id'))
    
    print('access_token: ', access_token)
    print('access_token_secret: ', access_token_secret)
    print('consumer_key: ', consumer_key)
    print('consumer_secret_key: ', consumer_secret_key)

    logger= logging.getLogger()

    

    while True: 
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
        auth.set_access_token(access_token, access_token_secret)


        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        try:
            api.verify_credentials()
            print("Authentication OK")
            logger.info('Authentication successful')
        except Exception as e:
            logger.error('Error creating API')
            logger.error(f'errror -> {e}')
    
        
        print('Old since_id: ' , since_id)

        since_id  = check_mentions(api, since_id)
        
        setVal(filename, 'tweepy' , 'since_id' , f'{since_id}')

        print('New since_id: ', since_id)

        time.sleep(30)          
        
        
if __name__ == "__main__":
    main()



