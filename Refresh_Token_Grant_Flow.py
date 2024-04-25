import datetime
import time
import json
from oauth_utils import OAuthClient

# def check_access_token_validity(oauth_client):
#     if oauth_client.is_token_valid("refresh_token_data.json"):
#         print("Access token is valid.")
#         return True
#     else:
#         print("Access token has expired.")
#         return False

# def check_refresh_token_validity(oauth_client):
#     if oauth_client.refresh_token:
#         print("Refresh token is available.")
#         return True
#     else:
#         print("Refresh token is not available.")
#         return False

# def manage_tokens(oauth_client):
#     # Check if access token is valid
#     if check_access_token_validity(oauth_client):
#         return

#     # Check if refresh token is available
#     if check_refresh_token_validity(oauth_client):
#         # Perform token refresh
#         oauth_client.refresh_access_token()
#         return

#     # If no refresh token is available, perform authorization code grant flow
#     oauth_client.authorization_code_grant_flow()

if __name__ == "__main__":
    # Initialize OAuthClient with credentials and token files
    oauth_client = OAuthClient(credentials_file="credentials.json", grant_flow_type_filenames_file = 'grant_flow_type_filenames.json')

    # Manage tokens to ensure continuous access
    # manage_tokens(oauth_client)
    oauth_client.manage_tokens()


# if __name__ == "__main__":
#     credentials_file = 'credentials.json'
#     token_file1 = 'authorization_code_token_data.json'
#     token_file2 = "client_credentials_token_data.json"
#     token_file3 = "refresh_token_data.json"
#     grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'

#     # Create OAuthClient instance
#     oauth_client = OAuthClient(
#         credentials_file, grant_flow_type_filenames_file
#     )
#     # oauth_client.manage_tokens()
#     # oauth_client.authorization_code_grant_flow()
#     # print("Access token:", oauth_client.access_token)
#     # print("Refresh token:", oauth_client.refresh_token)

