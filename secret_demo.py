# Open API Service 3 - API key pattern: keep your secrets secret
# The key lives in Streamlit secrets (or an environment variable), never in the code.

import os

import streamlit as st


def get_api_key():
    """Read the key from Streamlit secrets, or from an environment variable."""
    try:
        return st.secrets["MY_API_KEY"]
    except Exception:
        # Fallback for running on your own computer: set the key as an environment variable.
        return os.environ.get("MY_API_KEY")


st.set_page_config(page_title="API Key Demo", layout="centered")
st.title("API Key Demo")
st.caption("Arts and Advanced Big Data | Open API, Service 3")

st.markdown(
    """
The golden rule: never write a key in your code, and never upload it to GitHub.
Public repositories are scanned by bots, and a leaked key can be misused under your name.

This app reads the key from `st.secrets` (or from an environment variable), so the code
itself contains no secret.
"""
)

key = get_api_key()
if not key:
    st.warning("No API key found. Add MY_API_KEY to your app's Secrets.")
    st.stop()

st.success("API key found.")
st.write(f"Key starts with: {key[:3]}***")   # never print the whole key

# A real request would send the key like this:
# requests.get(url, params={"serviceKey": key, ...})
st.caption("Where the key goes when you call a real service: a parameter, or a header.")

st.divider()
st.markdown(
    """
**How to add the secret**

1. On Streamlit Cloud open your app, then *Settings* -> *Secrets*.
2. Add one line, for example `MY_API_KEY = "abcd1234"` (any fake value is fine for practice).
3. Save and reload the app. The warning turns into "API key found".

Running on your own computer? Put the key in `.streamlit/secrets.toml` and add that file
name to `.gitignore` so Git never uploads it.
"""
)

st.caption("No API key is stored in this file. If a key leaks, delete it and create a new one right away.")
