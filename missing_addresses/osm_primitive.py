class OsmPrimitive:
    type: str
    id: int

    def __init__(self, type: str, id: int):
        assert(type == "node" or type == "way" or type == "relation")
        self.type = type
        self.id = id

    def __key(self):
        return self.type, self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, OsmPrimitive):
            return self.__key() == other.__key()
        return NotImplemented
