"""
authorization_code_grant_flow.py

This script implements the Authorization Code Grant Flow for obtaining OAuth tokens.

The flow involves the following steps:
1. Redirect the user to the authorization endpoint.
2. Obtain the authorization code from the callback URL after user authorization.
3. Exchange the authorization code for access and refresh tokens.
4. Print the obtained tokens for verification.
"""



import json
from oauth_utils import OAuthClient

if __name__ == "__main__":
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    # token_file = 'authorization_code_token_data.json'

    # Create OAuthClient instance
    oauth_client = OAuthClient(
        credentials_file, grant_flow_type_filenames_file
    )

    oauth_client.authorization_code_grant_flow()
    print("Access token:", oauth_client.access_token)
    print("Refresh token:", oauth_client.refresh_token)
