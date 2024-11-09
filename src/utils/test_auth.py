from ..auth.auth import setup_google_cloud_auth
from google.cloud import storage

def test_authentication():
    """
    Test if authentication with Google Cloud is working by listing blobs
    in the public bucket 'fh-public' under the 'wikicrow2/' prefix.
    """
    # Set up Google Cloud authentication
    setup_google_cloud_auth()

    try:
        # Initialize the Cloud Storage client
        client = storage.Client()

        # Access the public bucket
        bucket = client.bucket('fh-public')

        # List blobs in the specified prefix
        blobs = bucket.list_blobs(prefix='wikicrow2/')

        print("Authentication successful. Accessible blobs:")
        for blob in blobs:
            print(blob.name)

    except Exception as e:
        print(f"Authentication failed: {e}")

if __name__ == "__main__":
    test_authentication()
