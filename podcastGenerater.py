import requests
import json
import re
from openAiPodcastGenerator import lang_differentiator, emptyPromptFunction, empty_GPT4o_mini, lang_finetune_differentiator, sentence_explainer,ending_writer
from gemini_functions import *
from claudeAiPodcast import claude_lang_separator
from savedocs import *

try:
    import keys as Keys
    api_key = Keys.gemini_key
except ImportError:
    api_key = input("Please enter your gemini API key: ")


level = input("\033[93m" + 'what is your level? \n' + "\033[0m").upper()
while level not in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'N']:
    print("\033[91m" + 'Invalid level. Please enter a level between A1 and C2. Please enter something like A1, A2, B1, B2, C1, C2 or n for none' + "\033[0m")
    level = input('what is your  the level that you are learning your language? \n').upper()
print("\033[92m" + f"your level is {level}" + "\033[0m")
target_language = input("\033[93m" + 'what is the language that you are currently learning? \n' + "\033[0m").upper()
storyInput = input('\033[92m' + 'what should the story be about (do not leave this empty)' + '\033[0m')
print("\n \n ")
print(" \n ")
print(" \n ")
endtext=""
open_ai_tokens = 0
baselanguage = input("\033[93m" + 'what is the language that you want to have it teached? \n' + "\033[0m").upper()
storyPrompt =f"I want you to write me a story in {target_language} that is about " +storyInput +f"be sure that the story is written in the level of {level} and using only wordsfrom the following language: {target_language}."
if level!='N':
    endtext =f"{storyPrompt} that is also purely written in the level of {level} in {target_language}."

def generate_story_prompt(target_language, level, story_topic, wordlist=None):
    base_prompt = f"""
    Create an engaging story in {target_language} based on the following topic and requirements:

    Topic and Special Requirements: "{story_topic}"

    Note: The topic and requirements above may be provided in any language, but your task is to write the story entirely in {target_language}. Pay close attention to any specific instructions regarding grammar, tense, or other linguistic aspects mentioned in the topic.

    The story should be appropriate for language learners at the {level} level.
    Ensure the story uses vocabulary and grammar structures suitable for this level, while also incorporating any specific grammatical requirements mentioned in the topic (e.g., using a particular tense).

    Guidelines:
    1. Write the entire story in {target_language}, regardless of the language of the provided topic and requirements.
    2. Strictly adhere to any grammatical or structural requirements specified in the topic (such as using a specific tense or focusing on particular grammar points).
    3. Use clear and concise language appropriate for {level} learners.
    4. Include a variety of sentence structures typical for {level}, unless the topic specifies a focus on particular structures.
    5. Ensure the story has a clear beginning, middle, and end.
    6. Aim for a story length of approximately 250-300 words. (feel free to aim for a shorter story if the user requests it in his requirements)
    """
    
    if wordlist:
            word_integration = f"""
            Additionally, you must incorporate words from the following wordlist into the story:

            {wordlist}

            Important notes about word usage:
            - Interpret the wordlist in the most appropriate way. It may be a simple list, comma-separated, JSON format, or any other structure.
            - Try to include as many words or concepts from this list as possible in the story.
            - You have the flexibility to use different forms of the words as appropriate:
            - For verbs: You may conjugate them or use different tenses as needed, ensuring consistency with any tense requirements specified in the topic.
            - For nouns: You may use singular or plural forms.
            - For adjectives: You may use comparatives or superlatives if it fits the context.
            - The goal is to include the words or their concepts naturally within the story's context.
            - Use these words or their variations in a way that helps illustrate their meaning.
            """
            base_prompt += word_integration
        
    base_prompt += f"\nPlease provide the story in {target_language}, ensuring you follow all specified requirements:"
    
    return base_prompt


def get_wordlist():
    print("\033[93mDo you have a wordlist of words that you're currently studying?")
    print("You can enter words in any format: plain text, comma-separated, JSON, or any other structure.")
    print("If you don't have a wordlist, just press Enter to skip.\033[0m")
    
    wordlist_input = input("Enter your wordlist (or press Enter to skip): ").strip()
    
    if not wordlist_input:
        return None
    
    return wordlist_input

# Usage in your main code
wordlist = get_wordlist()
storyPrompt = generate_story_prompt(target_language, level, storyInput, wordlist)

if wordlist:
    print("Wordlist provided. It will be incorporated into the story generation.")
else:
    print("No wordlist provided.")


