from enum import Enum
from typing import List, Literal
from uuid import uuid4

class Task(Enum):
    DETECTION = 'detection'
    CLASSIFICATION = 'classification'

def _str2color(name: str) -> str:
    hash = 0
    for char in name: hash = ord(char) + ((hash << 5) - hash)
    color = '#'
    for i in range(3):
        value = (hash >> (i * 8)) & 0xFF
        color += '%.02x' % value
    return color

def generate_label_config(task: Literal, classes: List[str]) -> str:
    view = '<View>'
    context = ''

    # detection
    if task == Task.DETECTION:
        '''
        <View>
            <Image name="image" value="$image"/>
            <RectangleLabels name="label" toName="image">
                <Label value="Airplane" background="green"/>
                <Label value="Car" background="blue"/>
            </RectangleLabels>
        </View>
        '''
        labels = []
        for name in classes:
            labels.append(f'<Label value="{name}" background="{_str2color(name=name)}"/>')
        
        rectanglelabels = f'<RectangleLabels name="label" toName="image">'
        for label in labels:
            choices += label
        rectanglelabels += '</RectangleLabels>'

        context = f'<Image name="image" value="$image"/>{rectanglelabels}'
    # classification
    elif task == Task.CLASSIFICATION:
        '''
        <View>
            <Image name="image" value="$image"/>
            <Choices name="choice" toName="image">
                <Choice value="Adult content"/>
                <Choice value="Weapons" />
                <Choice value="Violence" />
            </Choices>
        </View>
        '''
        labels = []
        for name in classes:
            labels.append(f'<Choice value="{name}"/>')
        
        choices = f'<Choices name="choice" toName="image">'
        for label in labels:
            choices += label
        choices += '</Choices>'

        context = f'<Image name="image" value="$image"/>{choices}'
    else:
        raise NotImplementedError(f"[{task}] is not supported task.")

    view += context
    view += '</View>'

    return view

def generate_annotations(task: Literal, image: dict, infos: List[dict]) -> List[dict]:
    annotations = []
    
    if task == Task.DETECTION:
        '''
        "annotations": [
            {
                "id": "1001",
                "result": [
                    {
                        "from_name": "tag",
                        "id": "Dx_aB91ISN",
                        "source": "$image",
                        "to_name": "img",
                        "type": "rectanglelabels",
                        "value": {
                            "height": 10.458911419423693,
                            "rectanglelabels": [
                                "Moonwalker"
                            ],
                            "rotation": 0,
                            "width": 12.4,
                            "x": 50.8,
                            "y": 5.869797225186766
                        }
                    }
                ],
                "was_cancelled":false,
                "ground_truth":false,
                "created_at":"2021-03-09T22:16:08.728353Z",
                "updated_at":"2021-03-09T22:16:08.728378Z",
                "lead_time":4.288,
                "result_count":0,
                "task":1,
                "completed_by":10
            }
        ]
        '''
        result = []
        for info in infos:
            annotation = {
                "id": info["id"],
                "type":"rectanglelabels",
                "to_name": "image",
                "from_name": "label",
                "original_width": image["width"],
                "original_height": image["height"],
                "image_rotation": image["rotation"],
                "value": {
                    "x": info["x"],
                    "y": info["y"],
                    "width": info["width"],
                    "height": info["height"],
                    "rotation": info["rotation"],
                    "rectanglelabels": info["classes"] # List
                }
            }
            result.append(annotation)
        annotations.append({"result": result})
    elif task == Task.CLASSIFICATION:
        '''
        "annotations": [
            {
                "id": "1001",
                "result": [
                    {
                        "id": "result3",
                        "type": "choices",
                        "from_name": "choice",
                        "to_name": "image",
                        "value": {
                        "choices": ["Airbus"]
                    }
                ],
                "was_cancelled":false,
                "ground_truth":false,
                "created_at":"2021-03-09T22:16:08.728353Z",
                "updated_at":"2021-03-09T22:16:08.728378Z",
                "lead_time":4.288,
                "result_count":0,
                "task":1,
                "completed_by":10
            }
        ]
        '''
        result = []
        for info in infos:
            annotation = {
                "id": info["id"],
                "type": "choices",
                "from_name": "choice",
                "to_name": "image",
                "value": {
                    "choices": info["classes"]
                }
            }
            result.append(annotation)
        annotations.append({"result": result})
    else:
        raise NotImplementedError(f"[{task}] is not supported task.")

    return annotations