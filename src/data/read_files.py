import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import storage
import os

from src.auth.auth import setup_google_cloud_auth

def list_gcs_files(bucket_name, prefix):
    """
    Lists all the files in the GCS bucket under the specified prefix.
    """
    # Set up Google Cloud authentication
    setup_google_cloud_auth()
    
    # Initialize the Cloud Storage client
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    
    # Get the list of file names
    file_names = [blob.name for blob in blobs if blob.name.endswith('.txt')]
    return file_names

def read_gcs_file(blob_name):
    """
    Reads the content of a GCS blob.
    """
    # Initialize the Cloud Storage client
    client = storage.Client()
    bucket = client.bucket('fh-public')
    blob = bucket.blob(blob_name)
    content = blob.download_as_text()
    return content

def run_read_files_pipeline(bucket_name, prefix):
    """
    Runs the Apache Beam pipeline to read files from GCS and returns a PCollection.
    """
    file_names = list_gcs_files(bucket_name, prefix)
    
    def read_file_to_dict(blob_name):
        content = read_gcs_file(blob_name)
        return {
            'gene_name': os.path.basename(blob_name).replace('.txt', ''),
            'content': content,
            'structure_file_path': None,
            'source': 'Google Cloud Storage'
        }
    
    return file_names, read_file_to_dict
