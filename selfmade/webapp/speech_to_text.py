import azure.cognitiveservices.speech as speechsdk
import os

speech_key=os.getenv("AZURE_SPEECH")
service_region=os.getenv("AZURE_SPEECH_REGION")

def save_text_to_audio(text, filename="response_audio.wav"):
    """performs speech synthesis to the default speaker with auto language detection
       Note: this is a preview feature, which might be updated in future versions."""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # create the auto detection language configuration without specific languages
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig()

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, auto_detect_source_language_config=auto_detect_source_language_config,audio_config=None)
    # speech_config.speech_synthesis_voice_speed = 5  # Pas deze waarde aan om de snelheid aan te passen
    result = speech_synthesizer.speak_text_async(text).get()
    
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        stream = speechsdk.AudioDataStream(result)
        stream.save_to_wav_file(filename)
