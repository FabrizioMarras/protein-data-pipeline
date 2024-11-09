from src.auth.auth import setup_google_cloud_auth
from src.data.read_files import list_gcs_files, read_gcs_file

def test_read_files():
    """
    Test reading files from Google Cloud Storage bucket and print the content.
    """
    # Step 1: Set up Google Cloud authentication
    setup_google_cloud_auth()
    
    # Step 2: List files in the GCS bucket
    bucket_name = 'fh-public'
    prefix = 'wikicrow2/'
    file_names = list_gcs_files(bucket_name, prefix)
    
    # Step 3: Read and print content of the first file for testing
    if file_names:
        first_file = file_names[0]
        print(f"Reading file: {first_file}")
        content = read_gcs_file(first_file)
        print("\nFile Content Preview:\n", content[:500])  # Print first 500 characters for preview
    else:
        print("No files found in the specified bucket and prefix.")

if __name__ == "__main__":
    test_read_files()
