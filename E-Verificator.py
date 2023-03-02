import re
import os
import time
import random
import string
import requests

print("""
███████╗    ██╗   ██╗███████╗██████╗ ██╗███████╗██╗ ██████╗ █████╗ ████████╗ ██████╗ ██████╗ 
██╔════╝    ██║   ██║██╔════╝██╔══██╗██║██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
█████╗█████╗██║   ██║█████╗  ██████╔╝██║█████╗  ██║██║     ███████║   ██║   ██║   ██║██████╔╝
██╔══╝╚════╝╚██╗ ██╔╝██╔══╝  ██╔══██╗██║██╔══╝  ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
███████╗     ╚████╔╝ ███████╗██║  ██║██║██║     ██║╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
╚══════╝      ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝                                                                               
""")

# Check if the file exists
if os.path.exists("api_key.txt"):
    # If the file exists, read the value and store it in a variable
    with open("api_key.txt", "r") as file:
        api = file.read().strip()
else:
    # If the file does not exist, prompt the user for the API key and store it in a file
    print("In order to utilize the tool, it is important to complete the two following steps.")
    print("- Create an account on https://mailsac.com/")
    print("- Generate a free API key")
    print("")
    api = input("Please input your API Key: ")
    with open("api_key.txt", "w") as file:
        file.write(api)

#==========================

def Account_Creation(api):
    # Set your API key and email address here
    api_key = api           # https://mailsac.com

    # Email randomization setup
    length = 20
    characters = string.ascii_lowercase + string.digits
    email = ''.join(random.choice(characters) for i in range(length)) + '@mailsac.com'

    #========================================================

    def create_email(email, api_key):
        # Make a request to get the messages for the given email address
        messages_url = f'https://mailsac.com/api/addresses/{email}'

        headers = {'Mailsac-Key': api_key}
        response = requests.get(messages_url, headers=headers).json()

        print(f"Use the following email address: {email}")

    def fetch_email(email, api_key):
        # First request (Fetching the message ID)
        message_id = f'https://mailsac.com/api/addresses/{email}/messages'
        headers = {'Mailsac-Key': api_key}
        response = []

        while not response:
            time.sleep(2)  # wait for 2 seconds before making another request
            response = requests.get(message_id, headers=headers).json()

        email_id = response[0]['_id']  # extract the _id value from the response and assign it to a variable

        # Second request (Fetching the message content)
        messages_text = f'https://mailsac.com/api/dirty/{email}/{email_id}'
        headers = {'Mailsac-Key': api_key}
        response = None

        while not response:
            time.sleep(2)  # wait for 2 seconds before making another request
            response = requests.get(messages_text, headers=headers).text

        pattern = r'\d{6}'  # match any sequence of 6 digits
        matches = re.findall(pattern, response)

        if len(matches) > 0:
            verification_code = matches[0]
            print(f'Found verification code: {verification_code}')
            return verification_code
        else:
            print('Verification code not found')
            return None

    def delete_email(email, api_key):
        # Request to delete email
        messages_url = f'https://mailsac.com/api/addresses/{email}?deleteAddressMessages=true'

        headers = {'Mailsac-Key': api_key}
        response = requests.get(messages_url, headers=headers)
        print(response.json())

    #========================================================

    create_email(email, api_key)
    fetch_email(email, api_key)

    # NOT IMPORTANT FOR NOW
    #delete_email(email, api_key)

#==========================

Account_Creation(api)