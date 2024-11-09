import os
from dotenv import load_dotenv

def setup_google_cloud_auth():
    """
    Sets up authentication for Google Cloud services by loading credentials
    from the environment variable and setting the appropriate OS environment variable.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get the path to the service account key file
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    if not credentials_path:
        raise EnvironmentError('GOOGLE_APPLICATION_CREDENTIALS not set in .env file.')

    # Set the environment variable for Google Cloud authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    print("Google Cloud authentication has been set up.")
