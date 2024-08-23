import os
import json
from datetime import datetime

def generate_filename(title):
    #Generates a filename based on title, date and time
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    title = ''.join(c for c in title if c.isalnum() or c.isspace())
    filename = f"{title}-{date_time}.json"
    return os.path.join('output', filename)


def generate_filepath(title):
    # Generates a filepath based on title, date, and time
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    title = ''.join(c for c in title if c.isalnum() or c.isspace())
    filename = f"{title}-{date_time}.json"
    return os.path.join('output', filename)

def ensure_output_directory():
    #Ensures that the output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')


def create_empty_file(filepath, target_language, base_language):
    # Creates an empty JSON file with initial structure
    initial_data = {
        "target_language": target_language,
        "base_language": base_language,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),  # Modified date format
        "title": "",
        "intro": "",
        "betweenpart": "",
        "story": "",
        "explanations": [],
        "wordList": ""
    }
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
        print(f"The full path is {filepath}")
    except Exception as e:
        print(f"Error creating file: {e}")

def add_title(filepath, title):
    # Adds the title to the JSON file
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['title'] = title
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

def add_intro(filepath, intro):
    # Adds the intro to the JSON file
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['intro'] = intro
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

def add_story(filepath, story):
    # Adds the story to the JSON file
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['story'] = story
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
        f.truncate()


def add_outro(filepath, outro):
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['outro'] = outro
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()


def append_explanation(filepath, sentence, explanation,raw_explanation, sentence_number):
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        explanation_entry = {
            "sentence_number": sentence_number,
            "sentence": sentence,
            "raw_explanation": raw_explanation,
            "explanation": explanation
        }
        data['explanations'].append(explanation_entry)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
        f.truncate()

def save_output(title, content, token_usage=None):
    #Saves the content and token usage in a file in the output directory with a generated filename
    ensure_output_directory()
    filename = generate_filename(title)
    full_path = os.path.join('output', f"{filename}.json")
    
    output_data = {
        "content": content
    }
    
    if token_usage is not None:
        output_data["token_usage"] = token_usage
    
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    return full_path

def load_output(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def add_betweenpart(filepath, betweenpart):
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['betweenpart'] = betweenpart
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

def add_wordList(filepath, wordList):
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['wordList'] = wordList
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

def edit_content(filepath):
    #Opens a file for editing and saves the changes
    data = load_output(filepath)
    content = data['content']
    
    print("Aktueller Inhalt:")
    for key, value in content.items():
        print(f"{key}: {value}")
    
    for key in content.keys():
        edited = input(f"Bearbeiten Sie den Inhalt von '{key}' (leer lassen für keine Änderung):\n")
        if edited:
            content[key] = edited
    
    data['content'] = content
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def analyze_output(filepath):
    #Analyzes the content of an output file and returns statistics
    data = load_output(filepath)
    content = data['content']
    token_usage = data['token_usage']
    
    stats = {
        "token_usage": token_usage,
        "content_stats": {}
    }
    
    for key, value in content.items():
        stats["content_stats"][key] = {
            'chars': len(value)
        }
    
    return stats


#this section is to try out the functions with random strings
current_filepath = ""

current_filepath = generate_filename("Test of Thomas's ")
create_empty_file(current_filepath, "English", "deutsch")
intro = "This is a test of Lisa's story generation capabilities."

story="Once upon a time, in a faraway land, there was a young prince named Diego. He was a brave and noble warrior, always ready to defend his kingdom from any threat. One day, a terrible dragon attacked the kingdom, breathing fire and destruction wherever it went. Diego knew that he was the only one who could stop the dragon and save his people. So he set out on a quest to find the dragon and defeat it once and for all. Along the way, he faced many dangers and challenges, but he never wavered in his determination. Finally, after a long and difficult journey, Diego reached the dragon's lair. With his sword in hand and his heart full of courage, he faced the dragon in a fierce battle. The dragon fought fiercely, but Diego was stronger and braver. In the end, he emerged victorious, the dragon lay defeated at his feet. The kingdom was saved, and Diego was hailed as a hero by all. And so, Diego returned to his kingdom, his head held high and his heart full of pride. He knew that no matter what challenges lay ahead, he would always be ready to face them with courage and honor."
add_story(current_filepath, story)
add_intro(current_filepath, intro)
