from src.auth.auth import setup_google_cloud_auth
from src.data.read_files import list_gcs_files, read_gcs_file
from src.data.write_to_db import WriteToDatabase
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def test_write_to_db():
    """
    Test reading a single file and writing its content to the database.
    """
    print("Setting up Google Cloud authentication...")
    setup_google_cloud_auth()
    
    print("Listing files in the GCS bucket...")
    bucket_name = 'fh-public'
    prefix = 'wikicrow2/'
    file_names = list_gcs_files(bucket_name, prefix)
    
    if not file_names:
        print("No files found in the specified bucket and prefix.")
        return
    
    print(f"Found files: {file_names}")
    
    # Read the first file for testing
    first_file = file_names[0]
    print(f"Reading file: {first_file}")
    content = read_gcs_file(first_file)
    
    print("Preparing test record...")
    test_record = {
        'gene_name': first_file.replace('.txt', '').split('/')[-1],
        'content': content,
        'structure_file_path': None,
        'source': 'Google Cloud Storage'
    }
    
    print(f"Test record prepared: {test_record}")
    
    pipeline_options = PipelineOptions()

    # Create an Apache Beam pipeline
    with beam.Pipeline(options=pipeline_options) as pipeline:
        records = pipeline | 'Create Test Record' >> beam.Create([test_record])
        
        # Debug print to ensure record creation
        records | 'Print Record' >> beam.Map(lambda x: print(f"Inserting record: {x}"))
        
        # Write the records to the database using ParDo with the DoFn class
        records | 'Write To DB' >> beam.ParDo(WriteToDatabase())
    
    print("Test pipeline executed successfully.")

if __name__ == "__main__":
    test_write_to_db()
