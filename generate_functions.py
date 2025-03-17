# import streamlit as st
# import requests
# import random
# import re
# import auth_token

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
#     """Detects the language of the given text using Google Translate API."""
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
#                 detected_language = detected_language.replace("-Latn", "-IN")
#             if detected_language == "en":
#                 detected_language = "en-IN"
#             return detected_language
#         else:
#             return "en-IN"
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error detecting language: {e}")
#         return "en-IN"

# def translate_text(text, to_language, token):
#     """Translates the given text to the target language using Google Translate API."""
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
#     """Synthesizes speech from text using Google Text-to-Speech API."""
#     api_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
#     headers = {
#         "Content-Type": "application/json",
#         "x-goog-user-project": PROJECT_ID,
#         "Authorization": f"Bearer {token}",
#     }

#     # Determine voice name based on language code
#     voice_name = ""
#     if language_code.endswith('-IN'):
#         voice_name = f"{language_code.replace('-IN', '')}-IN-Wavenet-A"
#         language_code = language_code.replace("-IN", "")
#     elif language_code == "en-US":
#         voice_name = "en-US-Wavenet-D"
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
#         voice_name = "en-IN-Wavenet-A"  # Default to English India if not found

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
#     """Calls the Dialogflow CX API to get the bot's response."""
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
import auth_token

# --- Configuration ---
PROJECT_ID = "heroprojectlivedemo"
AGENT_ID = "dfa3083e-e038-46c1-a006-7cebcdf11038"
LOCATION = "global"

# --- Helper Functions ---

def generate_session_id(length=6):
    """Generates a random session ID."""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(characters) for _ in range(length))

def detect_language_from_text(text, bearer_token):
    """Detects the language of the given text using Google Translate API."""
    api_url = "https://translation.googleapis.com/language/translate/v2/detect"
    headers = {
        "Content-Type": "application/json",
        "x-goog-user-project": PROJECT_ID,
        "Authorization": f"Bearer {bearer_token}",
    }
    data = {"q": text}
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if result.get("data") and result["data"].get("detections"):
            detected_language = result["data"]["detections"][0][0]["language"]
            if "Latn" in detected_language:
                detected_language = detected_language.replace("-Latn", "-IN")
            if detected_language == "en":
                detected_language = "en-IN"
            return detected_language
        else:
            return "en-IN"
    except requests.exceptions.RequestException as e:
        st.error(f"Error detecting language: {e}")
        return "en-IN"

def translate_text(text, to_language, bearer_token):
    """Translates the given text to the target language using Google Translate API."""
    api_url = "https://translation.googleapis.com/language/translate/v2/"
    headers = {
        "Content-Type": "application/json",
        "x-goog-user-project": PROJECT_ID,
        "Authorization": f"Bearer {bearer_token}",
    }
    data = {"q": text, "target": to_language}
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if result.get("data") and result["data"].get("translations"):
            return result["data"]["translations"][0]["translatedText"]
        else:
            return text
    except requests.exceptions.RequestException as e:
        st.error(f"Error translating text: {e}")
        return text

def synthesize_speech(text, language_code, bearer_token):
    """Synthesizes speech from text using Google Text-to-Speech API."""
    api_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    headers = {
        "Content-Type": "application/json",
        "x-goog-user-project": PROJECT_ID,
        "Authorization": f"Bearer {bearer_token}",
    }

    # Determine voice name based on language code
    voice_name = ""
    if language_code.endswith('-IN'):
        voice_name = f"{language_code.replace('-IN', '')}-IN-Wavenet-A"
        language_code = language_code.replace("-IN", "")
    elif language_code == "en-US":
        voice_name = "en-US-Wavenet-D"
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
        voice_name = "en-IN-Wavenet-A"  # Default to English India if not found

    data = {
        "input": {"ssml": text},
        "voice": {
            "languageCode": language_code,
            "name": voice_name,
        },
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "effectsProfileId": ["small-bluetooth-speaker-class-device"],
            "pitch": 0,
            "speakingRate": 1,
        },
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["audioContent"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error synthesizing speech: {e}")
        return None

def call_dialogflow_api(user_message, session_id, language_code, bearer_token):
    """Calls the Dialogflow CX API to get the bot's response."""
    api_url = f"https://{LOCATION}-dialogflow.googleapis.com/v3/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}:detectIntent"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-goog-user-project": PROJECT_ID,
        "Authorization": f"Bearer {bearer_token}",
    }
    data = {
        "queryInput": {
            "text": {"text": user_message},
            "languageCode": language_code.split('-')[0],
        },
        "queryParams": {"timeZone": "America/Los_Angeles"},
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
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