def Introwriter(fullStory, targetLanguage, baseLanguage, level, ):
    promptForIntro = f"""Hi, you are an excellent introduction writer for a Podcast.
      I want you to write me an introduction for a language learning podcast that is for language learners who are learning {targetLanguage} at the {level} level.
       The introduction should be written only in {baseLanguage} and should not include any other languages.
        You should write an introduction that is about the following story: "{fullStory}" .

        Now that you know the full story, keep in mind that as the last sentence, the listener will also hear this story in the language of {targetLanguage}.
        So, you should tell the listener something like "And now we're going to listen to the full story" in {baseLanguage}.
        Keep the introduction short and sweet."""
    introduction =podcastgenerator(api_key, promptForIntro)
    return introduction

def betweenPart(baselanguage, story):
    promptForBetween = f"""
    Hi, you are writing a part of a podcast for languagelearners and your part is the transition between the story and the explanation part of the story.
    You will be provided with a story and you should just mention a very brief summary of the story that the listener is about to hear. 
    before your part that you write the listener will hear the full story read in an normal speed. 
    Your job is to write a transition that is in the {baselanguage} language and that is a transition between the story and the explanation of the story.
    because after you the listener will hear the full story again but this time it's gonna be in a slower pace, and with translations and explenations for each sentence.

    The story of the podcast is the following: "{story}".

    Now that you know what the story is about answer only with the betweensection and nothing else. 
    And make sure to only use the {baselanguage} language in your answer.
    """
    inbetween_Part =podcastgenerator(api_key, promptForBetween)
    return inbetween_Part

def updateTokens(currentTokens, newTokens):
    currentTokens += newTokens
    return currentTokens

def explainPrompter(sentence, baseIso, targetIso, wordlist, level, fullStory, storyPrompt):#story Prompt has to be added
    startPrompt = f"""
            As an expert language teacher for a podcast, explain the following sentence from a {targetIso} story to a {level} level learner of {targetIso}. The explanation should be in {baseIso}.

            for context here's the full story for context: {fullStory}

            Current sentence to explain: "{sentence}"

            To give some rough guidlines on what the user wants the story to be focused and maby also what linguistic features the user wants to have explained here's the users Prompt: "{storyPrompt}" 

            Guidelines:
            - Start with a smooth transition from the last sentence if there was one (obviously ignore this if it's beeing the first sentence.) 
            - Explain the sentence, focusing on its meaning and any challenging words or structures.
            - If the sentence contains words from this list: {wordlist}, provide extra explanation and examples.
            - Aim for a concise yet informative explanation (maximum 5 sentences please don't go over that threshhold).
            - End with a brief summary or another way of using the sentence in a different context. 
            - Also try your best to not give any helps on how the words are supposed to sound like phonetically.
            - Super important is that you only use the languages {baseIso} and {targetIso} in the explanation and nothing else.
            - At least once the sentence should come fully translated in the language of {baseIso}.
            - Focus your attention not to every single word and try to not repeat yourself too much. Focus more on what the user is asking for.
            - Try to be compact and don't give too much information if it is not requested by the user
            - All the Answers you give should contain both languages the {baseIso} for the explenation and the {targetIso} so that the user knows what sentence we're currently talking abotut.
            
            Remember, your explanation should flow naturally as part of a podcast, maintaining listener engagement between sentences.
            """
    return startPrompt

