from google.cloud import texttospeech_v1 as tts
from google.cloud.texttospeech_v1 import TextToSpeechClient
from google.oauth2 import service_account

class GoogleTTS:
    def __init__(self, google_applications_credentials : str) -> None:
        credentials = service_account.Credentials.from_service_account_file(google_applications_credentials)
        self.client : TextToSpeechClient = tts.TextToSpeechClient(credentials=credentials)

    def list_voices(self, language_code : str | None = None) ->  None:
        response = self.client.list_voices(language_code=language_code)
        voices = sorted(response.voices, key=lambda voice: voice.name)

        print(f" Voices: {len(voices)} ".center(60, "-"))
        for voice in voices:
            languages = ", ".join(voice.language_codes)
            name = voice.name
            gender = tts.SsmlVoiceGender(voice.ssml_gender).name
            rate = voice.natural_sample_rate_hertz
            print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

    def text_to_speech(self, text : str, voice_name : str ="en-US-Studio-O")-> str:
        language_code = "-".join(voice_name.split("-")[:2])

        print(f"text to speech using voice {voice_name}")

        try:
            synthesis_input = tts.SynthesisInput(text= f"<speak>{text}</speak>")

            voice = tts.VoiceSelectionParams(
                language_code =language_code,
                name=voice_name
            )

            audio_config = tts.AudioConfig(
                audio_encoding = tts.AudioEncoding.MP3,
                effects_profile_id = "telephony-class-application",
                speaking_rate = 1,
                pitch = 1
            )

            request = tts.SynthesizeSpeechRequest(
                input = synthesis_input,
                voice = voice,
                audio_config = audio_config
            )

            response = self.client.synthesize_speech(request=request)

            audio_file : str = "output.mp3"

            with open(audio_file, "wb") as out:
                out.write(response.audio_content)
                print(f"audio written to the {audio_file}")
            return audio_file
        except Exception as e:
            raise e