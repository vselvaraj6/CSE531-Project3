from dataclasses import dataclass

@dataclass(repr=True, order=True)
class EventIdData:
    clock: int
    name: str
    

    def __repr__(self):
        return "{'clock': " + str(self.clock) + ", 'name': "+ self.name + '}'