import sqlalchemy
from sqlalchemy import text
from sqlalchemy import create_engine
import pyodbc
from dotenv import load_dotenv
import os
from typing import List, Optional
from urllib.parse import quote_plus


class DatabaseConfig:
    """Handles database configuration and environment loading"""
    def __init__(self):
        load_dotenv()
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_SERVER = os.getenv("DB_SERVER")
        self.DB_NAME = os.getenv("DB_NAME")
        self._validate_config()
        
    def _validate_config(self):
        """Validate that required configuration is present"""
        if not self.DB_SERVER or not self.DB_NAME:
            raise ValueError("DB_SERVER and DB_NAME must be set in environment variables")
    
    def get_connection_string(self, auth_type):
        driver="ODBC Driver 17 for SQL Server"
        if auth_type == 'Windows':
            conn_str =  (
                f"mssql+pyodbc://@{self.DB_SERVER}/{self.DB_NAME}"
                f"?driver={quote_plus(driver)}"
                f"&trusted_connection=yes"
                )
        elif auth_type == 'SQL':
            if not self.DB_USER or not self.DB_PASSWORD:
                raise ValueError("Missing DB_USER and DB_PASSWORD for this kind of connection.")
            conn_str = (
                 f"mssql+pyodbc://{quote_plus(self.DB_USER)}:{quote_plus(self.DB_PASSWORD)}"
                 f"@{self.DB_SERVER}/{self.DB_NAME}"
                 f"?{quote_plus(driver)}"
                )
        else:
            raise ValueError("Invalid auth_type. Use 'Windows' or 'SQL'.")
        return conn_str
    
    
class SQLConnector:
    def __init__(self, db_config: DatabaseConfig, auth_type='Windows'):
        self.LINK = db_config.get_connection_string(auth_type=auth_type)
        
        self.engine=None
        self._connect_to_db()
        self.db_info=self._get_database_info()
        self.db_schemas = self._get_table_schema()
    
    def _connect_to_db(self):
        try:
            print(self.LINK)
            self.engine = create_engine(self.LINK)
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT DB_NAME() AS dbname"))
                dbname = result.scalar()
                print("="*50)
                print(f"Connected to database: {dbname}")
                print("="*50)
        except Exception as e:
            print("="*50)
            print(f"Database connection failed:\n{e}")
            print("="*50)
            return False
        
    def fetch(self, query: str, params: Optional[dict]=None) -> List[sqlalchemy.engine.Row]:
        """
        Execute a SELECT query and return all results
        Args:
            query: SQL QUERY
            params: Optional dictionary of parameters for parameterized queries
        Returns:
            List of row objects
        """
        print("-"*50)
        print("FETCHING FROM DB")
        print("-"*50)
        if not self.engine:
            raise RuntimeError("Database engine not found.")
        
        try:
            with self.engine.connect() as conn:
                if params:
                    res = conn.execute(text(query), params)
                else:
                    res = conn.execute(text(query))
                print('Fetch successful')
                print("-"*50)
                return res.fetchall()
        except Exception as e:
            print(f"Query execution failed: {e}")
            raise

    def execute(self, query:str, params: Optional[dict]) -> sqlalchemy.engine.CursorResult:
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Optional dictionary of parameters for parameterized queries
            
        Returns:
            CursorResult object
        """
        if not self.engine:
            raise RuntimeError("Database engine not found.")
        
        try:
            with self.engine.begin() as conn:
                if params:
                    res = conn.execute(text(query), parameters=params)
                else:
                    res = conn.execute(text(query))
                return res
        
        except Exception as e:
            print(f"Query execution failed: {e}")
            raise

    def _get_database_info(self, schema: str='gold') -> str:
        """
        Retrieve and display all tables in the specified schema
        
        Args:
            schema: Database schema name (default: 'gold')
            
        Returns:
            Formatted string with database information
        """
        
        query_list_all_tables = """
            SELECT TABLE_SCHEMA,
                    TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'gold'
            ORDER BY TABLE_NAME;
        """
        try:
            result = self.fetch(query_list_all_tables, params={'schema': schema})
            info_parts = []
            print(f"\nTables in schema {schema}:")
            print("-"*50)
            for row in result:
                table_info = f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}"
                info_parts.append(table_info)
                print(f"  • {table_info}")
            
            self.db_info = '\n'.join(info_parts)
            #return self.db_info
        except Exception as e:
            print("FAILED TO: Retrieve database information.")
        
    def _get_table_schema(self, schema: str ='gold', use_cache:bool = True, table_name: str=None):
        """
        Get column information for all table
        
        Args:
            table_name: Name of the table
            schema: Schema name (default: 'gold')
        """
        tables = self.db_info.split('\n')
        for table_name in tables:
            table_key = f'{schema}.{table_name}'
            if use_cache and self.db_schemas and table_key:
                print(f"Using cached schema for {table_key}")
                res = self.db_schemas[table_key]
            else:
                query = """
                SELECT COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = :schema
                AND TABLE_NAME = :table_name
                """ 
                res = self.fetch(query, {"schema": schema, "table_name": table_name})
                # print(f"Table schema for {schema}.{table_name}")
                # caching
                self.db_schemas[table_key] = res
            
                    
                # Display formatted output
                print(f"\nSchema for {table_key}:")
                print("-" * 80)
                
                for row in res:
                    print(row)
        
    def close(self):
        if self.engine:
            self.engine.dispose()
            print("-"*50)
            print("DB Connection closed")
            print("-"*50)
            
            
if __name__ == "__main__":
    config = DatabaseConfig()
    connector = SQLConnector(config, auth_type="Windows")
    rows = connector.fetch("SELECT TOP 5 * FROM gold.fact_sales")
    for row in rows:
        print(row)
    # print(connector._get_database_info())
    # print()
    # print(type(connector._get_table_schema(table_name='dim_products')))