import requests
import json
import openai
try:
    import keys as Keys
    api_key = Keys.openai_key
    organization_id = Keys.openai_organization_id
    project_id = Keys.openai_project_id
    finetune_model_name = Keys.finetune_model_name
except ImportError:
    api_key = input("Please enter your OpenAI API key: ")
    organization_id = input("Please enter your OpenAI organization ID: ")
    project_id = input("Please enter your OpenAI project ID: ")
    finetune_model_name = input("Please enter the name of the model you have finetuned for the language differentiator: ")


openai.api_key = api_key
headers = {
    "Authorization": f"Bearer {api_key}",
    "OpenAI-Organization": organization_id,
    "OpenAI-Project": project_id,
}

def Introwriter(fullStory, targetLanguage, baseLanguage, level, ):
    promptForIntro = f"""Hi, you are an excellent introduction writer for a Podcast.
      I want you to write me an introduction for a language learning podcast that is for language learners who are learning {targetLanguage} at the {level} level.
       The introduction should be written only in {baseLanguage} and should not include any other languages.
        You should write an introduction that is about the following story: {fullStory}.
        Now that you know the full story, keep in mind that as the last sentence, the listener will also hear this story in the language of {targetLanguage}.
        So, you should tell the listener something like "And now we're going to listen to the full story" in {baseLanguage}.
        Keep the introduction short and sweet."""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a conversation designer."},
            {"role": "user", "content": promptForIntro},
        ],
    )
    return response

