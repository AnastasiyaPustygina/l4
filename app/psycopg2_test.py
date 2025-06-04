import psycopg2

try:
    conn = psycopg2.connect("dbname=user_manager_db user=postgres password=postgres host=localhost port=5432")
    print("Connection 1 successful!")
    conn.close()
    conn = psycopg2.connect(
        "dbname=test_db user=postgres password=postgres host=localhost port=5433 options='-c client_encoding=UTF8'"
    )
    conn.set_client_encoding('UTF8')

    print("Connection 2 successful!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
