# import streamlit as st
# import requests
# import random
# import re

# # --- Configuration ---
# PROJECT_ID = "heroprojectlivedemo"
# AGENT_ID = "dfa3083e-e038-46c1-a006-7cebcdf11038"
# LOCATION = "global"

# # --- Helper Functions ---

# def generate_session_id(length=6):
#     """Generates a random session ID."""
#     characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
#     return "".join(random.choice(characters) for _ in range(length))

# def detect_language_from_text(text, token):
#     """Detects the language of the given text using Google Translate API.
#     Args:
#         text (str): The input text.
#         token (str): The bearer token for API authentication.
#     """
#     api_url = "https://translation.googleapis.com/language/translate/v2/detect"
#     headers = {
#         "Content-Type": "application/json",
#         "x-goog-user-project": PROJECT_ID,
#         "Authorization": f"Bearer {token}",
#     }
#     data = {"q": text}
#     try:
#         response = requests.post(api_url, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()
#         if result.get("data") and result["data"].get("detections"):
#             detected_language = result["data"]["detections"][0][0]["language"]
#             if "Latn" in detected_language:
#                 detected_language = detected_language.replace("-Latn", "-US")
#             if detected_language == "en":
#                 detected_language = "en-US"
#             return detected_language
#         else:
#             return "en-US"
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error detecting language: {e}")
#         return "en-US"

# def translate_text(text, to_language, token):
#     """Translates the given text to the target language using Google Translate API.
#       Args:
#         text (str): The input text.
#         to_language (str): The target language code.
#         token (str): The bearer token for API authentication.
#     """
#     api_url = "https://translation.googleapis.com/language/translate/v2/"
#     headers = {
#         "Content-Type": "application/json",
#         "x-goog-user-project": PROJECT_ID,
#         "Authorization": f"Bearer {token}",
#     }
#     data = {"q": text, "target": to_language}
#     try:
#         response = requests.post(api_url, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()
#         if result.get("data") and result["data"].get("translations"):
#             return result["data"]["translations"][0]["translatedText"]
#         else:
#             return text
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error translating text: {e}")
#         return text

# def synthesize_speech(text, language_code, token):
#     """Synthesizes speech from text using Google Text-to-Speech API.
#         Args:
#         text (str): The input text.
#         language_code (str): The target language code.
#         token (str): The bearer token for API authentication.
#     """
#     api_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
#     headers = {
#         "Content-Type": "application/json",
#         "x-goog-user-project": PROJECT_ID,
#         "Authorization": f"Bearer {token}",
#     }

#     # Determine voice name based on language code
#     voice_name = ""
#     if language_code.endswith('-US'):
#         voice_name = f"{language_code.replace('-US', '')}-US-Wavenet-D"
#         language_code = language_code.replace("-US", "")
#     elif language_code == "es":
#         voice_name = "es-ES-Wavenet-B"
#     elif language_code == "fr":
#         voice_name = "fr-FR-Wavenet-B"
#     elif language_code == "de":
#         voice_name = "de-DE-Wavenet-B"
#     elif language_code == "ja":
#         voice_name = "ja-JP-Wavenet-B"
#     elif language_code == "ko":
#         voice_name = "ko-KR-Wavenet-B"
#     elif language_code == "pt":
#         voice_name = "pt-PT-Wavenet-B"
#     elif language_code == "it":
#         voice_name = "it-IT-Wavenet-B"
#     elif language_code == "ru":
#         voice_name = "ru-RU-Wavenet-B"
#     elif language_code == "zh":
#         voice_name = "zh-CN-Wavenet-B"
#     else:
#         voice_name = "en-US-Wavenet-D"  # Default to English US if not found

#     data = {
#         "input": {"ssml": text},
#         "voice": {
#             "languageCode": language_code,
#             "name": voice_name,
#         },
#         "audioConfig": {
#             "audioEncoding": "LINEAR16",
#             "effectsProfileId": ["small-bluetooth-speaker-class-device"],
#             "pitch": 0,
#             "speakingRate": 1,
#         },
#     }
#     try:
#         response = requests.post(api_url, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()
#         return result["audioContent"]
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error synthesizing speech: {e}")
#         return None

# def call_dialogflow_api(user_message, session_id, language_code, token):
#     """Calls the Dialogflow CX API to get the bot's response.
#         Args:
#         user_message (str): The input text.
#         session_id (str): the session id.
#         language_code (str): The target language code.
#         token (str): The bearer token for API authentication.
#     """
#     api_url = f"https://{LOCATION}-dialogflow.googleapis.com/v3/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}:detectIntent"
#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "x-goog-user-project": PROJECT_ID,
#         "Authorization": f"Bearer {token}",
#     }
#     data = {
#         "queryInput": {
#             "text": {"text": user_message},
#             "languageCode": language_code.split('-')[0],
#         },
#         "queryParams": {"timeZone": "America/Los_Angeles"},
#     }
#     try:
#         response = requests.post(api_url, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()
#         return result
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error calling Dialogflow API: {e}")
#         return None

# def remove_links_source_and_quotes(text):
#     """Removes URLs (links), the word "Source" (and variations) before links, and quotes around links from a given text string."""
#     # Regular expression to match URLs
#     url_pattern = re.compile(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

#     # Regular expression to match "Source" or "source" (case-insensitive) followed by optional whitespace and a colon
#     source_pattern = re.compile(r'(?:Source|source)\s*:?\s*', re.IGNORECASE)

#     # Regular expression to match quotes around links
#     quoted_link_pattern = re.compile(r'["\'](https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))["\']')

#     # Find all URLs in the text
#     urls = url_pattern.findall(text)

