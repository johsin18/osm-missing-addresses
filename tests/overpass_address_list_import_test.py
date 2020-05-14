import pytest

from missing_addresses import OverpassAddressListImport, Address, OsmPrimitive, Housenumber


@pytest.mark.skipif(True, reason="cannot query Overpass all the time")
def test_import():
    addresses = OverpassAddressListImport().read(349628081)  # industrial area in Leonberg, with relatively few addresses
    assert isinstance(addresses, list)
    assert len(addresses) >= 8
    assert (Address('Am Längenbühl', '12'), OsmPrimitive('way', 684944733)) in addresses
    for (a, p) in addresses:
        assert a.street != ""
        assert isinstance(a.housenumber, Housenumber)
        assert p.type in ['node', 'way', 'relation']
        assert isinstance(p.id, int)
