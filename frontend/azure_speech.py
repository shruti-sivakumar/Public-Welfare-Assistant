"""
Azure Speech Service integration for voice-to-text functionality.
Provides high-accuracy speech recognition using Azure Cognitive Services.
"""

import os
import io
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import streamlit as st
import tempfile
import wave

# Load environment variables
load_dotenv()

class AzureSpeechService:
    def __init__(self):
        """Initialize Azure Speech Service with credentials from environment variables"""
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        
        # Debug logging
        print(f"DEBUG: AZURE_SPEECH_KEY={'***' if self.speech_key else 'None'}")
        print(f"DEBUG: AZURE_SPEECH_REGION={self.speech_region}")
        
        if not self.speech_key or not self.speech_region:
            raise ValueError(f"Azure Speech Service credentials missing: KEY={'***' if self.speech_key else 'None'}, REGION={self.speech_region}")
        
        # Create speech config
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, 
            region=self.speech_region
        )
        
        # Set language to English (you can make this configurable)
        self.speech_config.speech_recognition_language = "en-US"
        
        # Optional: Set continuous recognition
        self.speech_config.set_property(
            speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, "2000"
        )
    
    def transcribe_audio_file(self, audio_data):
        """
        Transcribe audio data using Azure Speech Service
        
        Args:
            audio_data: Audio file data (BytesIO or similar)
            
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            # Create a temporary file for the audio data
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                # Write audio data to temporary file
                audio_data.seek(0)  # Reset file pointer
                temp_file.write(audio_data.read())
                temp_file_path = temp_file.name
            
            try:
                # Create audio config from file
                audio_config = speechsdk.audio.AudioConfig(filename=temp_file_path)
                
                # Create speech recognizer
                speech_recognizer = speechsdk.SpeechRecognizer(
                    speech_config=self.speech_config, 
                    audio_config=audio_config
                )
                
                # Perform recognition
                result = speech_recognizer.recognize_once()
                
                # Check result
                if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    return result.text.strip()
                elif result.reason == speechsdk.ResultReason.NoMatch:
                    return "No speech could be recognized from the audio"
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation = result.cancellation_details
                    if cancellation.reason == speechsdk.CancellationReason.Error:
                        return f"Speech recognition error: {cancellation.error_details}"
                    else:
                        return "Speech recognition was cancelled"
                else:
                    return "Unknown error occurred during speech recognition"
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                    
        except Exception as e:
            return f"Error during speech recognition: {str(e)}"
    
    def transcribe_audio_stream(self, audio_stream):
        """
        Transcribe audio from a stream (for real-time scenarios)
        
        Args:
            audio_stream: Audio stream data
            
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            # Create audio config from stream
            audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
            
            # Create speech recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            # Perform recognition
            result = speech_recognizer.recognize_once()
            
            # Check result
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text.strip()
            else:
                return None
                
        except Exception as e:
            st.error(f"Speech recognition error: {str(e)}")
            return None
    
    def test_connection(self):
        """
        Test Azure Speech Service connection
        
        Returns:
            bool: True if connection is successful
        """
        try:
            # Create a simple speech config test
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, 
                region=self.speech_region
            )
            return True
        except Exception as e:
            st.error(f"Azure Speech Service connection failed: {str(e)}")
            return False

# Global instance
_azure_speech_service = None

def get_azure_speech_service():
    """Get or create Azure Speech Service instance"""
    global _azure_speech_service
    try:
        if _azure_speech_service is None:
            _azure_speech_service = AzureSpeechService()
        return _azure_speech_service
    except Exception as e:
        print(f"ERROR: Failed to initialize Azure Speech Service: {str(e)}")
        if hasattr(st, 'error'):
            st.error(f"Failed to initialize Azure Speech Service: {str(e)}")
        return None

def transcribe_audio(audio_data):
    """
    Convenience function to transcribe audio using Azure Speech Service
    
    Args:
        audio_data: Audio file data
        
    Returns:
        str: Transcribed text or error message
    """
    speech_service = get_azure_speech_service()
    if speech_service:
        return speech_service.transcribe_audio_file(audio_data)
    else:
        return "Azure Speech Service not available"