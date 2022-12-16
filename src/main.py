# Import the SDK and the client module
from label_studio_sdk import Client
from typing import List

# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = ''
API_KEY = ''

IMAGE_FILE = './resource/images/test.jpg'


'''
- create project
- delete project
- push image & labels
- pull labels (label studio image - autocare_tx imagedata mapping logic)
'''
if __name__ == "__main__":
    # Connect to the Label Studio API and check the connection
    client = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    print(client.check_connection())