#     # Remove "Source" and variations before each URL
#     for url in urls:
#         # Find the index of the URL
#         url_index = text.find(url)
#         if url_index != -1:
#             # Search backwards for "Source" or "source"
#             match = source_pattern.search(text, 0, url_index)
#             if match:
#                 # Remove the "Source" part
#                 text = text[:match.start()] + text[match.end():]

#     # Remove quotes around links
#     text = quoted_link_pattern.sub(r'\1', text)

#     # Remove the URLs
#     text = url_pattern.sub('', text)
#     return text



import streamlit as st
import requests
import random
import re
from google.cloud import translate_v3
from google.cloud import texttospeech
from google.cloud import dialogflowcx_v3beta1 as dialogflow

# --- Configuration ---
PROJECT_ID = "heroprojectlivedemo"
AGENT_ID = "dfa3083e-e038-46c1-a006-7cebcdf11038"
LOCATION = "global"
PARENT = f"projects/{PROJECT_ID}/locations/{LOCATION}"

# --- Helper Functions ---

def generate_session_id(length=6):
    """Generates a random session ID."""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(characters) for _ in range(length))

def detect_language_from_text(text):
    """Detects the language of the given text using Google Translate API.
    Args:
        text (str): The input text.
        token (str): The bearer token for API authentication.
    """
    client = translate_v3.TranslationServiceClient()
    try:
        response = client.detect_language(
            content=text,
            parent=PARENT,
            mime_type="text/plain"
        )
        detected_language = response.languages[0].language_code
        if "Latn" in detected_language:
            detected_language = detected_language.replace("-Latn", "-US")
        if detected_language == "en":
            detected_language = "en-US"
        return detected_language
    except Exception as e:
        st.error(f"Error detecting language: {e}")
        return "en-US"

def translate_text(text, to_language):
    """Translates the given text to the target language using Google Translate API.
      Args:
        text (str): The input text.
        to_language (str): The target language code.
        token (str): The bearer token for API authentication.
    """
    client = translate_v3.TranslationServiceClient()
    try:
        response = client.translate_text(
            contents=[text],
            target_language_code=to_language,
            parent=PARENT,
            mime_type="text/plain",
            source_language_code="en-US",
        )
        return response.translations[0].translated_text
    except Exception as e:
        st.error(f"Error translating text: {e}")
        return text

def synthesize_speech(text, language_code):
    """Synthesizes speech from text using Google Text-to-Speech API.
        Args:
        text (str): The input text.
        language_code (str): The target language code.
        token (str): The bearer token for API authentication.
    """
    client = texttospeech.TextToSpeechClient()
    # Determine voice name based on language code
    voice_name = ""
    if language_code.endswith('-US'):
        voice_name = f"{language_code.replace('-US', '')}-US-Wavenet-D"
        language_code = language_code.replace("-US", "")
    elif language_code == "es":
        voice_name = "es-ES-Wavenet-B"
    elif language_code == "fr":
        voice_name = "fr-FR-Wavenet-B"
    elif language_code == "de":
        voice_name = "de-DE-Wavenet-B"
    elif language_code == "ja":
        voice_name = "ja-JP-Wavenet-B"
    elif language_code == "ko":
        voice_name = "ko-KR-Wavenet-B"
    elif language_code == "pt":
        voice_name = "pt-PT-Wavenet-B"
    elif language_code == "it":
        voice_name = "it-IT-Wavenet-B"
    elif language_code == "ru":
        voice_name = "ru-RU-Wavenet-B"
    elif language_code == "zh":
        voice_name = "zh-CN-Wavenet-B"
    else:
        voice_name = "en-US-Wavenet-D"  # Default to English US if not found

    input_text = texttospeech.SynthesisInput(ssml=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        effects_profile_id=["small-bluetooth-speaker-class-device"],
        pitch=0,
        speaking_rate=1,
    )
    try:
        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return response.audio_content
    except Exception as e:
        st.error(f"Error synthesizing speech: {e}")
        return None

def call_dialogflow_api(user_message, session_id, language_code):
    """Calls the Dialogflow CX API to get the bot's response.
        Args:
        user_message (str): The input text.
        session_id (str): the session id.
        language_code (str): The target language code.
        token (str): The bearer token for API authentication.
    """
    client = dialogflow.SessionsClient()
    session = f"{PARENT}/agents/{AGENT_ID}/sessions/{session_id}"
    text_input = dialogflow.TextInput(text=user_message)
    query_input = dialogflow.QueryInput(text=text_input,  language_code=language_code.split('-')[0])
    try:
        response = client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        st.info(f"Response: {response}")
        return response.__dict__()
    except Exception as e:
        st.error(f"Error calling Dialogflow API: {e}")
        return None

def remove_links_source_and_quotes(text):
    """Removes URLs (links), the word "Source" (and variations) before links, and quotes around links from a given text string."""
    # Regular expression to match URLs
    url_pattern = re.compile(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

    # Regular expression to match "Source" or "source" (case-insensitive) followed by optional whitespace and a colon
    source_pattern = re.compile(r'(?:Source|source)\s*:?\s*', re.IGNORECASE)

    # Regular expression to match quotes around links
    quoted_link_pattern = re.compile(r'["\'](https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))["\']')

    # Find all URLs in the text
    urls = url_pattern.findall(text)

    # Remove "Source" and variations before each URL
    for url in urls:
        # Find the index of the URL
        url_index = text.find(url)
        if url_index != -1:
            # Search backwards for "Source" or "source"
            match = source_pattern.search(text, 0, url_index)
            if match:
                # Remove the "Source" part
                text = text[:match.start()] + text[match.end():]

    # Remove quotes around links
    text = quoted_link_pattern.sub(r'\1', text)

    # Remove the URLs
    text = url_pattern.sub('', text)
    return text
