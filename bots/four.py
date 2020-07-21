import yagmail 


def sendMailWithAttachments(receiver, attachments, tweet_link):
    

    try:
        
        #receiver  = shubhamkumarpro1@gmail.com
        
        #print(f'tweet_link: {tweet_link}')

        body_content = f'Images attched in the tweet - {tweet_link}' 
        
        #Have removed email and password due to security reasons
        yag = yagmail.SMTP(user="", password = "")

        yag.send(to=receiver, subject="Attached images from the tweet!", contents =  body_content, attachments = attachments)

        print("Email sent successfully")
        
        return True

    except Exception as e:
        
        print(f'Exception {e}')
        print("Email was not sent")


