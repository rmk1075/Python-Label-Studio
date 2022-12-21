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