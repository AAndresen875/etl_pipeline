from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.sql.schema import Table as SQLTable
import os
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

    def get_table_names(self) -> List[str]:
        """
        Get the names of all tables in the database.

        :return: A list of table names
        """
        return list(self.metadata.tables.keys())

    def get_table(self, table_name: str) -> SQLTable:
        """
        Get a specific table by name.

        :param table_name: The name of the table
        :return: The SQLAlchemy Table object
        """
        return Table(table_name, self.metadata, autoload_with=self.engine)

    def execute_sql(self, statement: str) -> List[Any]:
        """
        Execute an SQL statement and return the results.

        :param statement: The SQL statement to execute
        :return: The results of the query
        """
        try:
            result = self.connection.execute(statement)
            return result.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def close_connection(self) -> None:
        """
        Close the database connection.
        """
        self.connection.close()
