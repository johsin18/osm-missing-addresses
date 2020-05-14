from dataclasses import dataclass
from missing_addresses import *


@dataclass
class MatchInformation:
    osm_primitive: OsmPrimitive
    coordinate: Coordinate
