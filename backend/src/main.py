from utils.gemini_chat import GeminiChat, OutputParserTypes
from utils.stt import speech_to_text
from configs.database import Database
from playsound import playsound
from dotenv import dotenv_values
from utils.database import create_all
import os

def main():
    sleeping = True
    env = dotenv_values("../.env")
    gemini_chat = GeminiChat(env.get('GOOGLE_GENERATIVE_LANGUAGE_API_KEY'))
    db = Database(env.get('DATABASE_URL'))
    db.connect()
    create_all(db)


    # try:
    #     gemini_chat.set_parser(OutputParserTypes.STRING)
    #     reposne = gemini_chat.invoke("hello, how are you?")
    #     print(reposne)
    # except Exception as e:
    #     print(e)

    # while True:
    #     print("Listening ...")
    #     # is_sleeping, text, ai_talk_first = speech_to_text(sleeping)
    #     google_tts = GoogleTTS(env.get('GOOGLE_APPLICATION_CREDENTIALS'))
    #     google_tts.list_voices()
        


if __name__ == '__main__':
    main()