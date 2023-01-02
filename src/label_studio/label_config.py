from enum import Enum
from typing import List, Literal, TypeVar

from src.common.utils import str2color

class Task(Enum):
    DETECTION = 'detection'
    CLASSIFICATION = 'classification'

LabelConfigBuilderType = TypeVar(name='LabelConfigBuilderType')

class LabelConfigBuilder:
    def __init__(self, task: Task) -> None:
        if type(task) is not Task:
            raise ValueError()
        
        self._task = task
        self._labels: List[self.Label] = []
    
    @classmethod
    def task(cls, task: Task) -> LabelConfigBuilderType:
        builder = cls(task=task)
        return builder
    
    def add_label(self, label: str) -> LabelConfigBuilderType:
        if self._task == Task.DETECTION:
            self._labels.append(self.L(value=label, background=str2color(name=label)))
        elif self._task == Task.CLASSIFICATION:
            self._labels.append(self.C(value=label))
        return self
    
    def build(self) -> str:
        result = ''
        if self._task == Task.DETECTION:
            for label in self._labels:
                result += f'<Label value="{label.value}" background="{label.background}"/>'
            result = '<RectangleLabels name="label" toName="image">' + result + '</RectangleLabels>'
        elif self._task == Task.CLASSIFICATION:
            for label in self._labels:
                result += f'<Choice value="{label.value}"/>'
            result = '<Choices name="label" toName="image">' + result + '</Choices>'
        else:
            if self._task == None:
                raise SyntaxError("task is not defined.")
            raise ValueError(f"task {self._task} is not supported.")
        return '<View><Image name="image" value="$image"/>' + result + '</View>'
    
    class Label:
        pass
    
    class L(Label):
        def __init__(self, value: str, background: str) -> None:
            self.value = value
            self.background = background
            
    class C(Label):
        def __init__(self, value: str) -> None:
            self.value = value
                
                
if __name__ == "__main__":
    task = Task.DETECTION
    classes = ['a', 'b', 'c', 'd']
    
    config = LabelConfigBuilder.task(task=task)
    for clazz in classes:
        config = config.add_label(label=clazz)
    result = config.build()
    print(result)