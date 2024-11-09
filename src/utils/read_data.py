from auth.auth import setup_google_cloud_auth
from google.cloud import storage

def read_data():
    """
    Reads data from the public GCS bucket and prints the content of each file.
    """
    # Set up Google Cloud authentication
    setup_google_cloud_auth()

    try:
        # Initialize the Cloud Storage client
        client = storage.Client()

        # # Access the public bucket
        bucket = client.bucket('fh-public')
        
#         # List blobs in the 'wikicrow2/' directory
#         blobs = bucket.list_blobs(prefix='wikicrow2/')

#         print("Files in 'wikicrow2/':")
#         for blob in blobs:
#             # Exclude directories (if any)
#             if not blob.name.endswith('/'):
#                 # Print the filename without the 'wikicrow2/' prefix
#                 print(blob.name.replace('wikicrow2/', ''))

#     except Exception as e:
#         print(f"Error listing files: {e}")

# if __name__ == "__main__":
#     read_data()

        # Specify the file to read
        blob_name = 'wikicrow2/XPNPEP1.txt'

        # Get the blob (file) object
        blob = bucket.blob(blob_name)

        print(f"Reading data from {blob_name}...")
        # Download the blob's content as a string
        content = blob.download_as_text()
        print("\n--- File Content ---")
        print(content)
                        # # List blobs in the specified prefix
                        # blobs = bucket.list_blobs(prefix='wikicrow2/')

                        # print("Reading data from GCS bucket...")
                        # for blob in blobs:
                        #     print(f"\n--- Content of {blob.name} ---")
                        #     # Download the blob's content as a string
                        #     content = blob.download_as_text()
                        #     print(content)

    except Exception as e:
        print(f"Error reading data: {e}")

if __name__ == "__main__":
    read_data()
