# import streamlit as st
# import os
# # from dotenv import load_dotenv
# from google.oauth2 import id_token
# from google.auth.transport import requests

# # load_dotenv()

# def authentication():
#     GOOGLE_CLIENT_ID = "633630984866-qj00anvn6cu2kahus5ft1cnc4o8pe7dp.apps.googleusercontent.com"  # Replace with your client ID

#     def verify_token(token):
#         try:
#             # Verify the token with Google's servers
#             idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

#             # Check if the token is from the correct audience (your client ID)
#             if idinfo['aud'] != GOOGLE_CLIENT_ID:
#                 raise ValueError('Wrong audience.')

#             return token  # Return the token if valid
#         except ValueError as e:
#             print(e)
#             return "Invalid"
#         except Exception as e:
#             print(e)
#             return "Error"

#     # Get the token from the query parameter
#     token = st.query_params.get("token", "")

#     print("Token from new: ", token)
#     if not token:
#         st.error("Unauthorized access. Token not provided.")
#         st.stop()

#     # Verify the token
#     decoded = verify_token(token)

#     if decoded == "Invalid":
#         st.error("Invalid token. Access denied.")
#         st.stop()
#     elif decoded == "Error":
#         st.error("Error in token verification. Access denied.")
#         st.stop()
#     else:
#         return decoded  # Return the valid token


import streamlit as st
import os
from google.oauth2 import id_token
from google.auth.transport import requests
import google.auth

project="heroprojectlivedemo"
def authentication():
    GOOGLE_CLIENT_ID = "633630984866-qj00anvn6cu2kahus5ft1cnc4o8pe7dp.apps.googleusercontent.com"  # Replace with your client ID

    def verify_token(token):
        try:
            # Verify the token with Google's servers
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

            # Check if the token is from the correct audience (your client ID)
            if idinfo['aud'] != GOOGLE_CLIENT_ID:
                raise ValueError('Wrong audience.')

            return token  # Return the token if valid
        except ValueError as e:
            print(e)
            return "Invalid"
        except Exception as e:
            print(e)
            return "Error"

    # Get the token from the query parameter
    token = st.query_params.get("token", "")

    print("Token from new: ", token)
    if not token:
        st.error("Unauthorized access. Token not provided.")
        st.stop()

    # Verify the token
    decoded = verify_token(token)

    if decoded == "Invalid":
        st.error("Invalid token. Access denied.")
        st.stop()
    elif decoded == "Error":
        st.error("Error in token verification. Access denied.")
        st.stop()
    else:
        return decoded  # Return the valid token

def get_bearer_token():
    """Gets a bearer token from the default service account."""
    try:
        # Get the default credentials
        st.info("Getting bearer token")
        creds, project = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",  # For general Cloud access
                "https://www.googleapis.com/auth/dialogflow", # For Dialogflow
                "https://www.googleapis.com/auth/cloud-translation", # For translation
                "https://www.googleapis.com/auth/cloud-texttospeech", # For text to speech
            ]
        )
        st.info(f"Bearer 1:  {creds.token}")
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        # print("Bearer " ,creds.token)
        # print("Project: ", project )
        st.info(f"Project: { project}")
        # Return the access token
        return creds.token
    except Exception as e:
        st.error(f"Error getting bearer token: {e}")
        return None
