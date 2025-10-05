import os
import requests
import streamlit as st
import tempfile
from typing import Dict, List
from datetime import timedelta
import subprocess
import base64

# ElevenLabs API Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your_api_key_here")
BASE_URL = "https://api.elevenlabs.io"

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
                    
                    # Parse subtitles for the video player
                    subtitles = parse_srt_subtitles(st.session_state['srt_content'])
                    
                    # Create video player with subtitle overlay
                    video_bytes = uploaded_file.getvalue()
                    video_player_html = create_video_player_with_subtitles(
                        video_bytes, subtitles, uploaded_file.name, subtitle_style, subtitle_size
                    )
                    
                    # Display the custom video player
                    st.components.v1.html(video_player_html, height=600)
                    
                    # Show subtitle information
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
                    
                    st.info("💡 Use the controls below the video to toggle subtitle display modes. You can switch between overlay subtitles and built-in browser subtitles.")
                
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
            
            # Display subtitle format tabs
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
    
    #### Usage Tips:
    1. For best results, use high-quality audio with minimal background noise
    2. Specify the number of speakers if known
    3. Choose the correct language for better accuracy
    4. Files can be up to 3GB and 10 hours long
    
    **Need an API key?** Get one at [ElevenLabs](https://elevenlabs.io/app/settings/api-keys)
    """)

if __name__ == "__main__":
    main()
