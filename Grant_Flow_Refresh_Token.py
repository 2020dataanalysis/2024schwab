import datetime
import time
import json
from oauth_utils import OAuthClient

if __name__ == "__main__":
    # Initialize OAuthClient with credentials and token files
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    oauth_client = OAuthClient(credentials_file, grant_flow_type_filenames_file)

    # Manage tokens to ensure continuous access
    # manage_tokens(oauth_client)
    oauth_client.manage_tokens()
