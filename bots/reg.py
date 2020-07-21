import re 


a= re.search(r'[a-z0-9]+@[a-z]+\.com', 'testemail@gmail.com')

if a: 
    print("Match found")

else:

    print("No match found")

print(a.group())


