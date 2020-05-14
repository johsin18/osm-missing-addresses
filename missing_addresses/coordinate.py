from dataclasses import dataclass


@dataclass()
class Coordinate:
    """Coordinate of an address, comprised of latitude and longitude"""
    lat: float
    lon: float
