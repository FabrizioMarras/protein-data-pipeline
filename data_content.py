from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam as beam

from src.auth.auth import setup_google_cloud_auth
from src.data.read_files import run_read_files_pipeline
from src.data.write_to_db import write_to_database

def main():
    # Set up Google Cloud authentication
    setup_google_cloud_auth()

    # Define your bucket and prefix
    bucket_name = 'fh-public'
    prefix = 'wikicrow2/'

    # Get the list of files and function to read them
    file_names, read_file_to_dict = run_read_files_pipeline(bucket_name, prefix)

    # Initialize Apache Beam pipeline options
    pipeline_options = PipelineOptions()

    # Create an Apache Beam pipeline
    with beam.Pipeline(options=pipeline_options) as pipeline:
        # Read files and create records
        protein_records = (
            pipeline
            | 'Create File Names' >> beam.Create(file_names)
            | 'Read Files' >> beam.Map(read_file_to_dict)
        )

        # Write the records to the database
        write_to_database(pipeline, protein_records)

    print("All files have been processed and loaded into the database.")

if __name__ == '__main__':
    main()
