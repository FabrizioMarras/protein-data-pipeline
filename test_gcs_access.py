from src.auth.auth import setup_google_cloud_auth
from google.cloud import storage

def test_authentication():
    """
    Test if authentication with Google Cloud is working by listing blobs
    in the public bucket 'my-protein-structures-bucket'.
    """
    # Set up Google Cloud authentication
    setup_google_cloud_auth()

    try:
        # Initialize the Cloud Storage client
        client = storage.Client()

        # Access the public bucket
        bucket_name = 'my-protein-structures-bucket'  # Replace with your actual bucket name
        bucket = client.bucket(bucket_name)
       # Verify if the bucket exists
        if not bucket.exists():
            print(f"Bucket '{bucket_name}' does not exist.")
            return

        print(f"Successfully accessed bucket '{bucket_name}'.")

        # List blobs in the bucket (if any)
        blobs = bucket.list_blobs()
        print("Accessible blobs:")
        for blob in blobs:
            print(blob.name)

    except Exception as e:
        print(f"Authentication failed: {e}")

if __name__ == "__main__":
    test_authentication()