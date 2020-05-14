from dataclasses import dataclass
from missing_addresses import OsmPrimitive, Coordinate


@dataclass
class MatchInformation:
    osm_primitive: OsmPrimitive
    coordinate: Coordinate
