import openai
import json
try:
    import keys as Keys
    api_key = Keys.openai_key
    organization_id = Keys.openai_organization_id
    project_id = Keys.openai_project_id
except ImportError:
    api_key = input("Please enter your OpenAI API key: ")
    organization_id = input("Please enter your OpenAI organization ID: ")
    project_id = input("Please enter your OpenAI project ID: ")


openai.api_key = api_key
headers = {
    "Authorization": f"Bearer {api_key}",
    "OpenAI-Organization": organization_id,
    "OpenAI-Project": project_id,
}


def lang_differentiator(sentence, baselanguage, targetlanguage):
    # Parsen des JSON-Strings, um sicherzustellen, dass er korrekt formatiert ist
    #sentence = json.loads(sentence)
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""
            You are an expert in differentiating languages. Your task is to separate text by language and return the result in a structured JSON format with the following keys:
            - 'sentence': the original sentence provided by the user
            - 'language_segments': an array where each element is an object containing 'language_code' and 'text', representing each part of the sentence in the respective language.
            - 'languages': an array of languages used in the sentence, with each language appearing once.
            Follow these rules:
            1. Use the ISO language code as 'language_code' when switching languages.
            2. Only switch languages for actual words or phrases, not for punctuation or spaces.
            3. Maintain the original sentence structure and punctuation.
            4. Do not add any explanatory text.
            5. If you encounter single words for explanatory purposes in another language, ensure they are also marked.
            6. Return the output strictly as a JSON object.
            """},
            {"role": "user", "content": f"{sentence} // languages being used are {baselanguage} and {targetlanguage}"}
        ],
    )
    
    result = response
    
    
    return result['choices'][0]['message']['content']


# Example usage:
sentence = "Na een leuke ochtend op het festival, zegt de tekst: \"In de middag verkennen ze het festivalterrein.\" Dit betekent: \"À tarde, eles exploram o terreno do festival.\" \n\nHier is een uitleg van deze zin. \"In de middag\" refereert à parte do dia depois do almoço. \"Verkennen\" significa explorar, conhecer um lugar novo. \"Ze\" é um pronome que se refere a Anna e seus amigos. \"Het festivalterrein\" é o lugar onde o festival acontece, com muitas barracas, música e pessoas. \n\nEntão, a frase nos mostra que Anna e seus amigos estão se divertindo e descobrindo coisas novas à tarde. Você poderia usar uma frase parecida, por exemplo: \"In de ochtend wandelen ze in het park,\" que significaria \"De manhã, eles caminham no parque.\""
baselanguage = "PT"
targetlanguage = "NL"
output = lang_differentiator(sentence, baselanguage, targetlanguage)
print(output)
