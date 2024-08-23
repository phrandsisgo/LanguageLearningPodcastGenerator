import requests
import json
try:
    import keys as Keys
    api_key = Keys.gemini_key
except ImportError:
    api_key = input("Please enter your gemini API key: ")

def podcastgenerator(api_key, text):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"


def get_ISO(input):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    starting_prompt = """ 
    
    """
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""I want you to just return the code of the language with 2 leters of the ISO-Code of the language that is beeing inputted standard. The first input that you need to return is now "japanisch" """
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": "JP"
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"the input is {input}"
                    }
                ]
            },
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        if response.json()["candidates"][0]["content"]["parts"][0]["text"] == "JA":
            response.json()["candidates"][0]["content"]["parts"][0]["text"] = "JP" #found out during testing that the API returns the wrong code for Japanese
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}" 
    

def differentiator(story, baseLanguage, targetLanguage):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    promptForDifferentiator = f"""
        You're an excellent for when it comes to differentiating languages from each other for a podcast.
        Make sure to give the answer with separators (---) when switching languages to separate the languages one from another.
        Always when using a Separator, you will start the sentence with the correct ISO-code of the language that you're writing in.
        Do it as it is shown in the example below.
        Be sure to always use the correct ISO-code for the language that you're writing in (always use the correct one that is provided by me).
        Only return the separated text with the correct ISO-code for the language that you're writing in.
        The text you're writing will be later separated by a regex function that will separate the text by the ISO-code.
        make sure that you always pick the correct language even if it is for only a single word.

        the first sentence that you need to differentiate is the following: the Sentence, "Я на улице!" means I'm outside. However, "на улице" can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, "на улице" has 2 meanings.
   

    """
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": promptForDifferentiator #muss noch umgeschrieben werden
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": """ ---EN the Sentence, ---RU Я на улице ---EN means I'm outside. However, ---RU на улице ---EN can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, ---RU на улице ---EN has 2 meanings."""
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": """ "Was läuft bei dir Junge?" means "what's up with you, boy?" in English if we want to be literal. But you can also translate it as: "what's up dude" it is usually used in informal settings. But literally the word "läuft" means walking and "Junge" means boy. One last time the full sentence: "Was läuft bei dir Junge?"' / targetLanguage: 'DE' / explainLanguage: 'EN'"""
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": """ ---DE Was läuft bei dir Junge? ---EN means 'What's up with you, boy?' in English if we want to be literal. But you can also translate it as: 'what's up dude' it is usually used in informal settings. But literally the word ---DE "läuft" ---EN means walking and ---DE Junge ---EN means boy. One last time the full sentence: ---DE Was läuft bei dir Junge? """
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": """ "Je suis dans la cuisine" bedeutet "Ich bin in der Küche" auf Deutsch. Das Wort "cuisine" bedeutet "Küche". noch einmal der ganzer Satz zur Wiederholung:  "Je suis dans la cuisine" ' / targetLanguage: 'FR' / explainLanguage: 'DE'"""
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": """ ---FR Je suis dans la cuisine ---DE bedeutet 'Ich bin in der Küche' auf Deutsch. Das Wort ---FR "cuisine" ---DE bedeutet 'Küche'. noch einmal der ganzer Satz zur Wiederholung: ---FR "Je suis dans la cuisine" """
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""{story}" in the language of "{baseLanguage}" and "{targetLanguage}" """
                    }
                ]
            },
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
    #return differentiator["candidates"][0]["content"]["parts"][0]["text"]


