from missing_addresses import Housenumber


class Address:
    street: str
    housenumber: Housenumber

    def __init__(self, street: str, housenumber):
        assert isinstance(street, str)
        self.street = street
        if isinstance(housenumber, Housenumber):
            self.housenumber = housenumber
        else:
            self.housenumber = Housenumber(housenumber)

    def __key(self):
        return self.street, self.housenumber.equality_key()

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Address):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        return f'{self.street} {self.housenumber}'