def emptyPromptFunction(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", #alternative model: gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    message_content = response['choices'][0]['message']['content']
   # total_tokens = response['choices'][0]['total_tokens']
    return message_content

def empty_GPT4o_mini(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    message_content = response['choices'][0]['message']['content']
    return message_content


def lang_differentiator(sentence, baselanguage, targetlanguage):
    #started to make a second one for redundancy
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-08-06",
        temperature=0.3,
        messages=[
            {"role": "system", "content": """

             You are an expert in differentiating languages for a podcast. Your task is to separate text by language, following these rules:
            1. Use separators (---) followed by the correct ISO language code when switching languages.
            2. Only switch languages for actual words or phrases, not for punctuation or spaces.
            3. Maintain the original sentence structure and punctuation.
            4. Do not add any explanatory text; only provide the differentiated sentence. Your job is also not to help with the 
            5. If you see a single word for a explenation purpose that is in an other language like the rest is has to be differentiated as well.


            """},
            {"role": "user", "content": f""" the first sentence that you need to differentiate is the following: the Sentence, "Я на улице!" means I'm outside. However, "на улице" can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, "на улице" has 2 meanings. // Baselanguage: "EN" Targetlanguage "RU"  """ },

            {"role": "assistant", "content": f""" ---EN the first sentence that you need to differentiate is the following: the Sentence, ---RU Я на улице ---EN means I'm outside. However, ---RU на улице ---EN can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, ---RU на улице ---EN has 2 meanings. """},


            {"role": "user", "content": f""" "Was läuft bei dir Junge?" means "what's up with you, boy?" in English if we want to be literal. But you can also translate it as: "what's up dude" it is usually used in informal settings. But literally the word "läuft" means walking and "Junge" means boy. One last time the full sentence: "Was läuft bei dir Junge?"' // Baselanguage: "EN" Targetlanguage "DE"  """}, 

            {"role": "assistant", "content": f""" ---DE "Was läuft bei dir Junge?" ---EN means 'What's up with you, boy?' in English if we want to be literal. But you can also translate it as: 'what's up dude' it is usually used in informal settings. But literally the word ---DE "läuft" ---EN means walking and ---DE Junge ---EN means boy. One last time the full sentence: ---DE Was läuft bei dir Junge? """},


            {"role": "user", "content": f""" "Anna kijkt naar de mensen om zich heen en denkt aan het festival. Ze denkt: \"Het Sziget Festival was een van de beste momenten van haar leven.\" \n\nEsta frase significa que o festival foi uma experiência muito especial e positiva para Anna. A palavra \"beste\" quer dizer que foi uma das melhores experiências. \"Momenten\" se refere a períodos de tempo que foram importantes ou memoráveis. Essa estrutura é usada para descrever eventos significativos na vida de alguém. \n\nUm exemplo semelhante poderia ser: \"De vakantie was een van de mooiste tijden van het jaar.\" Isso mostra que você teve uma experiência feliz. No caso de Anna, o festival ficou na memória dela como um momento especial." // Baselanguage: "PT" Targetlanguage "NL" """},
     
            {"role": "assistant", "content": f"---NL Anna kijkt naar de mensen om zich heen en denkt aan het festival. Ze denkt: \"Het Sziget Festival was een van de beste momenten van haar leven.\" \n\n---PT Esta frase significa que o festival foi uma experiência muito especial e positiva para Anna. A palavra ---NL \"beste\" ---PT quer dizer que foi uma das melhores experiências. \"Momenten\" se refere a períodos de tempo que foram importantes ou memoráveis. Essa estrutura é usada para descrever eventos significativos na vida de alguém. \n\n Um exemplo semelhante poderia ser: ---NL \"De vakantie was een van de mooiste tijden van het jaar.\" ---PT Isso mostra que você teve uma experiência feliz. No caso de Anna, o festival ficou na memória dela como um momento especial."},



            {"role": "user", "content": f""" "Emely a Lánchídnál van, és éppen csodálja a hidat, amikor azt mondja: \"\" - mondja magában. En français, cela signifie : \"elle dit dans sa tête\". Cette phrase montre qu'Emely pense quelque chose sans le dire à haute voix. Le verbe “mond” signifie “dire”, et “magában” signifie “dans sa tête”. C'est une façon de montrer ce que l'on ressent ou pense intérieurement. Par exemple, si vous voyez quelque chose de beau, vous pouvez également dire “c’est magnifique!” - magában. \n\nEn résumé, cette phrase nous permet de comprendre ce que ressent Emely sans qu'elle le dise à voix haute." // Baselanguage: "FR" Targetlanguage "HU" """},

            {"role": "assistant", "content": f"""---HU Emely a Lánchídnál van, és éppen csodálja a hidat, amikor azt mondja: \"\" - mondja magában. ---FR En français, cela signifie : \"elle dit dans sa tête\". Cette phrase montre qu'Emely pense quelque chose sans le dire à haute voix. Le verbe ---HU “mond” ---FR signifie “dire”, et ---HU “magában” ---FR signifie “dans sa tête”. C'est une façon de montrer ce que l'on ressent ou pense intérieurement. Par exemple, si vous voyez quelque chose de beau, vous pouvez également dire  “c’est magnifique!” - ---HU magában. \n\n---FR En résumé, cette phrase nous permet de comprendre ce que ressent Emely sans qu'elle le dise à voix haute."""},


            {"role": "user", "content": f"""{sentence} // Baselanguage: "{baselanguage}" Targetlanguage "{targetlanguage}" """ },

        ],
    )
    
    return response


def lang_finetune_differentiator(sentence, baselanguage, targetlanguage):
    #started to make a second one for redundancy
    response = openai.ChatCompletion.create(
        model="ft:gpt-4o-mini-2024-07-18:personal:lang-differentiator:9xA4SIG5",
        temperature=0.3,
        messages=[
            
            {"role": "system", "content": """

             You are an expert in differentiating languages for a podcast. Your task is to separate text by language, following these rules:
            1. Use separators (---) followed by the correct ISO language code when switching languages.
            2. Only switch languages for actual words or phrases, not for punctuation or spaces.
            3. Maintain the original sentence structure and punctuation.
            4. Do not add any explanatory text; only provide the differentiated sentence. Your job is also not to help with the 
            5. If you see a single word for a explenation purpose that is in an other language like the rest is has to be differentiated as well.


            """},
            {"role": "user", "content": f"""{sentence} // Baselanguage: "{baselanguage}" Targetlanguage "{targetlanguage}" """ },
        ],
    )

    return response

def sentence_explainer(sentence, baseIso, targetIso, level, fullStory, storyPrompt, wordlist=None):
    system_prompt = f"""
    As an expert language teacher for a podcast, your task is to explain sentences from a story to language learners. Follow these guidelines:

    - Start with a smooth transition from the last sentence (if not the first sentence).
    - Provide a full translation of the sentence in the base language.
    - Explain the sentence, focusing on its meaning and any challenging words or structures.
    - Use both the base and target languages throughout your explanation. Switch between languages multiple times.
    - Aim for a concise yet informative explanation (maximum 4 sentences).
    - End with a brief summary or another way of using the sentence in a different context.
    - Do not provide phonetic pronunciation help.
    - Do not announce when you're doing the translation of the sentence.
    - Use primarely the language of "{baseIso}" for the explanation and the language of "{targetIso}" for the examples and context.
    - Focus on aspects requested by the user, avoiding repetition and excessive detail.
    - Ensure a natural flow as part of a podcast, maintaining listener engagement.
    - If a wordlist is provided, give extra attention to those words in your explanation.
    - Try to repeat the sentence at the end of the explanation in the target language which is "{targetIso}.
    - Oh and also just because the instructions are in english doesn't mean you have to use it you only have to use it if either "{baseIso}" or "{targetIso}" is is representing "EN" in the instructions.
    

    Remember, your explanation must contain both the base language for explanation and the target language for examples and context.
    """

    user_prompt = f"""
    Explain the following sentence: "{sentence}"

    Base language The language that you should talk about what's going on in the sentence of the story: {baseIso}
    Target language (being learned): {targetIso}
    Learner's level: {level} level. It's so that you know what kind of words you can use.
    Full story so that you know the  context of the story: "{fullStory}"
    this is what the user asked for when he specified what he wanted in the story: "{storyPrompt}"

    """

    if wordlist:
        user_prompt += f"\nWordlist to focus on: {wordlist}"
    else :
        user_prompt += f"\nNo wordlist has been provided."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        temperature=0.9,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response['choices'][0]['message']['content']

def ending_writer(fullStory, targetLanguage, baseLanguage, level):
    prompt_for_ending = f"""Hi, you are an excellent writer for a Podcast.
    please follow the following instructions:
    - I want you to write the ending of a language learning podcast that is for language learners who are learning {targetLanguage} at the {level} level.
    - The ending should be written only in {baseLanguage} and should not include any other languages.
    - Do not include any new information in the ending, just summarize the story and say goodbye to the listener.
    - The podcast doesn't has a name and you don't need to tell em them to subscribe or anything like that.
    - Keep the ending short and sweet.
    just say something like "And that's the end of our story about (storytopic). I hope you liked it and could learn something about the {targetLanguage} language." but be sure to say that in {baseLanguage}.
    
    for reference here's the full story so you know about what is the storypopic: {fullStory}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Hi, you are an excellent writer for a Podcast."},
            {"role": "user", "content": prompt_for_ending},
        ],
    )
    return response['choices'][0]['message']['content']