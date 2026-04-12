from abc import ABC, abstractmethod

class BaseAction(ABC):
    name: str # stores the action name (shown in gui)
    description: str # stores the action description (shown in gui)
    id: str # stores the actual id of the action which the program calls during execution

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError