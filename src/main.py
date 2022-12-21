from dotenv import load_dotenv
from label_studio_sdk import Client
from label_studio_sdk.project import Project
import os
from typing import List
from uuid import uuid4

from label_studio.label_studio import Task, generate_label_config

# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = ''
API_KEY = ''

IMAGE_FILE = './resource/images/test.jpg'
ENV_FILE = './resource/.env'

def initialize() -> None:
    load_dotenv(dotenv_path=ENV_FILE)

    global LABEL_STUDIO_URL
    LABEL_STUDIO_URL = os.environ.get('LABEL_STUDIO_URL')

    global API_KEY
    API_KEY = os.environ.get('API_KEY')

'''
- create project
- delete project
- push image & labels
- pull labels (label studio image - autocare_tx imagedata mapping logic)
'''
if __name__ == "__main__":
    initialize()

    # Connect to the Label Studio API and check the connection
    client = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    print(client.check_connection())

    # get projects
    projects: List[Project] = client.get_projects()
    print(projects)

    # find project
    title: str = "LS Test Project"
    project: Project = None
    for proj in projects:
        if proj.get_params()['title'] == title:
            project = proj
            break

    config = {
        'task': Task.DETECTION,
        'classes': ['person', 'flame']
    }

    if project is None:
        # create project
        description: str = "test project for label-studio adaptor task"
        label_config: str = generate_label_config(
            task=config['task'],
            classes=config['classes']
        )
        project = client.start_project(
            title=title,
            description=description,
            label_config=label_config
        )

    print(f"project={project}")



