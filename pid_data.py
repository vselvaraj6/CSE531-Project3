from dataclasses import dataclass

@dataclass(repr=True, order=True)
class PIdData:
    id: int
    name: str
    clock: int
    

    def __repr__(self):
        return "{'id': " + str(self.id) + ", 'name': "+ self.name + ", 'clock': " + str(self.clock) + '}'