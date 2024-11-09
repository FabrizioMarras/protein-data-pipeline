import apache_beam as beam
from src.db.db_connection import connect_to_db

class WriteToDatabase(beam.DoFn):
    """
    A DoFn class for writing protein records to the database.
    """
    def setup(self):
        self.connection = connect_to_db()
        if self.connection is None:
            raise Exception("Failed to connect to the database.")
        self.cursor = self.connection.cursor()

    def process(self, element):
        gene_name = element.get('gene_name')
        content = element.get('content')
        structure_file_path = element.get('structure_file_path')
        source = element.get('source', 'Unknown')

        insert_query = '''
        INSERT INTO proteins (gene_name, content, structure_file_path, source)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (gene_name) DO UPDATE SET
            content = EXCLUDED.content,
            structure_file_path = EXCLUDED.structure_file_path,
            source = EXCLUDED.source,
            date_added = CURRENT_TIMESTAMP;
        '''

        try:
            self.cursor.execute(insert_query, (gene_name, content, structure_file_path, source))
            self.connection.commit()
            yield f"Inserted/Updated record for gene: {gene_name}"
        except Exception as e:
            self.connection.rollback()
            print(f"Error inserting record for gene {gene_name}: {e}")

    def teardown(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'connection'):
            self.connection.close()

def write_to_database(pipeline, protein_records):
    """
    Function to write records to the database using Apache Beam.
    """
    return protein_records | 'Write To DB' >> beam.ParDo(WriteToDatabase())
