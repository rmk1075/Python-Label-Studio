from dotenv import load_dotenv
from label_studio_sdk import Client
import os
from typing import List

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

def generate_label_config(task: str, classes: List[str]) -> str:
    # detection
    if task == 'detection':
        pass
    
    # classification
    elif task == 'classification':
        pass

    pass


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
    projects = client.get_projects()
    print(projects)

    # create project
    title: str = "Test Project"
    description: str = "test project for label-studio adaptor task"
    # label_config: str = generate_label_config() # TODO:
    project = client.start_project(
        title=title,
        description=description
    )
    print(f"new project={project}")

    tasks = project.get_tasks()
    print(f"tasks=[size={len(tasks)} tasks={tasks}]")

    tasks = project.get_labeled_tasks()
    print(f"tasks=[size={len(tasks)} tasks={tasks}]")

    # image = open(IMAGE_FILE, 'rb')
    # print(image.name)

    # tasks = {}
    # project.import_tasks(
    #     tasks=tasks,
    #     preannotated_from_fields=None
    # )

    # response = client.delete_project(project_id=project.id)
    # print(response)
