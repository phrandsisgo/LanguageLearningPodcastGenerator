# LanguageLearningPodcastGenerator

Welcome to **LanguageLearningPodcastGenerator** – a project designed to help you create custom language learning podcasts using modern AI tools.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Installation

To set up this project, follow these steps:

1. Clone the repository:
git clone https://github.com/phrandsisgo/LanguageLearningPodcast.git

2. Install  reuired packages:

```bash
pip install -r requirements.txt
```	
3. Run the app:
more to follow here on this step

4. Create a keys.py file in the root directory and add the following keys:
```python
gemini_key= "YOUR-API-KEY"
openai_key = "YOUR-API-KEY"
openai_organization_id = "YOUR-API-KEY"
openai_project_id = "YOUR-API-KEY"
anthropic_key = "YOUR-API-KEY"
finetune_model_name = "YOUR-API-KEY"
```

## Usage

After installation, you can start creating your scripts as a JSON document by using
```bash	
python podcastGenerater.py
```
And answer the questions that follow.
after successfully creating your script, you can now generate your podcast by running
```bash
main_audio.py
```

## Project-structure

Well beeing honest the project structure is still kinda messy, but here is a brief overview of the project structure:
    
```bash
    LanguageLearningPodcast/
    ├── output/                     # Folder for Output of the scripts
    ├── Audio/                      # Folder for the generated Audio
    ├── keys.py                     # For where the API keys are stored
    ├── audio_save.py               # To return the correct audio scripts to then save it later on
    ├── claudeAiPodcast.py          # To create the API calls for Anthropic products 
    ├── example-keys.py             # Example of the keys.py file
    ├── gemini_functions.py         # To create the API calls for Gemini products
    ├── mein_audio.py               # start this to create the audio files
    ├── openAiPodcastGenerator.py   # To create the API calls for OpenAI products
    ├── podcastGenerater.py         # Start this first To create the JSON file for the podcast
    ├── requirements.txt            # Required Python packages
    ├── savedocs.py                 # To save the generated scripts
    ├── tryOuts.py                  # To test the API calls
    ├── tts.py                      # To create the API calls for Google Text to Speech
    └── README.md                   # Project documentation

```

## Contributing

Honestly, I have never worked with outdide contributors, so I am not sure how to handle this. But I am open to any suggestions.
