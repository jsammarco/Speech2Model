import speech_recognition as sr

def live_transcription():
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        sr.pause_threshold = 5
        sr.energy_threshold = 3000
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=4)
        print("Ready to transcribe. Speak now!")

        try:
            # Continuously listen and transcribe
            while True:
                print("Listening...")
                audio = recognizer.listen(source)

                try:
                    # Convert speech to text
                    transcription = recognizer.recognize_google(audio)
                    print(f"You said: {transcription}")
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand what you said. Try again.")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")

        except KeyboardInterrupt:
            print("Exiting live transcription...")

if __name__ == "__main__":
    live_transcription()
