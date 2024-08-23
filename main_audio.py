from audio_save import *
from tts import tts_decisioner
import os
from datetime import datetime
from moviepy.editor import AudioFileClip, concatenate_audioclips
import re
json_name = get_correct_json_data()

short_file = json_name.rstrip(".json")
json_path = create_audio_folder(short_file)
def do_intro():
    if os.path.exists(os.path.join("output",json_path, "intro")):
        return
    full_path = os.path.join("output",json_path, "intro")
    tts_decisioner(get_base_language(json_name), get_intro(json_name), path_name=full_path)
    print("Intro audio file created.")
    return

def do_story():
    print("starting to create story audio file")
    if os.path.exists(os.path.join("output",json_path, "story")):
        return
    full_path = os.path.join("output",json_path, "story")
    tts_decisioner(get_target_language(json_name), get_story(json_name),speed=0.8, path_name=full_path)   
    print("Story audio file created.")
    return

def do_inbetween():
    print("Starting to create inbetween audio files")
    if os.path.exists(os.path.join("output",json_path, "inbetween")):
        return
    tts_decisioner(get_base_language(json_name), get_inbetween_part(json_name), speed=1.0, path_name=os.path.join("output",json_path, "inbetween"))
    print("Inbetween audio file created.")
    return

def do_outro():
    print("Starting to create outro audio file")
    if os.path.exists(os.path.join("output",json_path, "outro")):
        return
    tts_decisioner(get_base_language(json_name), get_outro(json_name), path_name=os.path.join("output",json_path, "outro"))
    print("Outro audio file created.")
    return

def do_explanations():
    print("Starting to create explanation audio files")
    explanations_path = os.path.join("output", json_path)
    # Check if there are files starting with "explanation" and have the extension ".mp3"
    if os.path.exists(explanations_path) and any(fname.startswith("explanation") and fname.endswith(".mp3") for fname in os.listdir(explanations_path)):
        print("Explanation files already exist.")
        return
    explanations = get_explanations(json_name)
    if explanations is None:
        print("Error: Could not retrieve explanations.")
        return

    target_language = get_target_language(json_name)
    base_language = get_base_language(json_name)

    for idx, explanation in enumerate(explanations, 1):
        explanation_text = explanation.get('explanation')

        if explanation_text is None:
            print(f"Error: Missing explanation text for item {idx}")
            continue

        # Split the explanation into parts based on language tags
        parts = re.split(r'(---\w{2})', explanation_text)
        parts = [part for part in parts if part.strip()]  # Remove empty parts

        for sub_idx, part in enumerate(parts[1:], 1):  # Start from 1 to skip the first tag
            if re.match(r'---\w{2}', part):
                continue

            language_tag = parts[sub_idx - 1]
            language = base_language if language_tag == f'---{base_language.upper()}' else target_language

            # Create audio for each part of the explanation
            explanation_path = os.path.join(explanations_path, f"explanation{idx}-{sub_idx}")
            if not os.path.exists(explanation_path + ".mp3"):
                speed = 0.8 if language == target_language else 1.0
                tts_decisioner(language, part.strip(), speed=speed, path_name=explanation_path)
                print(f"Created audio for explanation {idx}-{sub_idx} in {language} with speed {speed}")

    print("All explanation audio files created.")
    return

def merge_mp3_files(files_folder):
    # Dateinamen in der gewünschten Reihenfolge
    file_order = ["intro.mp3", "story.mp3", "inbetween.mp3"]
    
    # Alle Erklärung-Dateien in der richtigen Reihenfolge sammeln
    explanation_files = sorted(
        (f for f in os.listdir(files_folder) if f.startswith("explanation") and f.endswith(".mp3")),
        key=lambda x: tuple(map(int, re.findall(r'\d+', x)))
    )

    # Schauen, ob der Ordner existiert
    if not os.path.exists(files_folder):
        print(f"Error: The folder {files_folder} does not exist.")
        return
    
    # Schauen, ob die Output-Datei mit dem namen done-Datum.mp3 schon existiert
    if any(fname.startswith("done") and fname.endswith(".mp3") for fname in os.listdir(files_folder)):
        print("Error: The combined audio file already exists.")
        return

    # Die Reihenfolge in der Datei-Liste kombinieren
    all_files = file_order + explanation_files

    # Liste der Audio-Clips erstellen
    audio_clips = []

    for file_name in all_files:
        file_path = os.path.join(files_folder, file_name)
        if os.path.exists(file_path):
            audio_clips.append(AudioFileClip(file_path))
        else:
            print(f"Warning: {file_name} does not exist in the folder.")

    # Audio-Clips kombinieren
    if audio_clips:
        combined = concatenate_audioclips(audio_clips)

        # Zeitstempel für den Dateinamen
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_path = os.path.join(files_folder, f"done-{timestamp}.mp3")

        # Zusammengeführte Audiodatei speichern
        combined.write_audiofile(output_path)
        print(f"Combined audio saved as {output_path}")
    else:
        print("No audio files to combine.")

do_intro()
do_inbetween()
do_story()
do_explanations()
merge_mp3_files(os.path.join("output", json_path))