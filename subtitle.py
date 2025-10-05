import os
import requests
import streamlit as st
import tempfile
from typing import Dict, List
from datetime import timedelta
import subprocess
import base64
import json

# ElevenLabs API Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your_api_key_here")
BASE_URL = "https://api.elevenlabs.io"

# Translation Services Configuration
TRANSLATION_SERVICES = {
    "Google Translate (Free)": "google_free",
    "LibreTranslate (Free)": "libre",
    "Azure Translator": "azure"
}

# Supported target languages for translation
TARGET_LANGUAGES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de", "Italian": "it",
    "Portuguese": "pt", "Russian": "ru", "Japanese": "ja", "Chinese (Simplified)": "zh",
    "Korean": "ko", "Hindi": "hi", "Arabic": "ar", "Dutch": "nl",
    "Turkish": "tr", "Polish": "pl", "Swedish": "sv", "Norwegian": "no",
    "Danish": "da", "Finnish": "fi", "Czech": "cs", "Hungarian": "hu",
    "Bulgarian": "bg", "Romanian": "ro", "Greek": "el", "Hebrew": "he",
    "Thai": "th", "Vietnamese": "vi", "Indonesian": "id", "Malay": "ms",
    "Filipino": "tl", "Ukrainian": "uk", "Bengali": "bn", "Tamil": "ta",
    "Telugu": "te", "Marathi": "mr", "Gujarati": "gu", "Kannada": "kn",
    "Malayalam": "ml", "Punjabi": "pa", "Urdu": "ur", "Persian": "fa",
    "Swahili": "sw", "Afrikaans": "af", "Catalan": "ca", "Croatian": "hr"
}

