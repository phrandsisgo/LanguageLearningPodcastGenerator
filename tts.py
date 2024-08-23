from google.cloud import texttospeech
import os
import sys
import requests
import re
documentation = "https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#client-libraries-install-python"
# Replace 'your_api_key.json' with the path to your API key
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = texttospeech.TextToSpeechClient.from_service_account_json('linguatech-tts.json') 

try:
    import keys as Keys
    api_key = Keys.openai_key
    organization_id = Keys.openai_organization_id
    project_id = Keys.openai_project_id
except ImportError:
    api_key = input("Please enter your OpenAI API key: ")
    organization_id = input("Please enter your OpenAI organization ID: ")
    project_id = input("Please enter your OpenAI project ID: ")

def tts_decisioner(language, text, speed=1, path_name= None):
    print("\033[92m" + text + "\033[0m")
    ssml_text =f"<speak>{text}</speak>"
    if language == "EN":
        return synthesize_text_EN(ssml_text, speed, path_name)
    elif language == "DE":
        return synthesize_text_DE(ssml_text, speed, path_name)
    elif language == "ES":
        return synthesize_text_ES(ssml_text, speed, path_name)
    elif language == "RU":
        return synthesize_text_RU(ssml_text, speed, path_name)
    elif language == "FR":
        return synthesize_text_FR(ssml_text, speed, path_name)
    elif language == "PT":
        return synthesize_text_PT(ssml_text, speed, path_name)
    elif language == "HU":
        return syntehtize_text_HU(ssml_text, speed, path_name)
    elif language == "NL":
        return syntehtize_text_NL(ssml_text, speed, path_name)
    else:
        return openai_tts(text, path_name, speed)

def openai_tts(text, output_file="output.mp3", speed=1):
    # Setze die notwendigen Header
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Organization": organization_id,
        "OpenAI-Project": project_id,
        "Content-Type": "application/json"
    }

    # Setze die Daten für die Anfrage
    data = {
        "model": "tts-1",
        "voice": "nova",
        "input": text,
        "speed": speed
    }

    # Sende die Anfrage
    response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data)

    # Überprüfe die Antwort
    if response.status_code == 200:
        with open(f"{output_file}.mp3", "wb") as f:
            f.write(response.content)
        print("Text-to-Speech conversion completed. File saved as '{output_file}.mp3'.")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

def synthesize_text_RU(text, speed=0.9, path_name= None):
    synthesis_input = texttospeech.SynthesisInput(ssml=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ru-RU",  # Russian
        name="ru-RU-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-1.0,
    )

    # Send the request and get the response
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Get the current directory
    current_dir = os.getcwd()

    if path_name is None:
        # If no path_name is given, we generate a new file name
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)
        existing_files = len(os.listdir(audio_dir))
        output_file = os.path.join(audio_dir, f"{existing_files + 1}Test.mp3")
    else:
        output_file = f"{path_name}.mp3"

    # Ensure that the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the response (as an MP3 file)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")

    return output_file

def synthesize_text_ES(text, speed=0.9, path_name= None):
    # Text, der in Sprache umgewandelt werden soll
    # text = "Hallo,<break time='1.5s'/> wie geht es dir heute?"

    # Konfiguration der Anfrage
    synthesis_input = texttospeech.SynthesisInput(ssml=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-ES",  # British English
        name="es-ES-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-5.6
    )

    # Anfrage senden und Antwort erhalten
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Get the current directory
    current_dir = os.getcwd()

    if path_name is None:
        # If no path_name is given, we generate a new file name
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)
        existing_files = len(os.listdir(audio_dir))
        output_file = os.path.join(audio_dir, f"{existing_files + 1}Test.mp3")
    else:
        output_file = f"{path_name}.mp3"

    # Ensure that the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the answer (as MP3-File)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")

    return output_file

