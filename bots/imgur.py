import requests
import base64
import json
import configparser


## Important variables used
    
client_id = "101a0efabb00a9f"

client_secret  = "40ddd04c5cef9ce63774d945884d1184377da184"

access_token = "503607b9cc26bdfde9c23974dbb46f63260b9afe"

refresh_token = "e29865e0b8829c2a91990a7fa04ff7db72706ddf"

username = 'skpro19'

baseUrl = 'https://api.imgur.com/'

anonymousAlbumDict = {}

def printJsonDict(response_json):
    
    print("  ")
    print(f'Printing response_json dict')
    for key in response_json:
        print(f'{key} -> {response_json[key]}')


def createComment(image_id):
    
    print("Trying to create a new comment")
    
    url = 'https://api.imgur.com/3/comment'

    payload = {'image_id' : image_id , 'comment':'This is my first comment!' }

    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.request("POST" , url , headers = headers, data = payload)

    print(f'response: {response} type(response): {type(response)}')
    
    
    return response 


"""
* Create a new Anonymous  album
* Update the anonymous album
* Upload an image in the album
* Uplad an image without any album
"""

#Working with authentication
def getAllImages():
   
    url = 'https://api.imgur.com/3/account/{username}/images/'

    headers = { 'Authorization': f'Bearer {access_token}' }

    response = requests.request("GET" , url)
    
    return response 

"""
List of available functions->
*   printJsonDict

"""

def getMyImages():

    url = f'{baseUrl}/3/account/me/images'

    headers = {'Authorization' : f'Bearer {access_token}' }
    #headers = {'Authorization': f'Client-ID {client_id}' }


    response = requests.request("GET" , url , headers = headers)

    return response


def getMyAlbumsWithoutAuthentication(): 

    url = f'{baseUrl}/3/account/{username}/albums/'

    headers = {'Authorization': f'Client-ID {client_id}' }

    response = requests.request("GET", url , headers = headers)

    return response


def getAlbumCountUnauthenticated():

    url = f'{baseUrl}/3/account/{username}/albums/count'

    headers = {'Authorization' : f'Client-ID {client_id}' }
    
    response = requests.request("GET", url, headers = headers)

    return response 

def getAlbumCountAuthenticated(): 

    url = f'{baseUrl}/3/account/{username}/albums/count'

    headers = {'Authorization' : f'Bearer {access_token}' }
    
    response = requests.request("GET", url, headers = headers)

    return response 



def generateAccessToken():
   
    url = f'{baseUrl}/oauth2/token'

    payload = { 'refresh_token' : refresh_token, 'client_id' : client_id, 'client_secret' : client_secret , 'grant_type': 'refresh_token' }

    response = requests.request("POST" , url, data = payload)

    return response

#Working with authentication
def getAlbumImages(album_id): 
    
    url = f"{baseUrl}/3/album/{album_id}/images"

    headers = {'Authorization' : f'Client-ID {client_id}' }
    
    response = requests.request("GET", url , headers = headers)

    return response

#Working with authentication
def addImageToAlbum(album_id, img_ids):

    url = f"{baseUrl}/3/album/{album_id}/add"
    
   # payload = { 'ids[]' : img_ids }

    payload = { 'ids[]' : img_ids }

    headers = {'Authorization': f'Bearer {access_token}' }
    
   # headers = {'Authorization' : f'Client-ID {client_id}' }
    
    response = requests.request("POST", url ,data = payload,  headers = headers)

    return response


#Working - works only with authentication
def uploadImage(img_url):
    
    url = f'{baseUrl}/3/upload'
    
    headers = {'Authorization' : f'Bearer {access_token}' }
    

    payload = {'image' : img_url , 'type' : 'url' , 'title' : 'cuteDoggo' } 

    response = requests.request("POST", url , headers = headers, data = payload)

    return response 

#Not to be confused with addImageToAlbum()
def uploadImageToAlbum(img_url, deletehash):
    
    url = f'{baseUrl}/3/upload'
    
    headers = {'Authorization' : f'Bearer {access_token}' }
    

    payload = {'image' : img_url , 'type' : 'url' , 'title' : 'cuteDoggo', 'album' : deletehash } 

    response = requests.request("POST", url , headers = headers, data = payload)

    return response 



def createAnonymousAlbum():
    
    url = f'{baseUrl}/3/album'

    payload = {'title' : 'AnonymousTwo' , 'description' : 'This is the second anonymous  album' }
    
    headers = {'Authorization' : f'Client-ID {client_id}' }

    respone = requests.request("POST", url, headers = headers, data = payload)

    return respone 





#Works - Albums will be reflected in the imgur profile only when authenticaiton is used
def createAlbum(): 
    
    url = f'{baseUrl}/3/album'
    
    payload = {'title' : 'Fourth Album' , 'description' : 'This is the fourth album' }

    headers = {'Authorization':  f'Bearer {access_token}' }
    
    respone = requests.request("POST", url, headers = headers, data = payload)

    return respone 


def setTokens(filename):
    
    config = configparser.ConfigParser()
    config.read(filename)
    access_token = config['tokens']['access_token']
    refresh_token = config['tokens']['refresh_token']
    client_secret = config['tokens']['client_secret']
    client_id = config['tokens']['client_id']
    
    print("Tokens were successfully set")
    
    #print("access_token: " , access_token)



"""
Few important tips- 
* Use getMyImages() to check with Authentication is working or not

* Functions that are working-
    - uploadImage()


"""


albumId_dict = { 'one' : 'P0pMqKp' , 'two': 'cF8TEBV', 'three' : 'dC3lPvq' }

anonymousAlbumId_dict = {} 


#albumThree
album_id = 'dC3lPvq'

image_id = 'Owl2KGB'


img_url = 'https://www.dogstrust.org.uk/help-advice/_images/164742v800_puppy-1.jpg'

img_ids = ['J8nu91G', 'Ll4bC9q']

def main():
    
    setTokens('config.ini') 

    res = createAnonymousAlbum()

    print(res.status_code)

    res_json = res.json()

    print(res_json)

    for key in res_json['data']:
        
        anonymousAlbumDict[key] = res_json['data'][key]

    print("Printing anonymousAlbumDict => ")
    for key in anonymousAlbumDict:
        print(f"{key} => {anonymousAlbumDict[key]}")


    img_urls = ['http://pbs.twimg.com/media/EbcWU24WkAAo97j.jpg', 'http://pbs.twimg.com/media/EbcWVwrWsAMt_MO.jpg',  'http://pbs.twimg.com/media/EbcWWlOWkAIQehn.jpg', 'http://pbs.twimg.com/media/EbcWXQCXgAANS3M.jpg']

    res_list = [] 

    for idx, img_url in enumerate(img_urls): 
        
        print("idx: ", idx)
        res = uploadImageToAlbum(img_url, anonymousAlbumDict['deletehash']) 
        res_list.append(res)


    #print(res_list[0].json())

    anonAlbumId = anonymousAlbumDict['id']

    res = getAlbumImages(album_id)

    #print(res.status_code)

    res_json = res.json()

    #print(res.json())

    img_list= []

    for dict in res_json['data']:
        
        img_list.append(dict['link'])



    print("Printing img_list \n")
    print(img_list)


if __name__ == "__main__" :
    main()





