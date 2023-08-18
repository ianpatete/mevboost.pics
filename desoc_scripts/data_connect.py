import psycopg2
import csv
import os

# Database Configuration
POSTGRES_DB = 'hub'
POSTGRES_USER = 'app'
POSTGRES_PASSWORD = 'password'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 6541

# Establishing Connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    with conn.cursor() as cur:
        cur.execute("SET jit TO 'off';")
    return conn

# Export query results to CSV
def query_to_csv(query, filename):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Execute the query
    cur.execute(query)
    
    # Fetch results
    results = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    
    # Write results to CSV
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(column_names)  # Write header
        writer.writerows(results)      # Write data
    
    cur.close()
    conn.close()

# Your provided SQL query
query = """
SELECT c.timestamp,
       c.created_at,
       c.fid,
       c.text,
       encode(c.hash, 'hex') as hash_encode,
       encode(c.parent_hash, 'hex') as parent_hash_encode,
       c.mentions,
       c.embeds
FROM casts c
ORDER BY 1 DESC
"""

# Specifying the path to save the CSV file
filename = "casts_output.csv"
query_to_csv(query, filename)