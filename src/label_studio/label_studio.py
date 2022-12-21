from enum import Enum
from typing import List, Literal

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
        
        choices = f'<RectangleLabels name="label" toName="image">'
        for label in labels:
            choices += label
        choices += '</RectangleLabels>'

        context = f'<Image name="image" value="$image"/>{choices}'
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
        
        choices = f'<Choices name="label" toName="image">'
        for label in labels:
            choices += label
        choices += '</Choices>'

        context = f'<Image name="image" value="$image"/>{choices}'
    else:
        raise NotImplementedError(f"[{task}] is not supported task.")

    view += context
    view += '</View>'

    return view

def generate_annotations() -> List[dict]:
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
    annotations = [
        {
            "result": [
                {
                    "to_name": "image",
                    "from_name": "label",
                    "original_width": 1920,
                    "original_height": 1080,
                    "image_rotation": 0,
                    "value": {
                        "x": 18.548387096774192,
                        "y": 20.43010752688172,
                        "width": 20.967741935483872,
                        "height": 34.40860215053764,
                        "rotation": 0,
                        "rectanglelabels": [
                            "Airplane"
                        ]
                    }
                }
            ]
        }
    ]

    return annotations