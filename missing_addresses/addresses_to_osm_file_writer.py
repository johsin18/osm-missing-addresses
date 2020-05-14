from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation
from missing_addresses import Address, MissingAddressInformation, Coordinate
from typing import Dict


class AddressesToOsmFileWriter:
    def __init__(self):
        return

    def write(self, addresses: Dict[Address, MissingAddressInformation], filepath: str):
        impl = getDOMImplementation()
        osm_file = impl.createDocument(None, "osm", None)
        root_node = osm_file.childNodes[0]
        root_node.setAttribute("version", "0.6")

        identifier: int = -1  # negative identifiers for new primitives, decrementing from -1
        for a, i in addresses.items():
            n: minidom.Element
            n = osm_file.createElement("node")
            n.setAttribute("id", str(identifier))
            identifier -= 1
            c: Coordinate = i if (isinstance(i, Coordinate)) else i.coordinate
            n.setAttribute("lat", str(c.lat))
            n.setAttribute("lon", str(c.lon))
            street_tag = osm_file.createElement("tag")
            street_tag.setAttribute("k", "addr:street")
            street_tag.setAttribute("v", a.street)
            housenumber_tag = osm_file.createElement("tag")
            housenumber_tag.setAttribute("k", "addr:housenumber")
            housenumber_tag.setAttribute("v", str(a.housenumber))
            n.appendChild(street_tag)
            n.appendChild(housenumber_tag)
            root_node.appendChild(n)

        output_file = open(filepath, "w", encoding="utf-8")  # encoding is important to preserve umlauts
        osm_file.writexml(output_file, "  ", "  ", "\n", "UTF-8")
        output_file.close()
