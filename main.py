import speech_recognition as sr  # type: ignore
import webbrowser
import pyttsx3  # type: ignore
import os
import google.generativeai as genai

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def aiProcess(command):
    """Processes a given command using the Gemini-1.5-flash model and speaks the response.

    Args:
        command (str): The command to be processed.
    """
    try:
        genai.configure(api_key=os.environ.get('GENAI_API_KEY'))
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(command)
        speak(response)
    except KeyError:
        print("API key not found. Please set the 'GENAI_API_KEY' environment variable.")
    except Exception as e:
        print(f"An error occurred while processing the AI command: {e}")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com")
    else:
        aiProcess(command)

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for the wake word 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                command = recognizer.recognize_google(audio)
                print(f"Recognized command: {command}")

                if command.lower() == "jarvis":
                    speak("Yes?")
                    print("Jarvis is active...")

                    # Listen for the next command
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    print(f"Command received: {command}")

                    processCommand(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
