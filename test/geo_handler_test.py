import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from ..src.geo_dataframe_handler import GeoDataFrameHandler


@pytest.fixture
def handler():
    return GeoDataFrameHandler()


@pytest.fixture
def sample_gdf():
    data = {
        "field_name": [1, 2],
        "shape": [
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
            Polygon([(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)]),
        ],
    }
    return gpd.GeoDataFrame(data)


def test_get_min_max_coordinates(handler, sample_gdf):
    result = handler.get_min_max_coordinates(sample_gdf, "field_name", 1)
    assert result == {"min_coordinates": (0.0, 0.0), "max_coordinates": (1.0, 1.0)}

    result = handler.get_min_max_coordinates(sample_gdf, "field_name", 2)
    assert result == {"min_coordinates": (2.0, 2.0), "max_coordinates": (3.0, 3.0)}

    with pytest.raises(ValueError):
        handler.get_min_max_coordinates(sample_gdf, "field_name", 3)


def test_aggregate_coordinates(handler):
    coord1 = {"min_coordinates": (0.0, 0.0), "max_coordinates": (1.0, 1.0)}
    coord2 = {"min_coordinates": (2.0, 2.0), "max_coordinates": (3.0, 3.0)}
    result = handler.aggregate_coordinates(coord1, coord2)
    assert result == {"min_coordinates": (0.0, 0.0), "max_coordinates": (3.0, 3.0)}

    result = handler.aggregate_coordinates(coord1, coord2, buffer=0.5)
    assert result == {"min_coordinates": (-0.5, -0.5), "max_coordinates": (3.5, 3.5)}


def test_create_rectangle_polygon(handler):
    coordinates = {"min_coordinates": (0.0, 0.0), "max_coordinates": (1.0, 1.0)}
    rectangle = handler.create_rectangle_polygon(coordinates)
    assert rectangle.equals(
        Polygon([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)])
    )
