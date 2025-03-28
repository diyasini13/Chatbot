# import streamlit as st
# import base64
# from generate_functions import generate_session_id, detect_language_from_text, call_dialogflow_api, translate_text, synthesize_speech, remove_links_source_and_quotes
# import auth_token

# # --- Configuration ---
# PROJECT_ID = "heroprojectlivedemo"
# AGENT_ID = "dfa3083e-e038-46c1-a006-7cebcdf11038"
# LOCATION = "global"

# # --- Streamlit App ---
# def app(token): 
#     # Pass the token as an argument
#     # if not token:
#     #     st.error("Failed to get access token. Check service account credentials.")
#     #     return
#     st.title("Google Agent")

#     # Initialize session state variables
#     if "session_id" not in st.session_state:
#         st.session_state.session_id = generate_session_id()
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
#     if "detected_language" not in st.session_state:
#         st.session_state.detected_language = "en-IN"

#     # Display chat history
#     for message in st.session_state.chat_history:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # User input (text)
#     if prompt := st.chat_input("Enter your message here"):
#         user_message = prompt
#         st.session_state.chat_history.append({"role": "user", "content": user_message})
#         with st.chat_message("user"):
#             st.markdown(user_message)

#         # Process user message
#         with st.chat_message("assistant"):
#             message_placeholder = st.empty()
#             full_response = ""

#             # Detect language
#             st.session_state.detected_language = detect_language_from_text(user_message, token) # Pass the token

#             # Call Dialogflow API
#             dialogflow_response = call_dialogflow_api(
#                 user_message, st.session_state.session_id, st.session_state.detected_language, token # Pass the token
#             )

#             if dialogflow_response and dialogflow_response.get("queryResult"):
#                 bot_responses = dialogflow_response["queryResult"]["responseMessages"]
#                 all_text_responses = []
#                 for response in bot_responses:
#                     if response.get("text"):
#                         text_response = response["text"]["text"][0]
#                         translated_text = translate_text(
#                             text_response, st.session_state.detected_language, token # Pass the token
#                         )
#                         all_text_responses.append(translated_text)
#                         full_response += translated_text + " "
#                 message_placeholder.markdown(full_response)

#                 # Synthesize speech and play automatically
#                 if all_text_responses:
#                     full_response_for_audio = " ".join(all_text_responses)

#                     # Remove links, "Source" text, and quotes before synthesizing speech
#                     text_to_synthesize = remove_links_source_and_quotes(full_response_for_audio)

#                     audio_content = synthesize_speech(
#                         text_to_synthesize, st.session_state.detected_language, token # Pass the token
#                     )
#                     if audio_content:
#                         audio_bytes = base64.b64decode(audio_content)
#                         st.audio(audio_bytes, format="audio/wav", start_time=0, )
#             else:
#                 full_response = "Sorry, I couldn't understand that."
#                 message_placeholder.markdown(full_response)
#                 audio_content = synthesize_speech(
#                             full_response, st.session_state.detected_language, token # Pass the token
#                         )
#                 if audio_content:
#                     audio_bytes = base64.b64decode(audio_content)
#                     st.audio(audio_bytes, format="audio/wav", start_time=0)

#             st.session_state.chat_history.append({"role": "assistant", "content": full_response})

# if __name__ == "__main__":
#     token = auth_token.authentication() # Get the token
#     app(token)  # Pass the token to the app function

import streamlit as st
import base64
from generate_functions import generate_session_id, detect_language_from_text, call_dialogflow_api, translate_text, synthesize_speech, remove_links_source_and_quotes
import auth_token

# --- Configuration ---
PROJECT_ID = "heroprojectlivedemo"
AGENT_ID = "dfa3083e-e038-46c1-a006-7cebcdf11038"
LOCATION = "global"

# --- Streamlit App ---
def app(bearer_token): 
    
    st.title("Google Agent")

    # Initialize session state variables
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "detected_language" not in st.session_state:
        st.session_state.detected_language = "en-IN"

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input (text)
    if prompt := st.chat_input("Enter your message here"):
        user_message = prompt
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        # Process user message
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Detect language
            st.session_state.detected_language = detect_language_from_text(user_message, bearer_token) # Pass the right token

            # Call Dialogflow API
            dialogflow_response = call_dialogflow_api(
                user_message, st.session_state.session_id, st.session_state.detected_language, bearer_token # Pass the right token
            )

            if dialogflow_response and dialogflow_response.get("queryResult"):
                bot_responses = dialogflow_response["queryResult"]["responseMessages"]
                all_text_responses = []
                for response in bot_responses:
                    if response.get("text"):
                        text_response = response["text"]["text"][0]
                        translated_text = translate_text(
                            text_response, st.session_state.detected_language, bearer_token # Pass the right token
                        )
                        all_text_responses.append(translated_text)
                        full_response += translated_text + " "
                message_placeholder.markdown(full_response)

                # Synthesize speech and play automatically
                if all_text_responses:
                    full_response_for_audio = " ".join(all_text_responses)

                    # Remove links, "Source" text, and quotes before synthesizing speech
                    text_to_synthesize = remove_links_source_and_quotes(full_response_for_audio)

                    audio_content = synthesize_speech(
                        text_to_synthesize, st.session_state.detected_language, bearer_token # Pass the right token
                    )
                    if audio_content:
                        audio_bytes = base64.b64decode(audio_content)
                        st.audio(audio_bytes, format="audio/wav", start_time=0, )
            else:
                full_response = "Sorry, I couldn't understand that."
                message_placeholder.markdown(full_response)
                audio_content = synthesize_speech(
                            full_response, st.session_state.detected_language, bearer_token # Pass the right token
                        )
                if audio_content:
                    audio_bytes = base64.b64decode(audio_content)
                    st.audio(audio_bytes, format="audio/wav", start_time=0)

            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    bearer_token = auth_token.get_bearer_token() #get the bearer token first
    print("BEARER TOKEN: ", bearer_token)
    if not bearer_token:
        st.error("Failed to get access token. Check service account credentials.")
    else :
        id_token = auth_token.authentication() # Get the id token
        if not id_token:
            st.error("Unauthenticated")
        else:
            app(bearer_token)  # Pass only the bearer token to the app function
