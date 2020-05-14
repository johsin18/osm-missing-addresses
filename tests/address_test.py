from missing_addresses import Address, Housenumber


def test_constructor():
    a = Address('street', '3')
    assert a.street == 'street'
    assert a.housenumber == Housenumber('3')

    housenumber = Housenumber('42')
    a = Address('street', housenumber)
    assert a.street == 'street'
    assert a.housenumber == housenumber


def test_eq():
    assert Address('street', '3') != Housenumber('42')


def test_str():
    a = Address('street', '42')
    assert str(a) == 'street 42'
