from dotenv import load_dotenv
from label_studio_sdk import Client
from label_studio_sdk.project import Project
import os
from typing import List
from uuid import uuid4

from label_studio.label_studio import Task, generate_label_config, generate_annotations

# Define the URL where Label Studio is accessible and the API key for your user account
LABEL_STUDIO_URL = ''
API_KEY = ''

ENV_FILE = './resource/.env'
IMAGE_URI = ''

def initialize() -> None:
    load_dotenv(dotenv_path=ENV_FILE)

    global LABEL_STUDIO_URL
    LABEL_STUDIO_URL = os.environ.get('LABEL_STUDIO_URL')

    global API_KEY
    API_KEY = os.environ.get('API_KEY')

    global IMAGE_URI
    IMAGE_URI = os.environ.get('IMAGE_URI')

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

    # import task
    # generate tasks
    image_info = {
        "width": 1920,
        "height": 1080,
        "rotation": 0
    }
    
    infos = [
        {
            "id": str(uuid4()),
            "x": 18.548387096774192,
            "y": 20.43010752688172,
            "width": 20.967741935483872,
            "height": 34.40860215053764,
            "rotation": 0,
            "classes": ["person"]
        }
    ]
    
    annotations = generate_annotations(
        task=Task.DETECTION,
        image=image_info,
        infos=infos
    )

    # generate task
    task_id = str(uuid4())
    image = IMAGE_URI
    tasks = {
        'data': {
            'image': image,
        },
        'annotations': annotations,
        'meta': {
            'id': task_id
        }
    }
    
    # import task
    task_id = project.import_tasks(tasks=tasks)
    
    task = project.get_task(task_id=task_id[0])
    print(f"task=[{task}]")
