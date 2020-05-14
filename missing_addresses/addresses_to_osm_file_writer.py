from xml.dom.minidom import getDOMImplementation, DOMImplementation, Document, Node, Element
from missing_addresses import *
from typing import Dict


class AddressesToOsmFileWriter:
    def write_missing(self, addresses: Dict[Address, MissingAddressInformation], filepath: str):
        """
        Write missing addresses to an OSM file.
        :param addresses: Addresses to write, as dictionary mapping from Address to MissingAddressInformation.
        :param filepath: Filepath for the file to be written.
        """
        dom: DOMImplementation = getDOMImplementation()
        osm_file: Document = dom.createDocument(None, "osm", None)
        root_node: Node = osm_file.childNodes[0]
        root_node.setAttribute("version", "0.6")

        identifier: int = -1  # negative identifiers for new primitives, decrementing from -1
        for a, i in addresses.items():
            n: Element = osm_file.createElement("node")
            n.setAttribute("id", str(identifier))
            identifier -= 1
            c: Coordinate = i if (isinstance(i, Coordinate)) else i.coordinate
            n.setAttribute("lat", str(c.lat))
            n.setAttribute("lon", str(c.lon))
            street_tag: Element = osm_file.createElement("tag")
            street_tag.setAttribute("k", "addr:street")
            street_tag.setAttribute("v", a.street)
            housenumber_tag: Element = osm_file.createElement("tag")
            housenumber_tag.setAttribute("k", "addr:housenumber")
            housenumber_tag.setAttribute("v", str(a.housenumber))
            n.appendChild(street_tag)
            n.appendChild(housenumber_tag)
            root_node.appendChild(n)

        output_file = open(filepath, "w", encoding="utf-8")  # encoding is important to preserve umlauts
        osm_file.writexml(output_file, "  ", "  ", "\n", "UTF-8")
        output_file.close()
