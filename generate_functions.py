
import streamlit as st
import requests
import random
import re
from google.cloud import translate_v3
from google.cloud import texttospeech
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.protobuf.json_format import MessageToDict


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
    # if to_language == st.session_state.detected_language: 
    #     return text
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

    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
   
    

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
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
        response_dict = MessageToDict(response._pb)
        return response_dict
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