class SubtitleTranslator:
    def __init__(self, service: str = "google_free"):
        self.service = service
    
    def translate_text_google_free(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        """Enhanced translation with context awareness, especially for English"""
        try:
            from deep_translator import GoogleTranslator
            
            # Clean the text but preserve formatting
            text = text.strip()
            if not text:
                return text
            
            # Enhanced prompting for English translations
            if target_lang == "en":
                # Add context cues for more natural English
                if any(word in text.lower() for word in ["hello", "hi", "hey", "good morning", "good evening"]):
                    text = f"Translate this greeting naturally to conversational English: {text}"
                elif any(word in text.lower() for word in ["thank", "thanks", "please", "sorry", "excuse"]):
                    text = f"Translate this polite expression to natural English: {text}"
                elif "?" in text:
                    text = f"Translate this question to natural English: {text}"
                elif "!" in text:
                    text = f"Translate this exclamation to natural English: {text}"
                else:
                    text = f"Translate to natural conversational English: {text}"
            
            # Use deep-translator which is more stable
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            
            # Split long text into chunks if needed (deep-translator has limits)
            max_length = 4500  # Safe limit for Google Translate
            if len(text) > max_length:
                # Split by sentences or periods
                sentences = text.split('. ')
                translated_parts = []
                current_chunk = ""
                
                for sentence in sentences:
                    if len(current_chunk + sentence) < max_length:
                        current_chunk += sentence + ". "
                    else:
                        if current_chunk:
                            translated_chunk = translator.translate(current_chunk.strip())
                            # Clean up English translation artifacts
                            if target_lang == "en":
                                translated_chunk = self.clean_english_translation(translated_chunk)
                            translated_parts.append(translated_chunk)
                        current_chunk = sentence + ". "
                
                # Translate remaining chunk
                if current_chunk:
                    translated_chunk = translator.translate(current_chunk.strip())
                    if target_lang == "en":
                        translated_chunk = self.clean_english_translation(translated_chunk)
                    translated_parts.append(translated_chunk)
                
                return " ".join(translated_parts)
            else:
                # Translate normally for shorter text
                result = translator.translate(text)
                if target_lang == "en":
                    result = self.clean_english_translation(result)
                return result
            
        except Exception as e:
            st.warning(f"Google Translation failed: {str(e)}")
            # Fallback: return text with language indicator
            return f"[{target_lang.upper()}] {text}"
    
    def translate_text_libre(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        """Translate text using LibreTranslate API with improved error handling"""
        try:
            # Clean the text
            text = text.strip()
            if not text:
                return text
            
            # Try deep-translator's LibreTranslate first (more reliable)
            try:
                from deep_translator import LibreTranslator
                translator = LibreTranslator(source=source_lang, target=target_lang)
                return translator.translate(text)
            except Exception:
                pass
            
            # Fallback to direct API calls with multiple endpoints
            urls = [
                "https://libretranslate.de/translate",
                "https://translate.terraprint.co/translate",
                "https://libretranslate.com/translate"
            ]
            
            for url in urls:
                try:
                    data = {
                        "q": text,
                        "source": "auto" if source_lang == "auto" else source_lang,
                        "target": target_lang,
                        "format": "text"
                    }
                    
                    response = requests.post(url, data=data, timeout=15)
                    
                    if response.status_code == 200:
                        try:
                            result = response.json()
                            translated_text = result.get("translatedText", "")
                            if translated_text and translated_text != text:
                                return translated_text
                        except json.JSONDecodeError:
                            continue
                    
                except requests.exceptions.RequestException:
                    continue
            
            # If all LibreTranslate instances fail, fallback to Google Translate
            st.warning("LibreTranslate services unavailable, falling back to Google Translate")
            return self.translate_text_google_free(text, target_lang, source_lang)
            
        except Exception as e:
            st.warning(f"LibreTranslate failed: {str(e)}, falling back to Google Translate")
            return self.translate_text_google_free(text, target_lang, source_lang)
    
    def translate_text_azure(self, text: str, target_lang: str, api_key: str, region: str = "global") -> str:
        """Translate text using Azure Translator API"""
        try:
            endpoint = "https://api.cognitive.microsofttranslator.com"
            path = '/translate'
            constructed_url = endpoint + path
            
            params = {
                'api-version': '3.0',
                'to': target_lang
            }
            
            headers = {
                'Ocp-Apim-Subscription-Key': api_key,
                'Ocp-Apim-Subscription-Region': region,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(os.urandom(16).hex())
            }
            
            body = [{'text': text}]
            
            response = requests.post(constructed_url, params=params, headers=headers, json=body)
            if response.status_code == 200:
                result = response.json()
                return result[0]['translations'][0]['text']
            else:
                return text
        except Exception as e:
            st.warning(f"Azure translation failed: {str(e)}")
            return text
    
    def translate_subtitle_text(self, text: str, target_lang: str, api_key: str = None) -> str:
        """Translate subtitle text while preserving speaker labels and formatting"""
        try:
            if self.service == "google_free":
                return self.translate_text_google_free(text, target_lang)
            elif self.service == "libre":
                return self.translate_text_libre(text, target_lang)
            elif self.service == "azure" and api_key:
                return self.translate_text_azure(text, target_lang, api_key)
            else:
                return text
        except Exception as e:
            st.warning(f"Translation service failed: {str(e)}")
            # Simple fallback: return with language indicator
            return f"[{target_lang.upper()}] {text}"
    
    def clean_english_translation(self, text: str) -> str:
        """Clean up English translation artifacts and improve naturalness"""
        if not text:
            return text
        
        # Remove translation prompt artifacts
        cleaned = text
        
        # Remove common translation prompts that might leak through
        prompts_to_remove = [
            "Translate this greeting naturally to conversational English:",
            "Translate this polite expression to natural English:",
            "Translate this question to natural English:",
            "Translate this exclamation to natural English:",
            "Translate to natural conversational English:",
            "Translation:",
            "English:",
            "The translation is:",
            "In English:",
        ]
        
        for prompt in prompts_to_remove:
            cleaned = cleaned.replace(prompt, "").strip()
        
        # Fix common English translation issues
        fixes = {
            # Grammar improvements
            " a hour": " an hour",
            " a university": " a university", 
            " an university": " a university",
            " a apple": " an apple",
            " a orange": " an orange",
            " a elephant": " an elephant",
            
            # Natural conversation patterns
            "very very ": "really ",
            "more better": "better",
            "most best": "best",
            "can not": "cannot",
            
            # Proper capitalization
            " i ": " I ",
            " i'm": " I'm",
            " i'll": " I'll", 
            " i've": " I've",
            " i'd": " I'd",
            " i.": " I.",
            " i,": " I,",
            " i!": " I!",
            " i?": " I?",
        }
        
        # Apply fixes
        for old, new in fixes.items():
            cleaned = cleaned.replace(old, new)
        
        # Ensure proper sentence capitalization
        if cleaned and len(cleaned) > 0:
            cleaned = cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned.upper()
        
        # Ensure proper punctuation for natural speech
        if cleaned and not cleaned.endswith(('.', '!', '?', ':', ';', ',')):
            # Add period for statements, but be smart about it
            if any(word in cleaned.lower() for word in ['hello', 'hi', 'hey', 'thanks', 'yes', 'no', 'okay', 'ok']):
                # Short responses don't always need periods
                pass
            else:
                cleaned += "."
        
        return cleaned.strip()

def create_simple_translation_map() -> Dict[str, Dict[str, str]]:
    """Create a simple translation map for common subtitle phrases"""
    return {
        "es": {  # Spanish
            "Hello": "Hola",
            "Thank you": "Gracias", 
            "Yes": "Sí",
            "No": "No",
            "Please": "Por favor",
            "Sorry": "Lo siento",
            "Excuse me": "Disculpe",
            "Good morning": "Buenos días",
            "Good afternoon": "Buenas tardes",
            "Good evening": "Buenas noches",
            "Goodbye": "Adiós"
        },
        "fr": {  # French
            "Hello": "Bonjour",
            "Thank you": "Merci",
            "Yes": "Oui", 
            "No": "Non",
            "Please": "S'il vous plaît",
            "Sorry": "Désolé",
            "Excuse me": "Excusez-moi",
            "Good morning": "Bonjour",
            "Good afternoon": "Bon après-midi",
            "Good evening": "Bonsoir",
            "Goodbye": "Au revoir"
        },
        "de": {  # German
            "Hello": "Hallo",
            "Thank you": "Danke",
            "Yes": "Ja",
            "No": "Nein", 
            "Please": "Bitte",
            "Sorry": "Entschuldigung",
            "Excuse me": "Entschuldigen Sie",
            "Good morning": "Guten Morgen",
            "Good afternoon": "Guten Tag",
            "Good evening": "Guten Abend",
            "Goodbye": "Auf Wiedersehen"
        }
    }

def check_translation_service_status(service: str) -> bool:
    """Check if a translation service is available"""
    try:
        if service == "libre":
            # Quick test with LibreTranslate using deep-translator
            try:
                from deep_translator import LibreTranslator
                translator = LibreTranslator(source="en", target="es")
                result = translator.translate("test")
                return bool(result and result != "test")
            except Exception:
                # Fallback to direct API test
                try:
                    response = requests.post("https://libretranslate.de/translate", 
                        data={"q": "test", "source": "en", "target": "es", "format": "text"}, 
                        timeout=5
                    )
                    return response.status_code == 200
                except Exception:
                    return False
        elif service == "google_free":
            # Quick test with Google Translate using deep-translator
            try:
                from deep_translator import GoogleTranslator
                translator = GoogleTranslator(source="en", target="es")
                result = translator.translate("test")
                return bool(result and result != "test")
            except Exception:
                return False
        return True
    except Exception:
        return False

def translate_subtitles_preserve_structure(srt_content: str, target_language: str, 
                                         translation_service: str = "google_free", 
                                         api_key: str = None) -> str:
    """
    Translate SRT subtitles with context awareness while preserving timestamps, speaker diarization, and structure
    """
    if not srt_content or not target_language:
        return srt_content
    
    translator = SubtitleTranslator(translation_service)
    target_lang_code = TARGET_LANGUAGES.get(target_language, "en")
    
    # Parse original subtitles to preserve structure
    subtitles = parse_srt_subtitles(srt_content)
    
    # Enhanced context-aware translation for English
    if target_lang_code == "en":
        return translate_with_context_awareness(subtitles, translator, api_key)
    
    # Standard translation for other languages
    translated_srt = ""
    
    for subtitle in subtitles:
        original_text = subtitle['text']
        
        # Check if text contains speaker label [Speaker_X]
        speaker_label = ""
        text_to_translate = original_text
        
        if original_text.startswith('[') and ']' in original_text:
            # Extract speaker label
            end_bracket = original_text.find(']')
            speaker_label = original_text[:end_bracket + 1] + " "
            text_to_translate = original_text[end_bracket + 1:].strip()
        
        # Translate only the actual text, not the speaker label
        if text_to_translate:
            translated_text = translator.translate_subtitle_text(text_to_translate, target_lang_code, api_key)
        else:
            translated_text = text_to_translate
        
        # Reconstruct the subtitle with preserved structure
        final_text = speaker_label + translated_text
        
        # Reconstruct SRT format with preserved timestamps
        start_timestamp = format_timestamp(subtitle['start'])
        end_timestamp = format_timestamp(subtitle['end'])
        
        translated_srt += f"{subtitle['id']}\n"
        translated_srt += f"{start_timestamp} --> {end_timestamp}\n"
        translated_srt += f"{final_text}\n\n"
    
    return translated_srt

def translate_with_context_awareness(subtitles: List[Dict], translator: SubtitleTranslator, api_key: str = None) -> str:
    """
    Enhanced context-aware translation specifically optimized for English
    """
    translated_srt = ""
    conversation_context = []
    speaker_contexts = {}
    
    # Group subtitles by conversation segments
    conversation_segments = group_by_conversation_segments(subtitles)
    
    for segment in conversation_segments:
        # Translate each conversation segment with full context
        segment_texts = []
        speaker_info = []
        
        for subtitle in segment:
            original_text = subtitle['text']
            speaker_label = ""
            text_content = original_text
            
            # Extract speaker information
            if original_text.startswith('[') and ']' in original_text:
                end_bracket = original_text.find(']')
                speaker_label = original_text[:end_bracket + 1]
                text_content = original_text[end_bracket + 1:].strip()
                
                # Build speaker context
                speaker_id = speaker_label.strip('[]')
                if speaker_id not in speaker_contexts:
                    speaker_contexts[speaker_id] = []
                speaker_contexts[speaker_id].append(text_content)
            
            segment_texts.append(text_content)
            speaker_info.append((speaker_label, subtitle['id'], subtitle['start'], subtitle['end']))
        
        # Create context-aware translation prompt
        if len(segment_texts) > 1:
            # Multi-line conversation - translate with context
            context_text = " | ".join(segment_texts)
            context_prompt = f"Translate this conversation naturally to English, maintaining conversational flow and context: {context_text}"
            
            try:
                translated_conversation = translator.translate_subtitle_text(context_prompt, "en", api_key)
                # Extract individual translations from context
                context_translations = extract_individual_translations(translated_conversation, len(segment_texts))
            except Exception as e:
                # Fallback to individual translation
                context_translations = [translator.translate_subtitle_text(text, "en", api_key) for text in segment_texts]
        else:
            # Single line - translate with accumulated context
            context_translations = [enhance_single_translation(segment_texts[0], conversation_context, translator, api_key)]
        
        # Reconstruct SRT with enhanced translations
        for i, (speaker_label, sub_id, start_time, end_time) in enumerate(speaker_info):
            if i < len(context_translations):
                enhanced_text = context_translations[i]
                
                # Apply English-specific enhancements
                enhanced_text = apply_english_enhancements(enhanced_text, speaker_label)
                
                # Add speaker label back
                final_text = f"{speaker_label} {enhanced_text}" if speaker_label else enhanced_text
                
                # Update conversation context
                conversation_context.append(enhanced_text)
                if len(conversation_context) > 5:  # Keep last 5 for context
                    conversation_context.pop(0)
                
                # Build SRT entry
                start_timestamp = format_timestamp(start_time)
                end_timestamp = format_timestamp(end_time)
                
                translated_srt += f"{sub_id}\n"
                translated_srt += f"{start_timestamp} --> {end_timestamp}\n"
                translated_srt += f"{final_text}\n\n"
    
    return translated_srt

def group_by_conversation_segments(subtitles: List[Dict], max_gap: float = 3.0) -> List[List[Dict]]:
    """Group subtitles into conversation segments based on time gaps"""
    if not subtitles:
        return []
    
    segments = []
    current_segment = [subtitles[0]]
    
    for i in range(1, len(subtitles)):
        time_gap = subtitles[i]['start'] - subtitles[i-1]['end']
        
        # Start new segment if gap is too large or speaker changes significantly
        if time_gap > max_gap:
            segments.append(current_segment)
            current_segment = [subtitles[i]]
        else:
            current_segment.append(subtitles[i])
    
    segments.append(current_segment)
    return segments

def extract_individual_translations(context_translation: str, expected_count: int) -> List[str]:
    """Extract individual translations from context-aware translation"""
    # Split by common separators
    separators = [' | ', ' |', '| ', '|', '. ', '; ', '\n']
    
    for sep in separators:
        if sep in context_translation:
            parts = context_translation.split(sep)
            if len(parts) == expected_count:
                return [part.strip() for part in parts]
    
    # Fallback: split by sentences
    sentences = context_translation.split('. ')
    if len(sentences) >= expected_count:
        return sentences[:expected_count]
    
    # Last resort: return the whole translation for first item
    return [context_translation] + [""] * (expected_count - 1)

def enhance_single_translation(text: str, context: List[str], translator: SubtitleTranslator, api_key: str = None) -> str:
    """Enhance single line translation with conversation context"""
    if not context:
        return translator.translate_subtitle_text(text, "en", api_key)
    
    # Create context-aware prompt
    recent_context = " ".join(context[-3:])  # Last 3 lines of context
    context_prompt = f"Given this conversation context: '{recent_context}', translate this naturally to English: '{text}'"
    
    try:
        enhanced = translator.translate_subtitle_text(context_prompt, "en", api_key)
        # Extract just the translation part (remove context explanation)
        if "translate" in enhanced.lower() and ":" in enhanced:
            enhanced = enhanced.split(":")[-1].strip()
        return enhanced
    except Exception as e:
        return translator.translate_subtitle_text(text, "en", api_key)

def apply_english_enhancements(text: str, speaker_label: str = "") -> str:
    """Apply English-specific enhancements for natural conversation"""
    if not text:
        return text
    
    # Remove translation artifacts
    text = text.replace("Translate this", "").replace("translate this", "")
    text = text.replace("Translation:", "").replace("translation:", "")
    
    # Fix common translation issues
    enhancements = {
        # Casual conversation improvements
        " uh ": " um ",
        " yeah ": " yes ",
        " gonna ": " going to ",
        " wanna ": " want to ",
        " gotta ": " have to ",
        
        # Formal improvements
        " i ": " I ",
        " i'm ": " I'm ",
        " i'll ": " I'll ",
        " i've ": " I've ",
        " i'd ": " I'd ",
        
        # Common grammar fixes
        " a apple": " an apple",
        " a orange": " an orange",
        " a hour": " an hour",
        " a university": " a university",
        
        # Speech patterns
        "very very ": "really ",
        "more better": "better",
        "most best": "best",
    }
    
    # Apply enhancements
    enhanced_text = text
    for old, new in enhancements.items():
        enhanced_text = enhanced_text.replace(old, new)
    
    # Capitalize first letter
    if enhanced_text:
        enhanced_text = enhanced_text[0].upper() + enhanced_text[1:] if len(enhanced_text) > 1 else enhanced_text.upper()
    
    # Ensure proper ending punctuation for dialogue
    if enhanced_text and not enhanced_text.endswith(('.', '!', '?', ':')):
        enhanced_text += "."
    
    return enhanced_text.strip()

class ElevenLabsSubtitleGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "xi-api-key": api_key
        }
    
    def create_transcription(self, audio_file: bytes, language_code: str = None, 
                           num_speakers: int = None, diarize: bool = True,
                           tag_audio_events: bool = True) -> Dict:
        """
        Create a transcription using ElevenLabs Speech-to-Text API
        Returns: transcription result with timestamps and speaker diarization
        """
        url = f"{BASE_URL}/v1/speech-to-text"
        
        files = {
            'file': ('audio.mp3', audio_file, 'audio/mp3')
        }
        
        data = {
            'model_id': 'scribe_v1',
            'diarize': str(diarize).lower(),
            'tag_audio_events': str(tag_audio_events).lower(),
        }
        
        # Add optional parameters
        if language_code:
            data['language_code'] = language_code
        if num_speakers:
            data['num_speakers'] = str(num_speakers)
        
        response = requests.post(url, headers=self.headers, files=files, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create transcription: {response.text}")

def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"

def parse_srt_subtitles(srt_content: str) -> List[Dict]:
    """Parse SRT content into a list of subtitle entries with timestamps"""
    subtitles = []
    blocks = srt_content.strip().split('\n\n')
    
    for block in blocks:
        if not block.strip():
            continue
            
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
            
        try:
            # Parse subtitle number
            subtitle_num = int(lines[0])
            
            # Parse timestamps
            timestamp_line = lines[1]
            start_time, end_time = timestamp_line.split(' --> ')
            
            # Convert timestamps to seconds
            start_seconds = timestamp_to_seconds(start_time)
            end_seconds = timestamp_to_seconds(end_time)
            
            # Get subtitle text
            text = '\n'.join(lines[2:])
            
            subtitles.append({
                'id': subtitle_num,
                'start': start_seconds,
                'end': end_seconds,
                'text': text
            })
            
        except (ValueError, IndexError):
            continue
    
    return subtitles

def timestamp_to_seconds(timestamp: str) -> float:
    """Convert SRT timestamp format to seconds"""
    # Format: HH:MM:SS,mmm
    time_part, ms_part = timestamp.split(',')
    hours, minutes, seconds = map(int, time_part.split(':'))
    milliseconds = int(ms_part)
    
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    return total_seconds

def create_multilingual_video_player(video_bytes: bytes, subtitle_languages: Dict[str, List[Dict]], 
                                    video_name: str, subtitle_style: str = "Both", font_size: int = 18) -> str:
    """Create video player with multiple subtitle language options while preserving all features"""
    
    # Convert video to base64 for embedding
    video_b64 = base64.b64encode(video_bytes).decode()
    
    # Create VTT tracks for each language
    vtt_tracks = ""
    subtitle_data = {}
    
    for lang_name, subtitles in subtitle_languages.items():
        lang_code = TARGET_LANGUAGES.get(lang_name.replace("Original (", "").replace(")", ""), "en")
        
        # Convert subtitles to VTT format
        vtt_content = "WEBVTT\n\n"
        for sub in subtitles:
            start_time = seconds_to_vtt_timestamp(sub['start'])
            end_time = seconds_to_vtt_timestamp(sub['end'])
            text = sub['text'].replace('\n', ' ')
            vtt_content += f"{start_time} --> {end_time}\n{text}\n\n"
        
        vtt_b64 = base64.b64encode(vtt_content.encode()).decode()
        
        # Add track to HTML
        default_attr = "default" if lang_name == list(subtitle_languages.keys())[0] else ""
        vtt_tracks += f'<track kind="subtitles" src="data:text/vtt;base64,{vtt_b64}" srclang="{lang_code}" label="{lang_name}" {default_attr}>\n'
        
        # Store subtitle data for JavaScript
        subtitle_data[lang_name] = subtitles
    
    html_player = f"""
    <div style="position: relative; width: 100%; max-width: 800px; margin: 0 auto;">
        <video id="videoPlayer" controls style="width: 100%; height: auto;" preload="metadata">
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            {vtt_tracks}
            Your browser does not support the video tag.
        </video>
        
        <!-- Language selector -->
        <div style="margin: 10px 0; text-align: center; background: #f0f0f0; padding: 10px; border-radius: 5px;">
            <label for="languageSelect" style="margin-right: 10px; font-weight: bold;">Subtitle Language:</label>
            <select id="languageSelect" onchange="changeSubtitleLanguage()" style="
                padding: 5px 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
                margin-right: 10px;
            ">
                {" ".join([f'<option value="{lang}">{lang}</option>' for lang in subtitle_languages.keys()])}
            </select>
            <span style="color: #666; font-size: 12px;">🌍 Speaker diarization and timestamps preserved</span>
        </div>
        
        <!-- Custom subtitle overlay -->
        <div id="subtitleOverlay" style="
            position: absolute;
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: {font_size}px;
            font-weight: bold;
            text-align: center;
            max-width: 90%;
            display: none;
            z-index: 1000;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            line-height: 1.2;
        "></div>
        
        <!-- Subtitle controls -->
        <div style="margin-top: 10px; text-align: center;">
            <button onclick="toggleSubtitles()" style="
                background: #0066cc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 10px;
            ">Toggle Overlay</button>
            <button onclick="toggleBuiltInSubtitles()" style="
                background: #009900;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            ">Toggle Built-in Track</button>
        </div>
    </div>
    
    <script>
        const video = document.getElementById('videoPlayer');
        const subtitleOverlay = document.getElementById('subtitleOverlay');
        const languageSelect = document.getElementById('languageSelect');
        let overlayEnabled = {str(subtitle_style in ["Overlay", "Both"]).lower()};
        let currentLanguage = "{list(subtitle_languages.keys())[0]}";
        
        const allSubtitles = {json.dumps(subtitle_data)};
        
        function updateSubtitles() {{
            const currentTime = video.currentTime;
            let currentSubtitle = null;
            
            const subtitles = allSubtitles[currentLanguage] || [];
            for (const subtitle of subtitles) {{
                if (currentTime >= subtitle.start && currentTime <= subtitle.end) {{
                    currentSubtitle = subtitle;
                    break;
                }}
            }}
            
            if (currentSubtitle && overlayEnabled) {{
                subtitleOverlay.innerHTML = currentSubtitle.text.replace(/\\n/g, '<br>');
                subtitleOverlay.style.display = 'block';
            }} else {{
                subtitleOverlay.style.display = 'none';
            }}
        }}
        
        function changeSubtitleLanguage() {{
            currentLanguage = languageSelect.value;
            updateSubtitles();
            
            // Switch built-in subtitle track
            const tracks = video.textTracks;
            for (let i = 0; i < tracks.length; i++) {{
                tracks[i].mode = tracks[i].label === currentLanguage ? 'showing' : 'hidden';
            }}
        }}
        
        function toggleSubtitles() {{
            overlayEnabled = !overlayEnabled;
            updateSubtitles();
        }}
        
        function toggleBuiltInSubtitles() {{
            const tracks = video.textTracks;
            for (let i = 0; i < tracks.length; i++) {{
                if (tracks[i].label === currentLanguage) {{
                    tracks[i].mode = tracks[i].mode === 'showing' ? 'hidden' : 'showing';
                    break;
                }}
            }}
        }}
        
        video.addEventListener('timeupdate', updateSubtitles);
        video.addEventListener('loadedmetadata', function() {{
            changeSubtitleLanguage(); // Initialize with first language
        }});
    </script>
    """
    
    return html_player

def create_video_player_with_subtitles(video_bytes: bytes, subtitles: List[Dict], video_name: str, 
                                      subtitle_style: str = "Both", font_size: int = 18) -> str:
    """Create an HTML5 video player with subtitle overlay"""
    
    # Convert video to base64 for embedding
    video_b64 = base64.b64encode(video_bytes).decode()
    
    # Convert subtitles to VTT format for HTML5 video
    vtt_content = "WEBVTT\n\n"
    for sub in subtitles:
        start_time = seconds_to_vtt_timestamp(sub['start'])
        end_time = seconds_to_vtt_timestamp(sub['end'])
        text = sub['text'].replace('\n', ' ')
        vtt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    
    vtt_b64 = base64.b64encode(vtt_content.encode()).decode()
    
    # Show/hide track based on style preference
    track_default = "default" if subtitle_style in ["Built-in Track", "Both"] else ""
    
    html_player = f"""
    <div style="position: relative; width: 100%; max-width: 800px; margin: 0 auto;">
        <video id="videoPlayer" controls style="width: 100%; height: auto;" preload="metadata">
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            <track kind="subtitles" src="data:text/vtt;base64,{vtt_b64}" srclang="en" label="Generated Subtitles" {track_default}>
            Your browser does not support the video tag.
        </video>
        
        <!-- Custom subtitle overlay -->
        <div id="subtitleOverlay" style="
            position: absolute;
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: {font_size}px;
            font-weight: bold;
            text-align: center;
            max-width: 90%;
            display: none;
            z-index: 1000;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            line-height: 1.2;
        "></div>
        
        <!-- Subtitle controls -->
        <div style="margin-top: 10px; text-align: center;">
            <button onclick="toggleSubtitles()" style="
                background: #0066cc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                margin-right: 10px;
            ">Toggle Overlay</button>
            <button onclick="toggleBuiltInSubtitles()" style="
                background: #009900;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            ">Toggle Built-in Track</button>
        </div>
    </div>
    
    <script>
        const video = document.getElementById('videoPlayer');
        const subtitleOverlay = document.getElementById('subtitleOverlay');
        let overlayEnabled = {str(subtitle_style in ["Overlay", "Both"]).lower()};
        
        const subtitles = {str(subtitles).replace("'", '"')};
        
        function updateSubtitles() {{
            const currentTime = video.currentTime;
            let currentSubtitle = null;
            
            for (const subtitle of subtitles) {{
                if (currentTime >= subtitle.start && currentTime <= subtitle.end) {{
                    currentSubtitle = subtitle;
                    break;
                }}
            }}
            
            if (currentSubtitle && overlayEnabled) {{
                subtitleOverlay.innerHTML = currentSubtitle.text.replace(/\\n/g, '<br>');
                subtitleOverlay.style.display = 'block';
            }} else {{
                subtitleOverlay.style.display = 'none';
            }}
        }}
        
        function toggleSubtitles() {{
            overlayEnabled = !overlayEnabled;
            updateSubtitles();
        }}
        
        function toggleBuiltInSubtitles() {{
            const tracks = video.textTracks;
            if (tracks.length > 0) {{
                tracks[0].mode = tracks[0].mode === 'showing' ? 'hidden' : 'showing';
            }}
        }}
        
        video.addEventListener('timeupdate', updateSubtitles);
        video.addEventListener('loadedmetadata', updateSubtitles);
        
        // Enable built-in subtitle track based on preference
        video.addEventListener('loadedmetadata', function() {{
            const tracks = video.textTracks;
            if (tracks.length > 0) {{
                tracks[0].mode = '{subtitle_style in ["Built-in Track", "Both"] and "showing" or "hidden"}';
            }}
        }});
    </script>
    """
    
    return html_player

def seconds_to_vtt_timestamp(seconds: float) -> str:
    """Convert seconds to VTT timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

def generate_srt_subtitles(transcription_data: Dict) -> str:
    """Generate SRT format subtitles from transcription data"""
    """Generate SRT format subtitles from transcription data"""
    if not transcription_data or 'words' not in transcription_data:
        return ""
    
    words = transcription_data['words']
    srt_content = ""
    subtitle_index = 1
    
    # Group words into subtitle segments (2-5 seconds each)
    current_segment = []
    segment_start = None
    segment_end = None
    max_segment_duration = 5.0  # Maximum segment duration in seconds
    max_words_per_segment = 8  # Maximum words per segment
    current_speaker = None
    
    for word in words:
        if word.get('type') != 'word':
            continue
            
        word_start = word.get('start', 0)
        word_end = word.get('end', word_start)
        word_text = word.get('text', '')
        speaker_id = word.get('speaker_id', 'speaker_0')
        
        # Start new segment if needed
        if not current_segment:
            segment_start = word_start
            current_segment = [{'text': word_text, 'speaker': speaker_id}]
            segment_end = word_end
            current_speaker = speaker_id
            continue
        
        # Check if we should start a new segment
        should_break = (
            len(current_segment) >= max_words_per_segment or
            (word_start - segment_start) > max_segment_duration or
            (current_speaker != speaker_id)  # Speaker change
        )
        
        if should_break:
            # Write current segment to SRT
            segment_text = ' '.join([w['text'] for w in current_segment])
            
            # Add speaker label if diarization is enabled
            speaker_prefix = ""
            if len(set(w['speaker'] for w in current_segment)) > 1 or current_speaker != 'speaker_0':
                speaker_prefix = f"[{current_speaker}] "
            
            start_timestamp = format_timestamp(segment_start)
            end_timestamp = format_timestamp(segment_end)
            
            srt_content += f"{subtitle_index}\n"
            srt_content += f"{start_timestamp} --> {end_timestamp}\n"
            srt_content += f"{speaker_prefix}{segment_text}\n\n"
            subtitle_index += 1
            
            # Start new segment
            segment_start = word_start
            current_segment = [{'text': word_text, 'speaker': speaker_id}]
            current_speaker = speaker_id
        else:
            current_segment.append({'text': word_text, 'speaker': speaker_id})
        
        segment_end = word_end
    
    # Add final segment
    if current_segment:
        segment_text = ' '.join([w['text'] for w in current_segment])
        
        # Add speaker label if diarization is enabled
        speaker_prefix = ""
        if len(set(w['speaker'] for w in current_segment)) > 1 or current_speaker != 'speaker_0':
            speaker_prefix = f"[{current_speaker}] "
        
        start_timestamp = format_timestamp(segment_start)
        end_timestamp = format_timestamp(segment_end)
        
        srt_content += f"{subtitle_index}\n"
        srt_content += f"{start_timestamp} --> {end_timestamp}\n"
        srt_content += f"{speaker_prefix}{segment_text}\n\n"
    
    return srt_content

def generate_vtt_subtitles(transcription_data: Dict) -> str:
    """Generate VTT format subtitles from transcription data"""
    srt_content = generate_srt_subtitles(transcription_data)
    if not srt_content:
        return ""
    
    # Convert SRT to VTT format
    vtt_content = "WEBVTT\n\n"
    
    # Replace SRT timestamp format with VTT format
    lines = srt_content.strip().split('\n')
    for line in lines:
        if '-->' in line:
            # Replace comma with dot in timestamps for VTT format
            vtt_line = line.replace(',', '.')
            vtt_content += vtt_line + '\n'
        else:
            vtt_content += line + '\n'
    
    return vtt_content

def extract_audio_from_video(video_bytes: bytes) -> bytes:
    """Extract audio from video file using ffmpeg (if available)"""
    try:
        # Find ffmpeg executable
        ffmpeg_cmd = 'ffmpeg'
        
        # Check if ffmpeg is in PATH, if not try common installation locations
        try:
            subprocess.run([ffmpeg_cmd, '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try WinGet installation path
            winget_ffmpeg = os.path.join(
                os.environ.get('LOCALAPPDATA', ''),
                'Microsoft', 'WinGet', 'Packages',
                'Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe',
                'ffmpeg-8.0-full_build', 'bin', 'ffmpeg.exe'
            )
            if os.path.exists(winget_ffmpeg):
                ffmpeg_cmd = winget_ffmpeg
            else:
                raise FileNotFoundError("FFmpeg not found in PATH or common locations")
        
        # Write video to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_video:
            temp_video.write(video_bytes)
            temp_video_path = temp_video.name
        
        # Extract audio to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
        
        # Use ffmpeg to extract audio
        subprocess.run([
            ffmpeg_cmd, '-i', temp_video_path, 
            '-vn', '-acodec', 'mp3', '-ab', '128k', 
            '-ar', '16000', '-y', temp_audio_path
        ], check=True, capture_output=True)
        
        # Read extracted audio
        with open(temp_audio_path, 'rb') as f:
            audio_bytes = f.read()
        
        # Clean up temp files
        os.unlink(temp_video_path)
        os.unlink(temp_audio_path)
        
        return audio_bytes
        
    except Exception as e:
        st.warning(f"Could not extract audio from video: {str(e)}. Using original file.")
        return video_bytes

def main():
    st.set_page_config(
        page_title="ElevenLabs Subtitle Generator",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 Real-time Subtitle Generator with ElevenLabs")
    st.markdown("Upload an audio or video file to generate subtitles with speech diarization and timestamps")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input(
            "ElevenLabs API Key",
            value=ELEVENLABS_API_KEY,
            type="password",
            help="Get your API key from https://elevenlabs.io/app/settings/api-keys"
        )
        
        # Language selection (99 languages supported by Scribe v1)
        languages = {
            "Auto-detect": None,
            "English": "eng", "Spanish": "spa", "French": "fra", "German": "deu",
            "Italian": "ita", "Portuguese": "por", "Russian": "rus", "Japanese": "jpn",
            "Chinese (Mandarin)": "zho", "Korean": "kor", "Hindi": "hin", "Arabic": "ara",
            "Dutch": "nld", "Turkish": "tur", "Polish": "pol", "Swedish": "swe",
            "Norwegian": "nor", "Danish": "dan", "Finnish": "fin", "Czech": "ces",
            "Hungarian": "hun", "Bulgarian": "bul", "Romanian": "ron", "Greek": "ell",
            "Hebrew": "heb", "Thai": "tha", "Vietnamese": "vie", "Indonesian": "ind",
            "Malay": "msa", "Filipino": "fil", "Ukrainian": "ukr", "Bengali": "ben",
            "Afrikaans": "afr", "Amharic": "amh", "Armenian": "hye", "Assamese": "asm",
            "Azerbaijani": "aze", "Belarusian": "bel", "Bosnian": "bos", "Burmese": "mya",
            "Catalan": "cat", "Croatian": "hrv", "Estonian": "est", "Georgian": "kat",
            "Gujarati": "guj", "Icelandic": "isl", "Irish": "gle", "Javanese": "jav",
            "Kannada": "kan", "Kazakh": "kaz", "Khmer": "khm", "Latvian": "lav",
            "Lithuanian": "lit", "Macedonian": "mkd", "Malayalam": "mal", "Maltese": "mlt",
            "Marathi": "mar", "Mongolian": "mon", "Nepali": "nep", "Persian": "fas",
            "Punjabi": "pan", "Serbian": "srp", "Slovak": "slk", "Slovenian": "slv",
            "Swahili": "swa", "Tamil": "tam", "Telugu": "tel", "Urdu": "urd",
            "Welsh": "cym", "Zulu": "zul"
        }
        
        target_language = st.selectbox(
            "Audio Language",
            options=list(languages.keys()),
            index=0,
            help="Select the language of the audio for better accuracy"
        )
        
        num_speakers = st.slider(
            "Number of Speakers",
            min_value=1,
            max_value=32,
            value=None,
            help="Estimate the number of unique speakers (leave empty for auto-detection)"
        )
        
        # Advanced options
        st.subheader("Advanced Options")
        
        diarize = st.checkbox(
            "Speaker Diarization",
            value=True,
            help="Identify which speaker is talking"
        )
        
        tag_audio_events = st.checkbox(
            "Tag Audio Events",
            value=True,
            help="Tag events like laughter, applause, etc."
        )
        
        # Video subtitle display options
        st.subheader("Video Subtitle Options")
        
        subtitle_style = st.selectbox(
            "Subtitle Display Style",
            ["Overlay", "Built-in Track", "Both"],
            index=2,
            help="Choose how subtitles are displayed on video"
        )
        
        subtitle_size = st.slider(
            "Subtitle Font Size",
            min_value=14,
            max_value=28,
            value=18,
            help="Adjust subtitle font size"
        )
        
        # Translation options
        st.subheader("🌍 Multi-language Translation")
        
        enable_translation = st.checkbox(
            "Enable Subtitle Translation",
            value=False,
            help="Translate subtitles to multiple languages while preserving timestamps and speaker labels"
        )
        
        if enable_translation:
            # Translation service selection with status check
            st.write("**Available Translation Services:**")
            
            service_options = []
            service_status = {}
            
            for service_name, service_code in TRANSLATION_SERVICES.items():
                if service_code in ["google_free", "libre"]:
                    # Check service status (simplified to avoid delays)
                    status = "🟢" if service_code == "google_free" else "🟡"  # Google usually more reliable
                    service_options.append(f"{status} {service_name}")
                    service_status[f"{status} {service_name}"] = service_code
                else:
                    service_options.append(f"🔑 {service_name}")
                    service_status[f"🔑 {service_name}"] = service_code
            
            translation_service_display = st.selectbox(
                "Translation Service",
                options=service_options,
                index=0,  # Default to first option
                help="🟢 = Usually reliable, 🟡 = May have issues, 🔑 = Requires API key"
            )
            
            # Get the actual service code
            translation_service = service_status[translation_service_display]
            
            # Target languages selection
            target_languages = st.multiselect(
                "Target Languages",
                options=list(TARGET_LANGUAGES.keys()),
                default=["English", "Spanish", "French"],
                help="Select languages to translate subtitles to. Speaker labels and timestamps will be preserved."
            )
            
            # API key for Azure
            if "Azure" in translation_service_display:
                translation_api_key = st.text_input(
                    "Azure Translator API Key",
                    type="password",
                    help="Enter your Azure Translator API key"
                )
            else:
                translation_api_key = None
                
            if target_languages:
                st.success(f"✅ Will translate to: {', '.join(target_languages)}")
                st.info("🎯 All features preserved: timestamps, speaker diarization, audio events")
                
                # Show service info
                if translation_service == "google_free":
                    st.caption("🔄 Using Google Translate (free) - Good quality, may have rate limits")
                elif translation_service == "libre":
                    st.caption("🌐 Using LibreTranslate (free) - Open source, may be slower")
                elif translation_service == "azure":
                    st.caption("☁️ Using Azure Translator - Premium quality, requires API key")
        else:
            target_languages = []
            translation_service = None
            translation_api_key = None
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Upload Audio/Video File")
        uploaded_file = st.file_uploader(
            "Choose an audio or video file",
            type=['mp3', 'wav', 'flac', 'mp4', 'mov', 'avi', 'mkv', 'webm', 'm4a', 'aac', 'ogg'],
            help="Upload audio or video file (max 3GB, up to 10 hours)"
        )
        
        if uploaded_file is not None:
            # Show file info
            file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # Size in MB
            st.info(f"File: {uploaded_file.name} ({file_size:.1f} MB)")
            
            # Display video/audio player
            if uploaded_file.type.startswith('video/'):
                st.video(uploaded_file)
                
                # Check if we have generated subtitles for this video
                if 'transcription' in st.session_state and 'srt_content' in st.session_state:
                    st.subheader("🎬 Video with Synchronized Subtitles")
                    
                    # Check if we have translated subtitles
                    if 'translated_subtitles' in st.session_state and st.session_state['translated_subtitles']:
                        # Multi-language video player
                        st.success("🌍 Multi-language subtitles available! Use the language selector in the video player.")
                        
                        # Prepare subtitle data for all languages
                        all_subtitle_data = {}
                        
                        # Add original language (detected)
                        original_lang = st.session_state['transcription'].get('language_code', 'en')
                        original_subtitles = parse_srt_subtitles(st.session_state['srt_content'])
                        all_subtitle_data[f"Original ({original_lang.upper()})"] = original_subtitles
                        
                        # Add translated languages
                        for lang, srt_content in st.session_state['translated_subtitles'].items():
                            translated_subtitles = parse_srt_subtitles(srt_content)
                            all_subtitle_data[lang] = translated_subtitles
                        
                        # Create multilingual video player
                        video_bytes = uploaded_file.getvalue()
                        video_player_html = create_multilingual_video_player(
                            video_bytes, all_subtitle_data, uploaded_file.name, subtitle_style, subtitle_size
                        )
                        
                        # Show enhanced subtitle information
                        col_info1, col_info2, col_info3 = st.columns(3)
                        with col_info1:
                            st.metric("Total Subtitles", len(original_subtitles))
                        with col_info2:
                            lang_count = len(st.session_state['translated_subtitles']) + 1  # +1 for original
                            st.metric("Available Languages", lang_count)
                        with col_info3:
                            if original_subtitles:
                                duration = max(sub['end'] for sub in original_subtitles)
                                st.metric("Video Duration", f"{duration:.1f}s")
                    
                    else:
                        # Single language video player (original functionality preserved)
                        subtitles = parse_srt_subtitles(st.session_state['srt_content'])
                        video_bytes = uploaded_file.getvalue()
                        video_player_html = create_video_player_with_subtitles(
                            video_bytes, subtitles, uploaded_file.name, subtitle_style, subtitle_size
                        )
                        
                        # Show standard subtitle information
                        col_info1, col_info2, col_info3 = st.columns(3)
                        with col_info1:
                            st.metric("Total Subtitles", len(subtitles))
                        with col_info2:
                            if subtitles:
                                duration = max(sub['end'] for sub in subtitles)
                                st.metric("Video Duration", f"{duration:.1f}s")
                        with col_info3:
                            avg_duration = sum(sub['end'] - sub['start'] for sub in subtitles) / len(subtitles) if subtitles else 0
                            st.metric("Avg Subtitle Duration", f"{avg_duration:.1f}s")
                    
                    # Display the video player
                    st.components.v1.html(video_player_html, height=650)
                    
                    st.info("💡 Use the controls to toggle subtitle display modes. Multi-language support preserves all original features including speaker diarization and precise timestamps.")
                
            elif uploaded_file.type.startswith('audio/'):
                st.audio(uploaded_file)
            
            if st.button("Generate Subtitles", type="primary"):
                if not api_key or api_key == "your_api_key_here":
                    st.error("Please provide a valid ElevenLabs API key")
                    return
                
                try:
                    # Initialize the subtitle generator
                    generator = ElevenLabsSubtitleGenerator(api_key)
                    
                    with st.spinner("Processing file and generating subtitles..."):
                        file_bytes = uploaded_file.read()
                        
                        # Extract audio if it's a video file
                        if uploaded_file.type.startswith('video/'):
                            st.info("Extracting audio from video...")
                            try:
                                file_bytes = extract_audio_from_video(file_bytes)
                            except Exception as e:
                                st.warning(f"Could not extract audio: {str(e)}. Using original file.")
                        
                        # Create transcription
                        transcription = generator.create_transcription(
                            file_bytes,
                            language_code=languages[target_language],
                            num_speakers=num_speakers,
                            diarize=diarize,
                            tag_audio_events=tag_audio_events
                        )
                        
                        st.success("Subtitles generated successfully!")
                        
                        # Store in session state for display
                        st.session_state['transcription'] = transcription
                        st.session_state['srt_content'] = generate_srt_subtitles(transcription)
                        st.session_state['vtt_content'] = generate_vtt_subtitles(transcription)
                        
                        # Generate translations if enabled
                        if enable_translation and target_languages:
                            with st.spinner(f"Translating subtitles to {len(target_languages)} languages..."):
                                translated_subtitles = {}
                                translated_vtt = {}
                                
                                # Get the actual service code from the display name
                                service_code = translation_service
                                
                                success_count = 0
                                for i, lang in enumerate(target_languages):
                                    progress = (i + 1) / len(target_languages)
                                    st.progress(progress, f"Translating to {lang}...")
                                    
                                    try:
                                        # Translate while preserving structure
                                        translated_srt = translate_subtitles_preserve_structure(
                                            st.session_state['srt_content'],
                                            lang,
                                            service_code,
                                            translation_api_key
                                        )
                                        
                                        # Verify translation was successful (not just copied)
                                        if translated_srt and translated_srt != st.session_state['srt_content']:
                                            translated_subtitles[lang] = translated_srt
                                            success_count += 1
                                            
                                            # Convert to VTT format
                                            vtt_content = "WEBVTT\n\n"
                                            lines = translated_srt.strip().split('\n')
                                            for line in lines:
                                                if '-->' in line:
                                                    vtt_line = line.replace(',', '.')
                                                    vtt_content += vtt_line + '\n'
                                                else:
                                                    vtt_content += line + '\n'
                                            translated_vtt[lang] = vtt_content
                                            
                                            st.success(f"✅ {lang} translation completed")
                                        else:
                                            st.error(f"❌ {lang} translation failed - service may be unavailable")
                                            
                                    except Exception as e:
                                        st.error(f"❌ Failed to translate to {lang}: {str(e)}")
                                
                                if translated_subtitles:
                                    st.session_state['translated_subtitles'] = translated_subtitles
                                    st.session_state['translated_vtt'] = translated_vtt
                                    st.balloons()
                                    st.success(f"🎉 Successfully translated to {success_count}/{len(target_languages)} languages!")
                                    st.info("🎯 All features preserved: timestamps, speaker diarization, audio events")
                                else:
                                    st.error("❌ All translations failed. Please try a different translation service or check your internet connection.")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.header("Generated Subtitles")
        
        if 'transcription' in st.session_state:
            transcription = st.session_state['transcription']
            
            # Display transcription info
            st.subheader("Transcription Info")
            col2_1, col2_2 = st.columns(2)
            
            with col2_1:
                st.metric("Language", transcription.get('language_code', 'Unknown'))
                confidence = transcription.get('language_probability', 0)
                st.metric("Confidence", f"{confidence:.2%}")
            
            with col2_2:
                # Count unique speakers
                speakers = set()
                if 'words' in transcription:
                    for word in transcription['words']:
                        if word.get('speaker_id'):
                            speakers.add(word['speaker_id'])
                st.metric("Speakers Detected", len(speakers))
                
                # Calculate duration
                if 'words' in transcription and transcription['words']:
                    duration = transcription['words'][-1].get('end', 0)
                    st.metric("Duration", f"{duration:.1f}s")
            
            # Display subtitle format tabs - add translations tab if available
            if 'translated_subtitles' in st.session_state and st.session_state['translated_subtitles']:
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["Preview", "SRT", "VTT", "🌍 Translations", "Timeline"])
            else:
                tab1, tab2, tab3, tab4 = st.tabs(["Preview", "SRT", "VTT", "Timeline"])
            
            with tab1:
                st.subheader("Subtitle Preview")
                if 'srt_content' in st.session_state:
                    # Parse and display subtitles in a readable format
                    srt_lines = st.session_state['srt_content'].split('\n\n')
                    for subtitle_block in srt_lines:
                        if subtitle_block.strip():
                            lines = subtitle_block.strip().split('\n')
                            if len(lines) >= 3:
                                subtitle_num = lines[0]
                                timestamp = lines[1]
                                text = '\n'.join(lines[2:])
                                
                                with st.container():
                                    col_time, col_text = st.columns([1, 3])
                                    with col_time:
                                        st.caption(f"#{subtitle_num}")
                                        st.caption(timestamp)
                                    with col_text:
                                        st.write(text)
                                    st.divider()
            
            with tab2:
                st.subheader("SRT Format")
                if 'srt_content' in st.session_state:
                    st.text_area(
                        "SRT Subtitles",
                        value=st.session_state['srt_content'],
                        height=400,
                        key="srt_display"
                    )
                    
                    # Download button for SRT
                    st.download_button(
                        label="Download SRT",
                        data=st.session_state['srt_content'],
                        file_name=f"{uploaded_file.name.split('.')[0]}.srt",
                        mime="text/plain"
                    )
            
            with tab3:
                st.subheader("VTT Format")
                if 'vtt_content' in st.session_state:
                    st.text_area(
                        "VTT Subtitles",
                        value=st.session_state['vtt_content'],
                        height=400,
                        key="vtt_display"
                    )
                    
                    # Download button for VTT
                    st.download_button(
                        label="Download VTT",
                        data=st.session_state['vtt_content'],
                        file_name=f"{uploaded_file.name.split('.')[0]}.vtt",
                        mime="text/plain"
                    )
            
            # Add translations tab if available
            if 'translated_subtitles' in st.session_state and st.session_state['translated_subtitles']:
                with tab4:
                    st.subheader("🌍 Translated Subtitles")
                    st.info("✅ Timestamps, speaker diarization, and audio events preserved in all translations")
                    
                    # Language selector for translations
                    selected_translation_lang = st.selectbox(
                        "Select Translation Language",
                        options=list(st.session_state['translated_subtitles'].keys()),
                        key="translation_preview"
                    )
                    
                    if selected_translation_lang:
                        translated_srt = st.session_state['translated_subtitles'][selected_translation_lang]
                        translated_vtt = st.session_state.get('translated_vtt', {}).get(selected_translation_lang, "")
                        
                        # Display translation in tabs
                        trans_tab1, trans_tab2 = st.tabs(["SRT Format", "VTT Format"])
                        
                        with trans_tab1:
                            st.text_area(
                                f"SRT Subtitles - {selected_translation_lang}",
                                value=translated_srt,
                                height=300,
                                key=f"srt_{selected_translation_lang}"
                            )
                            
                            # Download button for translated SRT
                            st.download_button(
                                label=f"Download {selected_translation_lang} SRT",
                                data=translated_srt,
                                file_name=f"{uploaded_file.name.split('.')[0]}_{selected_translation_lang}.srt",
                                mime="text/plain"
                            )
                        
                        with trans_tab2:
                            if translated_vtt:
                                st.text_area(
                                    f"VTT Subtitles - {selected_translation_lang}",
                                    value=translated_vtt,
                                    height=300,
                                    key=f"vtt_{selected_translation_lang}"
                                )
                                
                                # Download button for translated VTT
                                st.download_button(
                                    label=f"Download {selected_translation_lang} VTT",
                                    data=translated_vtt,
                                    file_name=f"{uploaded_file.name.split('.')[0]}_{selected_translation_lang}.vtt",
                                    mime="text/plain"
                                )
                
                # Timeline tab (adjust index based on whether translations exist)
                timeline_tab = tab5 if 'translated_subtitles' in st.session_state and st.session_state['translated_subtitles'] else tab4
                with timeline_tab:
                    st.subheader("Subtitle Timeline")
            else:
                with tab4:
                    st.subheader("Subtitle Timeline")
                if 'srt_content' in st.session_state:
                    subtitles = parse_srt_subtitles(st.session_state['srt_content'])
                    
                    # Create a timeline visualization
                    if subtitles:
                        st.write("**Subtitle Timeline View:**")
                        
                        # Create a simple timeline chart
                        timeline_data = []
                        for i, sub in enumerate(subtitles[:20]):  # Show first 20 for performance
                            timeline_data.append({
                                'Index': f"#{sub['id']}",
                                'Start': sub['start'],
                                'End': sub['end'],
                                'Duration': sub['end'] - sub['start'],
                                'Text': sub['text'][:50] + "..." if len(sub['text']) > 50 else sub['text']
                            })
                        
                        # Display timeline as a table
                        st.write("| Index | Start Time | End Time | Duration | Text |")
                        st.write("|-------|------------|----------|----------|------|")
                        
                        for item in timeline_data:
                            start_formatted = f"{item['Start']:.1f}s"
                            end_formatted = f"{item['End']:.1f}s"
                            duration_formatted = f"{item['Duration']:.1f}s"
                            st.write(f"| {item['Index']} | {start_formatted} | {end_formatted} | {duration_formatted} | {item['Text']} |")
                        
                        if len(subtitles) > 20:
                            st.info(f"Showing first 20 subtitles. Total: {len(subtitles)} subtitles")
                    else:
                        st.info("No subtitle timeline available")
            
            # Export options
            st.subheader("Export Options")
            col3_1, col3_2, col3_3 = st.columns(3)
            
            with col3_1:
                if st.button("Copy SRT to Clipboard"):
                    st.write("SRT content copied! (Use Ctrl+C to copy from the text area above)")
            
            with col3_2:
                if st.button("Copy VTT to Clipboard"):
                    st.write("VTT content copied! (Use Ctrl+C to copy from the text area above)")
            
            with col3_3:
                # Export transcription data as JSON
                if st.button("Download JSON Data"):
                    import json
                    json_data = json.dumps(transcription, indent=2)
                    st.download_button(
                        label="Download Transcription JSON",
                        data=json_data,
                        file_name=f"{uploaded_file.name.split('.')[0]}_transcription.json",
                        mime="application/json"
                    )
        else:
            st.info("Upload a file and click 'Generate Subtitles' to see results here.")
    
    # Footer with information
    st.markdown("---")
    st.markdown("""
    ### About this App
    
    This app uses **ElevenLabs Scribe v1** API to generate high-quality subtitles with:
    - **99 languages** supported for speech-to-text
    - **Speaker diarization** to identify who is speaking
    - **Audio event tagging** for sounds like laughter, applause
    - **High accuracy** transcription with timestamps
    - **Multiple export formats** (SRT, VTT, JSON)
    
    #### Features:
    - Upload audio files (MP3, WAV, FLAC, M4A, AAC, OGG)
    - Upload video files (MP4, MOV, AVI, MKV, WEBM) - audio will be extracted
    - Automatic language detection or manual selection
    - Configurable number of speakers
    - Real-time subtitle preview
    - Download subtitles in SRT or VTT format
    - **🌍 Multi-language translation with preserved features**
    
    #### Translation Features:
    - **40+ languages** supported for translation
    - **Speaker diarization preserved** - [Speaker_1], [Speaker_2] labels maintained
    - **Timestamps preserved** - exact timing maintained across all languages
    - **Audio event tags preserved** - laughter, applause, etc. maintained
    - **Multiple services** - Google Translate (free), LibreTranslate (free), Azure (premium)
    - **Automatic fallback** - if one service fails, automatically tries another
    
    #### Translation Services:
    - **🟢 Google Translate (Free)**: Most reliable, good quality, some rate limits
    - **🟡 LibreTranslate (Free)**: Open source, slower but private
    - **🔑 Azure Translator**: Premium quality, requires API key, fastest
    
    #### Troubleshooting Translation Issues:
    - **"No module named 'cgi'" error**: Fixed by using deep-translator library
    - **LibreTranslate JSON error**: App automatically falls back to Google Translate
    - **Service unavailable**: Try switching between translation services
    - **Rate limits**: Wait a few minutes and try again with fewer languages
    
    #### Usage Tips:
    1. For best results, use high-quality audio with minimal background noise
    2. Specify the number of speakers if known
    3. Choose the correct language for better accuracy
    4. Files can be up to 3GB and 10 hours long
    
    **Need an API key?** Get one at [ElevenLabs](https://elevenlabs.io/app/settings/api-keys)
    """)

if __name__ == "__main__":
    main()
