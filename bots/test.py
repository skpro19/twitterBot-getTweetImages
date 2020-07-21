import requests
 
response  = requests.get("https://api.github.com")

print(f"response: {response} Typeof(response): {type(response)} ")

print(f"status code for response: {response.status_code}")

#print(response.content)

#print(response.text)

response_json = response.json()


def printResponseJSON(response):

    response_json = response.json()

    for key in response_json:
        print(f"{key} -> {response_json[key]}")

def printResponseHeader(response):
    
    print(f"Printing response headers -> ")
    response_header = response.headers
    
    for key in response_header:
        print(f"{key} -> {response_header[key]}")


printResponseHeader(response)



