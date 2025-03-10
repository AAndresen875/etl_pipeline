from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.sql.schema import Table as SQLTable
from sqlalchemy import text, select
from geoalchemy2 import Geometry
import geopandas as gpd
import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Any


class DatabaseHandler:
    """
    This class provides methods to interact with a database using SQLAlchemy.
    this includes retrieving table names, column information, table data,
    and executing custom SQL queries.
    It also supports operations with GeoDataFrames for spatial data.
    Attributes:
    ----------
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine object used to connect to the database.
    connection : sqlalchemy.engine.Connection
        The active connection to the database.
    metadata : sqlalchemy.MetaData
        The metadata object that holds information about the database schema.
    Methods:
    -------
    __init__(db_url: str)
    get_table_names() -> List[str]
    get_column_info_dataframe(table_name: str) -> pd.DataFrame
    get_table(table_name: str) -> sqlalchemy.Table
    get_table_data(table_name: str) -> pd.DataFrame
        Get the data of a specific table as a pandas DataFrame.
    execute_custom_sql(statement: str) -> List[Any]
        Execute a custom SQL statement and return the results.
    execute_custom_geo_sql(statement: str) -> gpd.GeoDataFrame
        Execute a custom SQL statement and return the results as a GeoDataFrame.
    get_geo_table_data(table_name: str, geom_col: str = None, where_clause: str = None) -> gpd.GeoDataFrame
        Get the data of a specific table as a GeoDataFrame.
    close_connection() -> None

    """

    def __init__(self, db_url: str):
        """
        Initialize the DatabaseHandler with a database URL.

        :param db_url: The database URL
        """
        self.engine: Engine = create_engine(db_url)
        self.connection: Connection = self.engine.connect()
        self.metadata: MetaData = MetaData()
        self.metadata.reflect(bind=self.engine)

    # methods to get info about the schemas
    def get_table_names(self) -> List[str]:
        """
        Get the names of all tables in the database.

        :return: A list of table names
        """
        return list(self.metadata.tables.keys())

    def get_column_info_dataframe(self, table_name: str) -> pd.DataFrame:
        """
        Get the column metadata for a given table.

        :param table_name: The name of the table
        :return: A DataFrame containing the column metadata
        """
        table = self.get_table(table_name)
        columns_info = []
        for column in table.columns:
            columns_info.append(
                {
                    "name": column.name,
                    "type": str(column.type),
                    "nullable": column.nullable,
                    "default": column.default,
                    "primary_key": column.primary_key,
                    "foreign_key": column.foreign_keys,
                    "unique": column.unique,
                }
            )
        return pd.DataFrame(columns_info)

    def get_table(self, table_name: str) -> SQLTable:
        """
        Get a specific table by name.

        :param table_name: The name of the table
        :return: The SQLAlchemy Table object
        """
        return self.metadata.tables[table_name]

    # # methods to get the
    def get_table_data(self, table_name: str) -> pd.DataFrame:
        """
        Get a specific table by name. This method gets a SQLAlchemy Table object
        and uses the metadata in it to create a pandas DataFrame.

        :param table_name: The name of the table
        :return: The SQLAlchemy Table object
        """
        # refreshing the connection
        self.connection = self.engine.connect()
        sql_table = Table(table_name, self.metadata)  # , autoload_with=self.engine)
        # Create a select statement to query the table
        stmt = select(sql_table)
        # Execute the query and fetch the results
        with self.connection as connection:
            result = connection.execute(stmt)
            rows = result.fetchall()
        return pd.DataFrame(rows, columns=sql_table.columns.keys())

    def execute_custom_sql(self, statement: str) -> List[Any]:
        """
        Execute an SQL statement and return the results.

        :param statement: The SQL statement to execute
        :return: The results of the query
        """
        try:
            # using We use self.engine.begin() to create a transaction context.
            # This ensures that the transaction is automatically committed if no
            # exceptions occur, or rolled back if an exception is raised.
            with self.engine.begin() as connection:
                result = connection.execute(text(statement))
                # If the statement is a SELECT, fetch and return the results
                if statement.strip().lower().startswith("select"):
                    return result.fetchall()
                # For other statements (UPDATE, INSERT, DELETE), return an empty list
                return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_geo_table_data(
        self, table_name: str, geom_col: str = None, where_clause: str = None
    ) -> gpd.GeoDataFrame:
        """
        Get a specific table by name and return a geopandas dataframe.

        :param table_name: The name of the table
        :param geom_col: The geometry column to use
        :param where_clause: The SQL WHERE clause to filter the data
        :return: The GeoDataFrame
        """
        # refreshing the connection
        self.connection = self.engine.connect()
        # Get the table
        table = self.get_table(table_name)
        # Find all geometry columns
        geom_cols = [
            column.name for column in table.columns if isinstance(column.type, Geometry)
        ]
        # checking to see if there are no geometry columns:
        if not geom_cols:
            raise ValueError(f"No geometry columns found in table '{table_name}'")
        # getting the local variable geom_col confirmed it's an option and can select
        if geom_col is None:
            # Use the first geometry column if none is specified
            geom_col = geom_cols[0]
        elif geom_col not in geom_cols:
            raise ValueError(
                f"Specified geometry column '{geom_col}' not found in table '{table_name}'. Available geometry columns: {geom_cols}"
            )
        # Construct the SQL query
        query = f"SELECT * FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"

        # return the geopandas dataframe
        return gpd.read_postgis(query, con=self.connection, geom_col=geom_col)

    def close_connection(self) -> None:
        """
        Close the database connection.
        """
        self.connection.close()
