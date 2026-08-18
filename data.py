import geopandas as gpd
from shapely.geometry import Polygon


def create_zones():
    """
    Create the initial territorial rice production zones.
    """

    zones = gpd.GeoDataFrame({
        "zone": [
            "Zone A",
            "Zone B",
            "Zone C",
            "Zone D"
        ],

        "surface_ha": [
            2000,
            4500,
            1800,
            3200
        ],

        "rice_type": [
            "Irrigated rice",
            "Rainfed rice",
            "Fragrant rice",
            "Irrigated rice"
        ],

        "yield_base_t_ha": [
            4.5,
            2.8,
            2.5,
            4.0
        ],

        "irrigation": [
            100,
            0,
            40,
            100
        ],

    })

    # --------------------------------------------------
    # TERRITORIAL GEOMETRY
    # --------------------------------------------------

    zones["geometry"] = [

    # Zone A - nord
    Polygon([
        (104.70, 11.65),
        (104.90, 11.75),
        (105.10, 11.65),
        (105.00, 11.50),
        (104.80, 11.50)
    ]),

    # Zone B - sud-ouest
    Polygon([
        (104.45, 11.25),
        (104.65, 11.40),
        (104.75, 11.25),
        (104.65, 11.05),
        (104.45, 11.10)
    ]),

    # Zone C - sud-est
    Polygon([
        (105.05, 11.35),
        (105.25, 11.45),
        (105.40, 11.30),
        (105.30, 11.10),
        (105.10, 11.15)
    ]),

    # Zone D - sud
    Polygon([
        (104.75, 10.90),
        (104.95, 11.05),
        (105.15, 10.95),
        (105.05, 10.75),
        (104.85, 10.75)
    ])
]

    zones = gpd.GeoDataFrame(
    zones,
    geometry="geometry",
    crs="EPSG:4326"
)
    
    return zones