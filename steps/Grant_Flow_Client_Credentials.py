"""
client_credentials_code_grant_flow.py

This script implements the Client Credentials Code Grant Flow for obtaining OAuth tokens.

"""
import json
from OauthClient import OAuthClient

# Main function to perform OAuth client credentials grant flow
if __name__ == "__main__":
    # File paths for credentials and token data
    credentials_file = 'credentials.json'
    token_file = "client_credentials_token_data.json"

    # Create OAuthClient instance with credentials file and token file paths
    oauth_client = OAuthClient(credentials_file, token_file)

    # Perform client credentials grant flow
    oauth_client.client_credentials_grant_flow()

    # Print obtained access token and refresh token
    print("Access token:", oauth_client.access_token)
    print("Refresh token:", oauth_client.refresh_token)
