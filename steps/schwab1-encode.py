import base64

def generate_basic_auth_header(username, password):
    # Concatenate the username and password separated by a colon
    user_pass = f"{username}:{password}"
    
    # Encode the user_pass string into Base64
    encoded_credentials = base64.b64encode(user_pass.encode()).decode()
    
    # Construct the Authorization header value
    auth_header = f"Basic {encoded_credentials}"
    
    return auth_header

# Example usage
username = "Aladdin"
password = "open sesame"

auth_header = generate_basic_auth_header(username, password)
print("Authorization Header:", auth_header)
