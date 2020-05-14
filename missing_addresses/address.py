from missing_addresses import Housenumber


class Address:
    """
    An address, i.e. what this tool is all about.
    Two addresses are equals iff the street and the housenumber are equal.
    """
    street: str
    housenumber: Housenumber

    def __init__(self, street: str, housenumber):
        """
        :param street: street name of the address
        :param housenumber: housenumber of the address, if a string is here, it will be parsed into a Housenumber
        """
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
        """Two addresses are equals iff the street and the housenumber are equal."""
        if isinstance(other, Address):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        return f'{self.street} {self.housenumber}'
