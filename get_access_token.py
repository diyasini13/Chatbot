import os
from google.oauth2 import id_token
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
import google.auth
import streamlit as st

def get_access_token(id_token_string, GOOGLE_CLIENT_ID):
    """
    Exchanges a Google ID token for an access token that can be used to call Google Cloud APIs.

    Args:
        id_token_string: The Google ID token string.
        GOOGLE_CLIENT_ID: The client ID of your Google Cloud project.

    Returns:
        An access token string, or None if an error occurred.
    """
    try:
        # Verify the ID token
        idinfo = id_token.verify_oauth2_token(id_token_string, requests.Request(), GOOGLE_CLIENT_ID)

        # Check if the token is from the correct audience (your client ID)
        if idinfo['aud'] != GOOGLE_CLIENT_ID:
            raise ValueError('Wrong audience.')

        # Get default credentials
        creds, project = google.auth.default()

        # Create a Credentials object from the ID token
        credentials = Credentials(
            token=id_token_string,
            id_token=id_token_string,
        )

        # Refresh the credentials to get an access token
        credentials.refresh(requests.Request())

        # Return the access token
        return credentials.token

    except ValueError as e:
        st.error(f"Invalid ID token: {e}")
        return None
    except Exception as e:
        st.error(f"Error getting access token: {e}")
        return None
