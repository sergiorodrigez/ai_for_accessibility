import os
import azure.cognitiveservices.speech as speechsdk

class AzureConnection:
    @staticmethod
    def text_to_speech(text):
        speech_key = "28953521c5604f22909c512ddf41d2f3" 
        service_region = "centralus"  
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        else:
            print(f'Text-to-speech conversion failed: {result.reason}')
            return None