def multiTurnExplainer(sentence, baseIso, targetIso, wordList, level):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    startPrompt = f"""
    Hi, you are an excellent teacher for foreign languages and are an expert to distinguish the languages from each other, for a podcast.
    Your explanations should be written in the desired explain language only. 
    You will be given a sentence from a story that is written in the target language that the user is currently learning.
    Your job is to explain the sentence in the explainin language in a way that it sutes the user quite good and he can learn it.
    Do it in a way, so that the user has to guess a word that might be challenging for someone at his level, do it in a way to describe the word without instantly translating it, But don't do it if the sentence is super easy in his level.

   And to give you a step by step guide on how to do it. here's a step by step guide:
    1. Start with the sentence that you are given. and read it in the language of the target language.
    2. if the sentence is super easy for the targeted level of the learner, then you can just explain the sentence in the language of the explain language and also add a simple translation.
    3. If the sentence is a bit more challenging, then you should explain the sentence in the language of the explain language and give also some examples on where the sentence might be used in other circumstances.
    4. If the sentence contains a word from the wordlist, also give some examples on how the word could be used in other sentences.
    5. End it with a simple translation of the sentence in the language of the explain language. followed by saying "next sentence" in the explain language. (so it can be used in a Loop for a podcast)

    So for your first sentence, I want you to explain the following sentence: "Je coupe les légumes pour la soupe" from the target language "FR" explained in the "DE" language. for the Level A2 and the wordlist is the following "[
    "Ingrédients (Zutaten)",
    "Recette (Rezept)",
    "Cuisiner (kochen)",
    "Éplucher (schälen)",
    "Couper (schneiden)",
    "Mélanger (mischen)",
    "Bouillir (sieden, kochen)",
    
    
    """
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": startPrompt
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": """Je coupe les légumes pour la soupe. Bei Ihnen das Wort "coupe" vorkommt konzentrieren wir uns zuerst darauf.
                         das Wort "coupe" kann auch in Sätzen wie "tu coupes une pomme" also "du schneidest ein Apfel  oder "il coupe le pain" was so viel bedeutet wie "er schneidet das Brot" verwendet werden.
                         Also in deinem Satz wäre "Ich und dann etwas das Gemüse für die Suppe".  
                         Wie du es vielleicht schon erraten hast, bedeutet "coupe" schneiden.
                        Also zusammengefasst bedeutet der Satz "Ich schneide das Gemüse für die Suppe" 
                         """
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""As a next sentence I want you to explain the following sentence: "{sentence}" from the target language {targetIso} explained in the {baseIso} language
                        and this is the wordlist that the user is currently learning: "{wordList}" and the level that the user is learning is {level}"""
                    }
                ]
            },
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}" 
    

def generateTitle(story, language):
    startPrompt = f"""
    Hi, you are an excellent title writer for a podcast.
    Your job is to generate a title for a language learning podcast.
    That title should be in the {language} language and should be a title to the following story:
    "{story}".
    """
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": startPrompt}]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print(f"Title of the story is: {response.json()['candidates'][0]['content']['parts'][0]['text']}")
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
    



def singleTurnExplainer(sentence, baseIso, targetIso, wordlist, level, fullStory):
    startPrompt = f"""
            As an expert language teacher for a podcast, explain the following sentence from a {targetIso} story to a {level} level learner of {targetIso}. The explanation should be in {baseIso}.

            for context here's the full story for context: {fullStory}

            Current sentence to explain: "{sentence}"

            Guidelines:
            1. Start with a smooth transition (e.g., "Let's move on to the next part." or "Now, we encounter an interesting phrase.")
            2. Explain the sentence, focusing on its meaning and any challenging words or structures.
            3. If the sentence contains words from this list: {wordlist}, provide extra explanation and examples.
            4. Include cultural notes or usage tips if relevant.
            5. Aim for a concise yet informative explanation (maximum 7 sentences please don't go over that threshhold).
            6. End with a brief summary or a question to engage the listener.
            7. Also try your best to not give any helps on how the words are supposed to sound like phonetically.
            8. Super important is that you only use the languages {baseIso} and {targetIso} in the explanation and nothing else.
            9. At least once the sentence should come fully translated in the language of {baseIso}.

            Remember, your explanation should flow naturally as part of a podcast, maintaining listener engagement between sentences.
            """
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": startPrompt}]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"
