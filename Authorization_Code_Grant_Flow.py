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
from urllib.parse import unquote
from oauth_utils import OAuthClient


def get_authorization_code(authorization_endpoint, client_id, redirect_uri):
    """
    Redirects the user to the authorization endpoint and prompts the user to input the authorization code.

    Args:
        authorization_endpoint (str): The OAuth authorization endpoint URL.
        client_id (str): The client ID of the OAuth application.
        redirect_uri (str): The redirect URI where the authorization server will redirect the user after authorization.

    Returns:
        str: The authorization code obtained from the user.
    """
    # Redirect the user to the authorization endpoint
    authorization_url = (
        f"{authorization_endpoint}?client_id={client_id}"
        f"&redirect_uri={redirect_uri}&response_type=code"
    )
    print("Please visit the following URL and authorize the application:")
    print(authorization_url)

    # After user authorization, the authorization code will be obtained via the redirect URI
    authorization_code_url = input(
        "Enter the authorization code from the callback URL: "
    )

    # Find the index of 'code=' and '&session=' in the URL
    code_index = authorization_code_url.find('code=')
    session_index = authorization_code_url.find('&session=')

    # Extract the authorization code using the indices
    if code_index != -1 and session_index != -1:
        authorization_code_extracted = (
            authorization_code_url[code_index + len('code='):session_index]
        )
    else:
        # Handle case where either 'code=' or '&session=' is not found
        authorization_code_extracted = None

    print("Extracted Authorization Code:", authorization_code_extracted)
    authorization_code = unquote(authorization_code_extracted)
    print("Extracted Authorization Code URL decoded:", authorization_code)
    return authorization_code


if __name__ == "__main__":
    # Define file paths and URLs
    credentials_file = 'credentials.json'
    oauth_tokens_file = 'oauth_tokens.json'
    token_url = 'https://api.schwabapi.com/v1/oauth/token'
    base_url = 'https://api.schwabapi.com/trader/v1'
    authorization_endpoint = 'https://api.schwabapi.com/v1/oauth/authorize'
    redirect_uri = 'https://127.0.0.1'  # Replace with your actual redirect URI

    # Load credentials from file
    with open(credentials_file, 'r') as f:
        credentials = json.load(f)

    # Extract relevant credentials
    client_id = credentials.get("app_key")

    # Get the authorization code
    authorization_code = get_authorization_code(
        authorization_endpoint, client_id, redirect_uri
    )
    print("Authorization code:", authorization_code)

    oauth_client = OAuthClient(
        credentials_file, oauth_tokens_file, token_url
    )
    # tokens = exchange_code_for_token(oauth_client, authorization_code)
    tokens = oauth_client.get_refresh_token(authorization_code)
    # print(f'tokens: {tokens}')
    print(f'refresh: {oauth_client.refresh_token}')
    print(f'access: {oauth_client.access_token}')
