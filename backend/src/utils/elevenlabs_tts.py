from typing import Iterator
from elevenlabs.client import ElevenLabs
from elevenlabs import play, Voice

class ElvenLabsTTS:
    def __init__(self, api_key:str) -> None:
        self.client : ElevenLabs = ElevenLabs(api_key=api_key)

    def list_voices(self) -> None:
        voices = self.client.voices.get_all()
        for voice in voices.voices:
            voice = Voice(
                voice_id=voice.voice_id,
                name= voice.name,
                labels= voice.labels
            )
            print(f"voice id: {voice.voice_id}")
            print(f"voice name: {voice.name}")
            print(f"voice labels: {voice.labels}")

    def text_to_speech(self, text:str, voice_name = 'Sarah') -> None:
        audio : Iterator[bytes] = self.client.generate(
            text=text,
            voice=voice_name,
            model="eleven_multilingual_v2"
        )
        play(audio)