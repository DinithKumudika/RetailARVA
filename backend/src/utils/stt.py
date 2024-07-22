import speech_recognition as sr

def speech_to_text(is_sleep):
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold=False
    rec.energy_threshold = 400
    ai_talk = False    

    with mic as source1:
        rec.adjust_for_ambient_noise(source1, duration= 0.5)
            
        try: 
            audio = rec.listen(source1, timeout = 10, phrase_time_limit = 15)
            text = rec.recognize_google(audio)
                
            # AI is in sleeping mode
            if is_sleep == True:
                if "hello gemini" in text.lower():
                    request = text.lower().split("hello gemini")[1]
                    is_sleep = False                       
                        
                    # if the user's question is none or too short, skip 
                    if len(request) < 5:
                        ai_talk = True
            # AI is awake         
            else: 
                request = text.lower()
                if "that's all" in request:
                    is_sleep = True
                if "hello gemini" in request:
                    request = request.split("hello gemini")[1]
            return is_sleep, request, ai_talk 
        except Exception as e:
            print(e)