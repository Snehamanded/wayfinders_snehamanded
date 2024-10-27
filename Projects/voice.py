import speech_recognition as sr

def recognize_speech():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Optional: adjusts for noise
        print("Listening for a command...")
        audio = recognizer.listen(source)  # Listen to input from the microphone

    try:
        # Recognize the speech using Google Web Speech API
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    
    return ""

# Main program
if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if command:
            print(f"Received Command: {command}")
        if command.lower() == "stop":
            break
