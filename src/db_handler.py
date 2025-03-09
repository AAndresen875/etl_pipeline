from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.sql.schema import Table as SQLTable
from sqlalchemy import text, select
import geopandas as gpd
import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Any


class DatabaseHandler:
    """
    A class to handle database operations using SQLAlchemy.
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

    def execute_sql(self, statement: str) -> List[Any]:
        """
        Execute an SQL statement and return the results.

        :param statement: The SQL statement to execute
        :return: The results of the query
        """
        try:
            result = self.connection.execute(text(statement))
            return result.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def execute_geo_sql(self, statement: str) -> gpd.GeoDataFrame:
        """
        Execute an SQL statement and return the results as a GeoDataFrame.

        :param statement: The SQL statement to execute
        :return: The results of the query
        """
        # read the query results into a GeoDataFrame
        gdf = gpd.read_postgis(statement, con=self.engine)
        # return the GeoDataFrame
        return gdf

    def close_connection(self) -> None:
        """
        Close the database connection.
        """
        self.connection.close()
