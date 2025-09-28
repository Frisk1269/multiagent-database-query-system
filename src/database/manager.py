from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    insert,
    inspect,
    text,
)
from sqlalchemy.sql import func
from datetime import datetime


class DatabaseManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.metadata_obj = MetaData()
        self.schema = self._load_schema()
        self.sample_data = self._sample_data()
        self.insert_data_into_database()
    
    def _sample_data(self):
        return {
        # Sample data (keeping your existing data)
            'business_category_samples' : [
                {"category_id": 1, "category_name": "Retail"},
                {"category_id": 2, "category_name": "Wholesale"},
                {"category_id": 3, "category_name": "Corporate"},
                {"category_id": 4, "category_name": "Government"},
                {"category_id": 5, "category_name": "Individual"},
            ],
            'customers_samples' : [
                {"customer_id": 1, "customer_name": "Alpha Mart", "category_id": 1},
                {"customer_id": 2, "customer_name": "Beta Supplies", "category_id": 2},
                {"customer_id": 3, "customer_name": "Gamma Corp", "category_id": 3},
                {"customer_id": 4, "customer_name": "City Council", "category_id": 4},
                {"customer_id": 5, "customer_name": "John Doe", "category_id": 5},
            ],
            'departments_samples' : [
                {"department_id": 1, "department_name": "Sales", "department_size": 15},
                {"department_id": 2, "department_name": "Finance", "department_size": 10},
                {"department_id": 3, "department_name": "HR", "department_size": 5},
                {"department_id": 4, "department_name": "IT", "department_size": 8},
                {"department_id": 5, "department_name": "Logistics", "department_size": 12},
            ],
            'job_desk_samples' : [
                {"job_desk_id": 1, "job_desk_name": "Sales Representative"},
                {"job_desk_id": 2, "job_desk_name": "Accountant"},
                {"job_desk_id": 3, "job_desk_name": "HR Specialist"},
                {"job_desk_id": 4, "job_desk_name": "Software Engineer"},
                {"job_desk_id": 5, "job_desk_name": "Warehouse Manager"},
            ],
            'employees_samples' : [
                {"employee_id": 1, "employee_name": "Alice Johnson", "job_desk_id": 1, "department_id": 1},
                {"employee_id": 2, "employee_name": "Bob Smith", "job_desk_id": 2, "department_id": 2},
                {"employee_id": 3, "employee_name": "Charlie Brown", "job_desk_id": 3, "department_id": 3},
                {"employee_id": 4, "employee_name": "Diana Prince", "job_desk_id": 4, "department_id": 4},
                {"employee_id": 5, "employee_name": "Ethan Hunt", "job_desk_id": 5, "department_id": 5},
            ],
            'products_samples' : [
                {"product_id": 1, "product_name": "Laptop Pro", "price": 1200.00, "stock": 25},
                {"product_id": 2, "product_name": "Office Chair", "price": 150.00, "stock": 100},
                {"product_id": 3, "product_name": "Printer X200", "price": 300.00, "stock": 40},
                {"product_id": 4, "product_name": "Desk Set", "price": 250.00, "stock": 60},
                {"product_id": 5, "product_name": "Monitor HD", "price": 200.00, "stock": 75},
            ],
            'transaction_types_samples' : [
                {"transaction_type_id": 1, "transaction_type_name": "purchase"},
                {"transaction_type_id": 2, "transaction_type_name": "refund"},
                {"transaction_type_id": 3, "transaction_type_name": "credit"},
                {"transaction_type_id": 4, "transaction_type_name": "installment"},
                {"transaction_type_id": 5, "transaction_type_name": "service"},
            ],
            'transactions_samples' : [
                {
                    "transaction_id": 1, "customer_id": 1, "employee_id": 1, "approver_id": 2,
                    "product_id": 1, "transaction_type_id": 1, "total_amount": 1200.00,
                    "remaining_amount": 0.00,
                    "created_at": datetime(2025, 8, 1, 10, 0, 0),
                    "due_at": None
                },
                {
                    "transaction_id": 2, "customer_id": 2, "employee_id": 1, "approver_id": 3,
                    "product_id": 2, "transaction_type_id": 4, "total_amount": 1500.00,
                    "remaining_amount": 500.00,
                    "created_at": datetime(2025, 8, 2, 11, 30, 0),
                    "due_at": datetime(2025, 9, 2, 11, 30, 0)  # Not overdue yet
                },
                {
                    "transaction_id": 3, "customer_id": 3, "employee_id": 2, "approver_id": 4,
                    "product_id": 3, "transaction_type_id": 1, "total_amount": 900.00,
                    "remaining_amount": 0.00,
                    "created_at": datetime(2025, 8, 3, 14, 20, 0),
                    "due_at": None
                },
                {
                    "transaction_id": 4, "customer_id": 4, "employee_id": 3, "approver_id": 5,
                    "product_id": 4, "transaction_type_id": 3, "total_amount": 250.00,
                    "remaining_amount": 0.00,
                    "created_at": datetime(2025, 8, 4, 9, 15, 0),
                    "due_at": None
                },
                {
                    "transaction_id": 5, "customer_id": 5, "employee_id": 4, "approver_id": 1,
                    "product_id": 5, "transaction_type_id": 2, "total_amount": -200.00,
                    "remaining_amount": 0.00,
                    "created_at": datetime(2025, 8, 5, 16, 45, 0),
                    "due_at": None
                },
                # Overdue installment
                {
                    "transaction_id": 6, "customer_id": 1, "employee_id": 2, "approver_id": 3,
                    "product_id": 3, "transaction_type_id": 4, "total_amount": 600.00,
                    "remaining_amount": 300.00,
                    "created_at": datetime(2025, 7, 15, 10, 0, 0),
                    "due_at": datetime(2025, 8, 15, 10, 0, 0)  # Overdue by 10 days
                },
                # Overdue installment (long overdue)
                {
                    "transaction_id": 7, "customer_id": 3, "employee_id": 1, "approver_id": 2,
                    "product_id": 1, "transaction_type_id": 4, "total_amount": 1200.00,
                    "remaining_amount": 800.00,
                    "created_at": datetime(2025, 6, 1, 14, 0, 0),
                    "due_at": datetime(2025, 7, 1, 14, 0, 0)  # Overdue by almost 2 months
                },
                # On-time installment (still active)
                {
                    "transaction_id": 8, "customer_id": 5, "employee_id": 4, "approver_id": 1,
                    "product_id": 2, "transaction_type_id": 4, "total_amount": 450.00,
                    "remaining_amount": 150.00,
                    "created_at": datetime(2025, 8, 10, 12, 0, 0),
                    "due_at": datetime(2025, 9, 10, 12, 0, 0)  # Not overdue yet
                },
            ]
        }

    def _load_schema(self):
                
        # Table definitions
        business_category = Table(
            "business_category",
            self.metadata_obj,
            Column("category_id", Integer, primary_key=True),
            Column("category_name", String(64)),
        )

        customers = Table(
            "customers",
            self.metadata_obj,
            Column("customer_id", Integer, primary_key=True),
            Column("customer_name", String(64)),
            Column("category_id", Integer),
        )

        departments = Table(
            "departments",
            self.metadata_obj,
            Column("department_id", Integer, primary_key=True),
            Column("department_name", String(64)),
            Column("department_size", Integer)
        )

        job_desk = Table(
            "job_desk",
            self.metadata_obj,
            Column("job_desk_id", Integer, primary_key=True),
            Column("job_desk_name", String(64))
        )

        employees = Table(
            "employees",
            self.metadata_obj,
            Column("employee_id", Integer, primary_key=True),
            Column("employee_name", String(64), nullable=False),
            Column("job_desk_id", Integer),
            Column("department_id", Integer)
        )

        products = Table(
            "products",
            self.metadata_obj,
            Column("product_id", Integer, primary_key=True),
            Column("product_name", String(128), nullable=False),
            Column("price", Float, nullable=False),
            Column("stock", Integer, nullable=False, default=0)
        )

        transaction_types = Table(
            "transaction_types",
            self.metadata_obj,
            Column("transaction_type_id", Integer, primary_key=True),
            Column("transaction_type_name", String(64))
        )

        transactions = Table(
            "transactions",
            self.metadata_obj,
            Column("transaction_id", Integer, primary_key=True),
            Column("customer_id", Integer, ForeignKey("customers.customer_id")),
            Column("employee_id", Integer, ForeignKey("employees.employee_id")),
            Column("approver_id", Integer, ForeignKey("employees.employee_id")),
            Column("product_id", Integer, ForeignKey("products.product_id")),
            Column("transaction_type_id", Integer, ForeignKey("transaction_types.transaction_type_id")),
            Column("total_amount", Float),
            Column("remaining_amount", Float),
            Column("created_at", DateTime(timezone=True), server_default=func.now()),
            Column("due_at", DateTime(timezone=True)),
        )

        self.metadata_obj.create_all(self.engine)
        return {
            'business_category' : business_category,
            'customers': customers,
            'departments': departments,
            'job_desk': job_desk,
            'employees': employees,
            'products': products,
            'transaction_types': transaction_types,
            'transactions': transactions
        }

    def insert_rows_into_table(self, rows, table):
        if not rows:
            return
        with self.engine.begin() as actor:
            actor.execute(insert(table), rows)
                
    def insert_data_into_database(self):
        inspector = inspect(self.engine)
        for table in self.schema.values():
            if inspector.has_table(table.name):
                with self.engine.begin() as conn:
                    conn.execute(table.delete())  # clear before insert
        # Insert all data
        sample_data = {
            self.schema['business_category']: self.sample_data['business_category_samples'],
            self.schema['customers']: self.sample_data['customers_samples'],
            self.schema['departments']: self.sample_data['departments_samples'],
            self.schema['employees']: self.sample_data['employees_samples'],
            self.schema['job_desk']: self.sample_data['job_desk_samples'],
            self.schema['products']: self.sample_data['products_samples'],
            self.schema['transaction_types']: self.sample_data['transaction_types_samples'],
            self.schema['transactions']: self.sample_data['transactions_samples'],
        }

        for table, rows in sample_data.items():
            self.insert_rows_into_table(rows, table)
            
    def display_table(self, table_name='transactions', limit=10):
        try:
            import pandas as pd
            from sqlalchemy import select

            table = self.schema[table_name]
            query = select(table).limit(limit)

            with self.engine.connect() as conn:
                result = conn.execute(query)
                rows = result.fetchall()
                if not rows:
                    print(f"The '{table_name}' table is empty.")
                else:
                    df = pd.DataFrame(rows, columns=result.keys())
                    print(df)
        except Exception as e:
            print(f"Error displaying {table_name} table: {e}")

    def run_query(self, query: str):
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            return result.fetchall()