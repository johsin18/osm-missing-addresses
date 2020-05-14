from missing_addresses import OsmPrimitive, Housenumber


def test_eq():
    assert OsmPrimitive('node', 3) == OsmPrimitive('node', 3)
    assert OsmPrimitive('node', 3) != OsmPrimitive('way', 3)
    assert OsmPrimitive('node', 3) != OsmPrimitive('node', 4)
    assert OsmPrimitive('node', 3) != Housenumber('42')