def explainSentence(fullstory, baseLanguage, targetLanguage, wordlist=None, level=None):
    sentences = re.split('[.!?]', fullstory)
    #sentences = re.findall(r'[^.!?]+[.!?]', fullstory) ## With this the punctuation is included in the sentence.
    promptForExplanation = ""
    combineedExplanations = ""
    print("\033[91m" + str(sentences) + "\033[0m")
    print("\033[91m" + " \n those should've been the sentences" + "\033[0m")
    if wordlist:
        for sentence in sentences:
            promptForExplanation = f"""
            Hi, you are an excellent teacher for foreign languages and are an expert to distinguish the languages from each other, for a podcast.
            You will be given a sentence from a story that is written in the language of {targetLanguage}.
            Your job is to explain the sentence in the language of {baseLanguage}.
            I want you to explain the sentence in a way that a language learner who is learning {targetLanguage} at the {level} level would understand and also learn something from it.
            If a word from the wordlist is being used in the sentence, you should explain it extra carefully and put more emphasis on it by using it in other sentences as well.
            You will be given the following sentence: "{sentence}".
            If none of the words from the wordlist are used in the sentence, you should explain another word that might be challenging for someone at the {level} level.
            Here is the wordlist that the listener is currently learning: "{wordlist}".
            Please try to only write 3-5 sentences as a explanation. for the sentence that you are given.
            When you have done that I will need you to differenciate the text by language. (so that in the production will know which language there is to use)
            """
            currentExplanation = podcastgenerator(api_key, promptForExplanation)["candidates"][0]["content"]["parts"][0]["text"]
            combineedExplanations = combineedExplanations + currentExplanation
            print("\033[91m" + currentExplanation + "\033[0m")
            print("\n\n")
            print("next phrase (with wordlist)")
            

    else:
        for sentence in sentences:
            promptForExplanation = f"""Hi, you are an excellent teacher for foreign languages, for a podcast.
            You will be given a sentence from a story that is written in the language of {targetLanguage}.
            Your job is to explain the sentence in the language of {baseLanguage}.
            I want you to explain the sentence in a way that a language learner who is learning {targetLanguage} at the {level} level would understand and also learn something from it.
            You will be given the following sentence: "{sentence}".
            If none of the words from the wordlist are used in the sentence, you should explain another word that might be challenging for someone at the {level} level."""
            currentExplanation = podcastgenerator(api_key, promptForExplanation)["candidates"][0]["content"]["parts"][0]["text"]
            combineedExplanations = combineedExplanations + currentExplanation
            print("\033[91m" + currentExplanation + "\033[0m")
            print("\n\n")
            print("next phrase")
    
    return combineedExplanations



#create the story
finishedStory = emptyPromptFunction(storyPrompt)
isoBase = get_ISO(baselanguage)
isoTarget = get_ISO(target_language)
print(finishedStory)
if "candidates" in finishedStory:
    finishedStory = finishedStory["candidates"][0]["content"]["parts"][0]["text"]

ensure_output_directory()
storytitle = generateTitle(finishedStory, target_language)["candidates"][0]["content"]["parts"][0]["text"]
print("the title of the story is: " + storytitle)
filepath = generate_filename(storytitle)
create_empty_file(filepath, isoTarget, isoBase)
add_title(filepath, storytitle)
add_story(filepath, finishedStory)
add_wordList(filepath, wordlist)

print("\n \n")
#Intro
introText = Introwriter(finishedStory, target_language, baselanguage, level)
print(introText["candidates"][0]["content"]["parts"][0]["text"])
add_intro(filepath, introText["candidates"][0]["content"]["parts"][0]["text"])
#the story
print("\033[92m" + finishedStory + "\033[0m")
#between part(the transition between the story and the explenation of the story)
betweenPart = betweenPart(baselanguage, finishedStory)
print("\n"+ betweenPart["candidates"][0]["content"]["parts"][0]["text"])
add_betweenpart(filepath, betweenPart["candidates"][0]["content"]["parts"][0]["text"])
storySentences = re.split('[.!?]', finishedStory)

add_story(filepath, finishedStory)
#story explenation
def process_openai_object(openai_object):
    # Wandelt das OpenAIObject in einen JSON-String um
    json_str = json.dumps(openai_object)
    return json.loads(json_str)

for index, sentence in enumerate(storySentences, start=1):
    #explenationPrompt = explainPrompter(sentence, isoBase, isoTarget, wordlist, level, finishedStory, storyInput)
    #sentenceExplenation = empty_GPT4o_mini(explenationPrompt)
    sentenceExplenation = sentence_explainer(sentence=sentence, baseIso=isoBase, targetIso=isoTarget, level=level, fullStory=finishedStory, storyPrompt=storyInput, wordlist=wordlist)
    print("\n")
    differentiated = claude_lang_separator(sentenceExplenation, isoBase, isoTarget)

    # Verarbeite das OpenAIObject
    """
    differentiated_json = process_openai_object(differentiated)

    differentiatedContent = differentiated_json["choices"][0]["message"]["content"]
    differentiatedCount = differentiated_json["usage"]["total_tokens"]"""
    differentiatedContent = differentiated[0].text
    print("\033[92m" + f"Message: {differentiatedContent}" + "\033[0m")

    print(f"Message: {differentiatedContent}")
    # print(f"Token count: {differentiatedCount}")
    append_explanation(filepath, sentence, differentiatedContent, sentenceExplenation, index)


#print("\n"+explainSentence(finishedStory["candidates"][0]["content"]["parts"][0]["text"], baselanguage, target_language, wordlist, level))

print("\n \n")
outro = ending_writer(baselanguage, target_language, baselanguage, level)
print(f"the outro is: {outro}")
add_outro(filepath, outro)
print("\n \n")
print(f"This is the end of the podcast all file should be saved in the output folder with the name of {storytitle}.json")