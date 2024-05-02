from SchwabAPIClient import SchwabAPIClient


if __name__ == "__main__":
    # Initialize SchwabAPIClient with credentials and base URL
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'

    client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)

    tick = client.get_ticker_data("AAPL")
    print(tick)