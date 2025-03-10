import geopandas as gpd
from shapely.geometry import Polygon


class GeoDataFrameHandler:
    """
    A handler class for operations on a GeoDataFrame.
    Attributes:
    -----------
    gdf : gpd.GeoDataFrame
        The GeoDataFrame containing geographical data.
    Methods:
    --------
    get_min_max_coordinates(boundary_id):
        Retrieves the minimum and maximum coordinates of the polygon associated with the given boundary ID.
    """

    def __init__(self):
        """
        Initializes the GeoDataFrameHandler with an empty GeoDataFrame.
        """
        self.gdf = gpd.GeoDataFrame()

    def get_min_max_coordinates(
        self, gdf: gpd.GeoDataFrame, field_name: str, field_id: int
    ) -> dict:
        """
        Retrieves the minimum and maximum coordinates of the polygon associated with the given field name and field ID.

        Parameters:
        -----------
        field_name : str
            The name of the field to search within the GeoDataFrame.
        field_id : int
            The ID of the field to retrieve the polygon coordinates for.

        Returns:
        --------
        dict
            A dictionary containing the minimum and maximum coordinates of the polygon.

        Raises:
        -------
        ValueError
            If no boundary is found with the given field ID or if the polygon is empty.
        """
        # if the geo dataframe isn't passed in
        if gdf is None:
            gdf = self.gdf
        # get the row with the specified field_id
        row = gdf[gdf[field_name] == field_id]
        if row.empty:
            raise ValueError(f"No boundary found with {field_name} = {field_id}")

        polygon = row.iloc[0]["shape"]
        if polygon.is_empty:
            raise ValueError(f"Polygon is empty for {field_name} = {field_id}")

        minx, miny, maxx, maxy = polygon.bounds
        return {"min_coordinates": (minx, miny), "max_coordinates": (maxx, maxy)}

    def aggregate_coordinates(
        self, coord1: dict, coord2: dict, buffer: float = 0.0
    ) -> dict:
        """
        Aggregates two coordinate dictionaries and applies an optional buffer.

        Parameters:
        -----------
        coord1 : dict
            The first coordinate dictionary containing min and max coordinates.
        coord2 : dict
            The second coordinate dictionary containing min and max coordinates.
        buffer : float, optional
            An optional buffer to apply to the aggregated coordinates (default is 0.0).

        Returns:
        --------
        dict
            A dictionary containing the aggregated minimum and maximum coordinates with the buffer applied.
        """
        minx = min(coord1["min_coordinates"][0], coord2["min_coordinates"][0]) - buffer
        miny = min(coord1["min_coordinates"][1], coord2["min_coordinates"][1]) - buffer
        maxx = max(coord1["max_coordinates"][0], coord2["max_coordinates"][0]) + buffer
        maxy = max(coord1["max_coordinates"][1], coord2["max_coordinates"][1]) + buffer

        return {"min_coordinates": (minx, miny), "max_coordinates": (maxx, maxy)}

    def create_rectangle_polygon(self, coordinates: dict) -> Polygon:
        """
        Creates a rectangular polygon from the given coordinates.

        Parameters:
        -----------
        coordinates : dict
            A dictionary containing the minimum and maximum coordinates of the rectangle.

        Returns:
        --------
        Polygon
            the rectangular polygon.
        """
        minx, miny = coordinates["min_coordinates"]
        maxx, maxy = coordinates["max_coordinates"]

        # Create a Shapely Polygon object
        rectangle = Polygon(
            [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)]
        )

        return rectangle
