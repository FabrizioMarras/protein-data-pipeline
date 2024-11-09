from google.cloud import storage

def count_gcs_files(bucket_name, prefix):
    """
    Counts the number of files in a Google Cloud Storage bucket under a specific prefix.
    """
    # Initialize the Cloud Storage client
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    
    # Count the number of files
    file_count = sum(1 for _ in blobs)
    return file_count

if __name__ == "__main__":
    bucket_name = 'fh-public'
    prefix = 'wikicrow2/'
    
    print("Counting files in the bucket...")
    num_files = count_gcs_files(bucket_name, prefix)
    print(f"Total number of files in '{bucket_name}/{prefix}': {num_files}")
