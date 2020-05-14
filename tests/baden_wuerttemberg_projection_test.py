from missing_addresses import BadenWuerttembergProjection


def test_projection():
    latlon = BadenWuerttembergProjection().projected_to_latlon(500997.85, 5405034.37)  # Leonberg city hall in Baden-Württemberg coordinates
    assert round(abs(latlon[0]-48.7983), 4) == 0
    assert round(abs(latlon[1]-9.0136), 4) == 0
