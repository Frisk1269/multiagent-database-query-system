
# Schema validation function
def validate_sql_query(query: str) -> tuple[bool, str]:
    """
    Validates SQL query against known schema to prevent hallucinations.
    Returns (is_valid, error_message)
    """
    # Valid table names (exact match required)
    valid_tables = {
        'transactions', 'transaction_types', 'products', 'customers',
        'employees', 'departments', 'business_category', 'job_desk'
    }

    # Valid column names by table
    valid_columns = {
        'transactions': {'transaction_id', 'customer_id', 'employee_id', 'approver_id',
                        'product_id', 'transaction_type_id', 'total_amount', 'remaining_amount',
                        'created_at', 'due_at'},
        'transaction_types': {'transaction_type_id', 'transaction_type_name'},
        'products': {'product_id', 'product_name', 'price', 'stock'},
        'customers': {'customer_id', 'customer_name', 'category_id'},
        'employees': {'employee_id', 'employee_name', 'job_desk_id', 'department_id'},
        'departments': {'department_id', 'department_name', 'department_size'},
        'business_category': {'category_id', 'category_name'},
        'job_desk': {'job_desk_id', 'job_desk_name'}
    }

    query_lower = query.lower()

    # Check for invalid table references
    import re

    # Find table references after FROM and JOIN
    table_patterns = [
        r'from\s+(\w+)',
        r'join\s+(\w+)',
        r'left\s+join\s+(\w+)',
        r'right\s+join\s+(\w+)',
        r'inner\s+join\s+(\w+)',
        r'outer\s+join\s+(\w+)'

    ]

    referenced_tables = set()
    for pattern in table_patterns:
        matches = re.findall(pattern, query_lower)
        referenced_tables.update(matches)

    # Check for invalid tables
    invalid_tables = referenced_tables - valid_tables
    if invalid_tables:
        return False, f"Invalid table(s) found: {invalid_tables}. Valid tables: {valid_tables}"

    # Check for common hallucinated table names
    hallucinated_tables = {
        'payments', 'installments', 'salesreps', 'sales_reps', 'orders',
        'invoices', 'customers_payments', 'payment_status'
    }

    found_hallucinated = referenced_tables & hallucinated_tables
    if found_hallucinated:
        return False, f"Hallucinated table(s) detected: {found_hallucinated}. Use only: {valid_tables}"

    # Check for common hallucinated column patterns
    hallucinated_patterns = [
        r'customerid', r'customername', r'salesrepid', r'salesrepname',
        r'amountowed', r'paymentstatus', r'duedate', r'amountpaid',
        r'amountdue', r'installmentid'
    ]

    for pattern in hallucinated_patterns:
        if re.search(pattern, query_lower):
            return False, f"Possible hallucinated column detected. Check column names against schema."

    return True, "Query appears valid"
