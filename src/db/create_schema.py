from db.db_connection import connect_to_db  

def create_proteins_table():
    """Creates the 'proteins' table in the database."""
    connection = connect_to_db()
    if connection is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS proteins (
            gene_name VARCHAR(255) PRIMARY KEY,
            content TEXT,
            structure_file_path VARCHAR(500),
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source VARCHAR(100)
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'proteins' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    create_proteins_table()
