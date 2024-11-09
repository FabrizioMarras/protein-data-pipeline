from src.db.db_connection import connect_to_db

def fetch_protein_data(gene_name):
    """
    Fetches the content of a specific gene from the database.
    """
    # Connect to the database
    connection = connect_to_db()
    if connection is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        # Query to fetch the data for the given gene_name
        query = '''
        SELECT gene_name, content, structure_file_path, date_added, source
        FROM proteins
        WHERE gene_name = %s;
        '''
        cursor.execute(query, (gene_name,))
        result = cursor.fetchone()

        if result:
            print("\nFetched data for gene:", result[0])
            print("Content:\n", result[1])
            print("Structure File Path:", result[2])
            print("Date Added:", result[3])
            print("Source:", result[4])
        else:
            print(f"No data found for gene: {gene_name}")

    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    # Specify the gene_name you want to fetch
    gene_name_to_fetch = 'A1BG'  # Replace with the gene name you want to fetch
    fetch_protein_data(gene_name_to_fetch)
