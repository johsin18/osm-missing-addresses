from dataclasses import dataclass
from missing_addresses import Coordinate, IgnoredAddressInformation


@dataclass()
class MissingAddressInformation:
    coordinate: Coordinate
    ignore_information: IgnoredAddressInformation
