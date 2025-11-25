Here’s a `README.md` you can drop straight into the repo. It includes a **sample** `credentials.json` (really a template) and makes it clear the real one should never go in git.

````markdown
# 2024schwab – Schwab Trader API Client

This project is a Python client for the Schwab Trader API, with helpers for:

- Handling OAuth token management
- Refreshing tokens periodically
- Making authenticated requests (e.g. getting quotes, account info)

It uses:

- `SchwabAPIClient` for REST calls
- `OAuthClient` for authorization-code + refresh-token flows
- Local JSON files under `private/` to store credentials and tokens

> ⚠️ **Important:** Your real `private/credentials.json` and token files **must NOT** be committed to GitHub. Use the sample below as a template only.

---

## 1. Prerequisites

- Python 3.9+ (project currently tested with 3.9)
- Schwab Developer account
- A registered Schwab application with:
  - **App Key** (Client ID / Consumer Key)
  - **App Secret**
  - **Redirect / Callback URL** (e.g. `https://127.0.0.1`)

Clone the repo:

```bash
git clone https://github.com/2020dataanalysis/2024schwab.git
cd 2024schwab
````

Create and activate a virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate   # on macOS/Linux
# .venv\Scripts\activate    # on Windows
```

Install dependencies (if `requirements.txt` exists):

```bash
pip install -r requirements.txt
```

---

## 2. Directory Layout (Relevant Parts)

```text
2024schwab/
  config/
    config.json           # holds base URLs and "private" path
  private/
    credentials.json      # REAL secrets (not committed)
    credentials_template.json   # SAMPLE/template (safe to commit)
    authorization_code_token.json      # created by OAuth flow
    refresh_token.json                # created by OAuth flow
    client_credentials_token_data.json # (optional/other flow)
  SchwabAPIClient.py
  OauthClient.py
  token_refresh_service.py
  get_price.py
```

The `SchwabAPIClient` constructor is called like:

```python
client = SchwabAPIClient(credentials_file="credentials.json",
                         grant_flow_type_filenames_file="grant_flow_type_filenames.json")
```

and `OAuthClient` internally loads `private/credentials.json`.

---

## 3. Sample `credentials_template.json`

Create a template file at:

```text
private/credentials_template.json
```

with the following content:

```json
{
  "app_key": "REPLACE_WITH_YOUR_SCHWAB_APP_KEY",
  "app_secret": "REPLACE_WITH_YOUR_SCHWAB_APP_SECRET",
  "redirect_uri": "https://127.0.0.1",

  "authorization_endpoint": "https://api.schwabapi.com/v1/oauth/authorize",
  "token_url": "https://api.schwabapi.com/v1/oauth/token"
}
```

### Field meanings

* **app_key**
  Your Schwab **App Key** (Client ID / Consumer Key) from the Schwab Developer Portal.
  Use the **raw** key value, e.g. `wiGqC23BInMwpuEXEDGawAAhVkNyHk4w`
  *(do NOT add `@APP_NAME`)*

* **app_secret**
  Your Schwab application secret (also from the Developer Portal).

* **redirect_uri**
  The callback URL you registered with Schwab (e.g. `https://127.0.0.1`).
  This **must match exactly** what’s configured on the Schwab Developer Portal.

* **authorization_endpoint**
  Schwab OAuth authorize URL:
  `https://api.schwabapi.com/v1/oauth/authorize`

* **token_url**
  Schwab OAuth token exchange URL:
  `https://api.schwabapi.com/v1/oauth/token`

---

## 4. Creating Your Real `credentials.json`

1. Copy the template:

   ```bash
   cp private/credentials_template.json private/credentials.json
   ```

2. Edit `private/credentials.json` and replace:

   * `"REPLACE_WITH_YOUR_SCHWAB_APP_KEY"` → your real App Key
   * `"REPLACE_WITH_YOUR_SCHWAB_APP_SECRET"` → your real App Secret
   * `"https://127.0.0.1"` → your real redirect URI if different

3. **Do not** commit `private/credentials.json` or any token files.

---

## 5. `.gitignore` – Keep Secrets & Tokens Out of Git

Add (or confirm) the following entries in `.gitignore`:

```gitignore
# Virtualenv / IDE
.venv/
venv/
.idea/
__pycache__/
*.pyc

# Schwab credentials and token files
private/credentials.json
private/authorization_code_token.json
private/refresh_token.json
private/client_credentials_token_data.json
refresh_token.log
```

`private/credentials_template.json` *is* safe to commit; `credentials.json` is not.

---

## 6. First-Time OAuth Flow

On first run, there is no valid token yet, so the client will:

1. Detect that `refresh_token.json` (or other token file) is missing/invalid.

2. Print an authorization URL like:

   ```text
   Please visit the following URL and authorize the application:
   https://api.schwabapi.com/v1/oauth/authorize?client_id=YOUR_APP_KEY&redirect_uri=https://127.0.0.1&response_type=code
   ```

3. You must:

   * Copy that URL into a browser
   * Log in to Schwab
   * Approve the app
   * Wait for redirect to your `redirect_uri` (e.g. `https://127.0.0.1/?code=...&session=...`)

4. Copy the **full callback URL** from your browser’s address bar.

5. When the script prompts:

   ```text
   Paste the FULL callback URL from your browser (starting with https://127.0.0.1/...):
   >
   ```

   paste the **entire** URL there and press Enter.

`OAuthClient` will parse out the `code=...` parameter, exchange it for access & refresh tokens, and write them to the token JSON files under `private/`.

Subsequent runs will use the refresh token and no longer prompt you unless the refresh token becomes invalid.

---

## 7. Quick Test: Get AAPL Quote

The repo includes a simple smoke test script, `get_price.py`:

```python
# get_price.py

from SchwabAPIClient import SchwabAPIClient


if __name__ == "__main__":
    credentials_file = "credentials.json"
    grant_flow_type_filenames_file = "grant_flow_type_filenames.json"

    client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)

    tick = client.get_ticker_data("AAPL")
    print(tick)
```

Run it with your venv active:

```bash
python get_price.py
```

On first run, you’ll go through the OAuth steps described above.
Once tokens are stored, subsequent runs should print a JSON blob with the AAPL quote and exit with code 0.

---

## 8. Known Warning on macOS (LibreSSL)

On macOS you may see a warning like:

```text
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'.
```

This is a **warning**, not a fatal error. The client should still function.

If desired, you can quiet this by:

* Using a Homebrew Python with OpenSSL, or
* Pinning `urllib3` to `<2.0` in `requirements.txt`:

```text
urllib3<2.0
```

---

## 9. Token Refresh Service

There is also a `token_refresh_service.py` that can keep the access token refreshed in the background by calling `refresh_token_timer()` periodically.

Run it with:

```bash
python token_refresh_service.py
```

This will:

* Initialize `SchwabAPIClient`
* Start an async loop that refreshes the token before expiry
* Log to `refresh_token.log`

Make sure you’ve completed the initial OAuth flow first (via `get_price.py` or another entrypoint).

---

## 10. Security Reminder

* Never commit real secrets (`credentials.json`) or token JSON files.
* Rotate your Schwab credentials if you suspect they’ve been exposed.
* Treat your `private/` folder as sensitive.

For collaborators, instruct them to:

1. Copy `private/credentials_template.json` → `private/credentials.json`
2. Fill in their own keys from the Schwab Developer Portal
3. Run `get_price.py` to complete their own OAuth flow.

```

::contentReference[oaicite:0]{index=0}
```