def synthesize_text_EN(inputText, speed=1, path_name= None):

    # Konfiguration der Anfrage
    synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",  # British English
        name="en-GB-Wavenet-B",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-5.6
    )

    # Anfrage senden und Antwort erhalten
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
        # Get the current directory
    current_dir = os.getcwd()

    if path_name is None:
        # If no path_name is given, we generate a new file name
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)
        existing_files = len(os.listdir(audio_dir))
        output_file = os.path.join(audio_dir, f"{existing_files + 1}Test.mp3")
    else:
        output_file = f"{path_name}.mp3"

    # Ensure that the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Save the answer (as MP3-File)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")
    return output_file

def synthesize_text_DE(inputText, speed=1, path_name= None):
        synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
        voice = texttospeech.VoiceSelectionParams(
            language_code="de-DE",  # German
            name="de-DE-Polyglot-1",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            pitch=-0.50
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Get the current directory
        current_dir = os.getcwd()

        if path_name is None:
            # If no path_name is given, we generate a new file name
            audio_dir = os.path.join(current_dir, "Audio")
            os.makedirs(audio_dir, exist_ok=True)
            existing_files = len(os.listdir(audio_dir))
            output_file = os.path.join(audio_dir, f"{existing_files + 1}Test.mp3")
        else:
            output_file = f"{path_name}.mp3"
    
        # Ensure that the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        # Save the answer (as MP3-File)
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            print("audio written to 'output_file'.")
        return output_file

def synthesize_text_FR(inputText, speed=1, path_name= None):
    synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",  # French
        name="fr-FR-Polyglot-1",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-0.50
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Get the current directory
    current_dir = os.getcwd()

    if path_name is None:
        # If no path_name is given, we generate a new file name
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)
        existing_files = len(os.listdir(audio_dir))
        output_file = os.path.join(audio_dir, f"{existing_files + 1}Test.mp3")
    else:
        output_file = f"{path_name}.mp3"

    # Ensure that the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Save the answer (as MP3-File)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("audio written to 'output_file'.")
    return output_file

def synthesize_text_PT(inputText, speed=1, path_name= None):
    synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",  # Portuguese
        name="pt-BR-Wavenet-D",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-2.80
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Get the current directory
    current_dir = os.getcwd()

    if path_name is None:
        # If no path_name is given, we generate a new file name
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)
        existing_files = len(os.listdir(audio_dir))
        output_file = os.path.join(audio_dir, f"{existing_files + 1}Test.mp3")
    else:
        output_file = f"{path_name}.mp3"

    # Ensure that the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Save the answer (as MP3-File)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("audio written to 'output_file'.")
    return output_file

def syntehtize_text_HU(inputText, speed=1, path_name= None):
    synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
    voice = texttospeech.VoiceSelectionParams(
        language_code="hu-HU",  # Hungarian
        name="hu-HU-Wavenet-A",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-1.0
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Get the current directory
    current_dir = os.getcwd()

    if path_name is None:
        # If no path_name is given, we generate a new file name
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)
        existing_files = len(os.listdir(audio_dir))
        output_file = os.path.join(audio_dir, f"{existing_files + 1}Test.mp3")
    else:
        output_file = f"{path_name}.mp3"

    # Ensure that the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Save the answer (as MP3-File)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("audio written to 'output_file'.")
    return output_file

def syntehtize_text_NL(inputText, speed=1, path_name= None):
    synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
    voice = texttospeech.VoiceSelectionParams(
        language_code="nl-NL",  # Dutch
        name="nl-NL-Wavenet-A",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-4.0
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Get the current directory
    current_dir = os.getcwd()

    if path_name is None:
        # If no path_name is given, we generate a new file name
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)
        existing_files = len(os.listdir(audio_dir))
        output_file = os.path.join(audio_dir, f"{existing_files + 1}Test.mp3")
    else:
        output_file = f"{path_name}.mp3"

    # Ensure that the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Save the answer (as MP3-File)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("audio written to 'output_file'.")
    return output_file
# languages available so far: EN, DE, ES, RU , FR, PT
#synthesize_text_PT("<speak>Quando tem feijoada na casa de Maria, ela convida alguns amigos para almoçar junto com ela.</speak>", 0.8, "hallo pt") # Test