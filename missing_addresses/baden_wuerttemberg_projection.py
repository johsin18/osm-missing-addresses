from pyproj import CRS, Transformer


class BadenWuerttembergProjection:
    """
    Projection from the Baden-Württemberg (German state) authority-official coordinate system, to polar coordinates.
    """
    projection_for_Baden_Wuerttemberg: CRS
    transformer: Transformer

    def __init__(self):
        self.projection_for_Baden_Wuerttemberg = CRS.from_wkt( # projection as used by Landesamt für Geoinformation und Landentwicklung in Baden-Württemberg
            """PROJCS["ETRS89 / UTM zone 32N",GEOGCS["ETRS89",DATUM["European Terrestrial Reference System 1989",SPHEROID["GRS 1980",6378137.0,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0.0,0.0,0.0,0.0,0.0,0.0,0.0],AUTHORITY["EPSG","6258"]],PRIMEM["Greenwich",0.0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.017453292519943295],AXIS["Geodetic longitude",EAST],AXIS["Geodetic latitude",NORTH],AUTHORITY["EPSG","4258"]],PROJECTION["Transverse Mercator",AUTHORITY["EPSG","9807"]],PARAMETER["central_meridian",9.0],PARAMETER["latitude_of_origin",0.0],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000.0],PARAMETER["false_northing",0.0],UNIT["m",1.0],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","25832"]]"""
        )
        self.transformer = Transformer.from_crs(self.projection_for_Baden_Wuerttemberg, "EPSG:4326")

    def projected_to_latlon(self, easting, northing):
        return self.transformer.transform(easting, northing)
