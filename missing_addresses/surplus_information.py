from dataclasses import dataclass

from missing_addresses import *


@dataclass
class SurplusInformation:
    osm_primitive: OsmPrimitive
    ignore_information: IgnoredAddressInformation
