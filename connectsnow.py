import snowflake.connector
import threading
import time

# Snowflake connection parameters
snowflake_user = 'bsharm36'
snowflake_password = 'April@1988'
snowflake_account = 'xvmzaaz-ql06493'
snowflake_warehouse = 'COMPUTE_WH'
snowflake_database = 'DEMO'
snowflake_schema = 'PUBLIC'

# SQL queries to execute
from tpch_snow import sql_queries

# Number of threads for multithreading
num_threads = 10  # You can adjust this number as needed

# Open a file in write mode to clear its contents
with open("output_snow.txt", "w") as file:
    pass 
def executionlog(log):
    with open("output_snow.txt", "a") as file:
        file.write(log)


# Function to execute a SQL query
def execute_query(query, thread_id):
    try:
        # Establish a Snowflake database connection
        conn = snowflake.connector.connect(
            user=snowflake_user,
            password=snowflake_password,
            account=snowflake_account,
            warehouse=snowflake_warehouse,
            database=snowflake_database,
            schema=snowflake_schema
        )
        cursor = conn.cursor()

        # Execute the SQL query and measure execution time
        start_time = time.time()
        cursor.execute(query)
        end_time = time.time()
        execution_time = end_time - start_time

        status=(f"Thread {thread_id}: Execution Time: {execution_time} seconds\n")
        executionlog(status)

    except Exception as e:
        # Handle query execution exceptions and log to output.txt
        status=(f"Thread {thread_id}: Query Execution Error: {e} \n")
        executionlog(status)

    finally:
        # Close cursor and database connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Choose execution mode (True for multithreading, False for sequential)
    multithreaded_mode = False

    if multithreaded_mode:
        # Multithreaded execution
        threads = []
        for i in range(num_threads):
            for j, query in enumerate(sql_queries):
                thread = threading.Thread(target=execute_query, args=(query, i + 1))
                threads.append(thread)

        # Start and join threads
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    else:
        # Sequential execution
        for i, query in enumerate(sql_queries):
            execute_query(query, i + 1)
