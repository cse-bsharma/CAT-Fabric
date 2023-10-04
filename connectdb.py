import pyodbc
import threading
import time
import datetime

# Define your Azure SQL Database connection parameters
server_name = "x6eps4xrq2xudenlfv6naeo3i4-bg5peawo7fiejdfosro6pwesuu.msit-datawarehouse.pbidedicated.windows.net"
# server_name = "azsqlv3.sql.azuresynapse.net"
# database_name = "contoso"
database_name = "lakehouse"
# database_name = "azsqldw"
client_id = "35ddfcdd-48a7-4978-9be4-27ab1eb52b6b"
client_secret = "uwQ8Q~CwGz4Tu2SGvclcyMesphIoo-OCuuxXnbH2"
tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"


# Import the sql_queries list from the file
# from query_tpcds import sql_queries
# from TPCH_1TB_LAKE import sql_queries
# from TPCH_1TB import sql_queries
# from TPCH1TB_SQLDW import sql_queries
from query_tpcds_sql_endpoint import sql_queries


# Construct the connection string
connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};" \
                    f"Server={server_name};" \
                    f"Database={database_name};" \
                    f"Authentication=ActiveDirectoryServicePrincipal;" \
                    f"UID={client_id};" \
                    f"PWD={client_secret};" \
                    f"Encrypt=yes;" \
                    f"TrustServerCertificate=no;" \
                    f"Connection Timeout=30;"

# Set this variable to True for multithreading, or False for sequential execution
run_multithreaded = False

# Open a file in write mode to clear its contents
with open("output.txt", "w") as file:
    pass 
def executionlog(log):
    with open("output.txt", "a") as file:
        file.write(log)
# Test_start_time = datetime.datetime.now()
# print(f"Test start time: {Test_start_time}")
def execute_sql(query, thread_id):
    try:
        # Establish the database connection
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        start_time = time.time()
        cursor.execute(query)
        end_time = time.time()
        status=(f"Thread {thread_id}: SQL query execution time: {end_time - start_time} : seconds \n")
        executionlog(status)
    except Exception as e:
        # Handle the exception here
        status=(f"Thread {thread_id}: SQL query failed at : {datetime.datetime.now()} : {str(e)} \n")
        executionlog(status)
    finally:
        # Close the cursor and the database connection
        cursor.close()
        conn.close()


# Create threads for each SQL query if run_multithreaded is True
if run_multithreaded:
    threads = []
    for iteration in range(5):
        for i, query in enumerate(sql_queries):
            thread = threading.Thread(target=execute_sql, args=(query, i + 1))
            threads.append(thread)
    
    # Start the threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
else:
    # Run queries sequentially if run_multithreaded is False
    for i, query in enumerate(sql_queries):
        execute_sql(query, i + 1)
