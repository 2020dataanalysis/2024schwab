# get_option_chain.py

from SchwabAPIClient import SchwabAPIClient


if __name__ == "__main__":
    credentials_file = "credentials.json"
    grant_flow_type_filenames_file = "grant_flow_type_filenames.json"

    client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)

    symbol = "AAPL"  # or SPY/QQQ/etc.

    chain = client.get_option_chain(
        symbol=symbol,
        contractType="ALL",            # calls + puts
        strikeCount=10,                # 10 strikes above/below ATM
        includeUnderlyingQuote=True,
        strategy="SINGLE",             # raw chain; we’ll build BWB/condor ourselves
        # fromDate="2025-12-01",       # optional filters
        # toDate="2026-01-31",
        # expMonth="ALL",
        # entitlement="PN",            # if needed for your token
    )

    print(chain)
