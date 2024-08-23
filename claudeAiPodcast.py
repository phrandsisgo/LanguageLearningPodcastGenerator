import anthropic
import os
from keys import anthropic_key

# Initialisieren Sie den Client mit dem API-Schlüssel aus keys.py
client = anthropic.Anthropic(
    api_key=anthropic_key,
)
def generate_claude_request(request):
  message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=4000,
    temperature=0,
    system=" Your Task is to write short stoies about stuff that the user wants.",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": request
          }
        ]
      }
    ]
  )
  print(message.content)

def claude_lang_separator(sentence, baselanguage, targetlanguage):
  message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=4000,
    system="""
      You are an expert in differentiating languages for a podcast. Your task is to separate text by language, following these rules:
      1. Use separators (---) followed by the correct ISO language code when switching languages.
      2. Only switch languages for actual words or phrases, not for punctuation or spaces.
      3. Maintain the original sentence structure and punctuation.
      4. Do not add any explanatory text; only provide the differentiated sentence. Your job is also not to help with the 
      5. If you see a single word for a explenation purpose that is in an other language like the rest is has to be differentiated as well.
      """,
    temperature=0.3,
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": f""" the first sentence that you need to differentiate is the following: the Sentence, "Я на улице!" means I'm outside. However, "на улице" can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, "на улице" has 2 meanings. // Baselanguage: "EN" Targetlanguage "RU"  """
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": f""" ---EN the first sentence that you need to differentiate is the following: the Sentence, ---RU Я на улице ---EN means I'm outside. However, ---RU на улице ---EN can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, ---RU на улице ---EN has 2 meanings. """
          }
        ] 
      },

      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text":  f""" "Was läuft bei dir Junge?" means "what's up with you, boy?" in English if we want to be literal. But you can also translate it as: "what's up dude" it is usually used in informal settings. But literally the word "läuft" means walking and "Junge" means boy. One last time the full sentence: "Was läuft bei dir Junge?"' // Baselanguage: "EN" Targetlanguage "DE"  """
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": f""" ---DE "Was läuft bei dir Junge?" ---EN means 'What's up with you, boy?' in English if we want to be literal. But you can also translate it as: 'what's up dude' it is usually used in informal settings. But literally the word ---DE "läuft" ---EN means walking and ---DE Junge ---EN means boy. One last time the full sentence: ---DE Was läuft bei dir Junge? """
        
          },
        ]
      },

      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text":  f""" "Anna kijkt naar de mensen om zich heen en denkt aan het festival. Ze denkt: \"Het Sziget Festival was een van de beste momenten van haar leven.\" \n\nEsta frase significa que o festival foi uma experiência muito especial e positiva para Anna. A palavra \"beste\" quer dizer que foi uma das melhores experiências. \"Momenten\" se refere a períodos de tempo que foram importantes ou memoráveis. Essa estrutura é usada para descrever eventos significativos na vida de alguém. \n\nUm exemplo semelhante poderia ser: \"De vakantie was een van de mooiste tijden van het jaar.\" Isso mostra que você teve uma experiência feliz. No caso de Anna, o festival ficou na memória dela como um momento especial." // Baselanguage: "PT" Targetlanguage "NL" """
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": f""" ---NL Anna kijkt naar de mensen om zich heen en denkt aan het festival. Ze denkt: \"Het Sziget Festival was een van de beste momenten van haar leven.\" \n\n---PT Esta frase significa que o festival foi uma experiência muito especial e positiva para Anna. A palavra ---NL \"beste\" ---PT quer dizer que foi uma das melhores experiências. \"Momenten\" se refere a períodos de tempo que foram importantes ou memoráveis. Essa estrutura é usada para descrever eventos significativos na vida de alguém. \n\n Um exemplo semelhante poderia ser: ---NL \"De vakantie was een van de mooiste tijden van het jaar.\" ---PT Isso mostra que você teve uma experiência feliz. No caso de Anna, o festival ficou na memória dela como um momento especial."""
        
          },
        ]
      },

      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text":  f""" "Emely a Lánchídnál van, és éppen csodálja a hidat, amikor azt mondja: \"\" - mondja magában. En français, cela signifie : \"elle dit dans sa tête\". Cette phrase montre qu'Emely pense quelque chose sans le dire à haute voix. Le verbe “mond” signifie “dire”, et “magában” signifie “dans sa tête”. C'est une façon de montrer ce que l'on ressent ou pense intérieurement. Par exemple, si vous voyez quelque chose de beau, vous pouvez également dire “c’est magnifique!” - magában. \n\nEn résumé, cette phrase nous permet de comprendre ce que ressent Emely sans qu'elle le dise à voix haute." // Baselanguage: "FR" Targetlanguage "HU" """
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text":  f"""---HU Emely a Lánchídnál van, és éppen csodálja a hidat, amikor azt mondja: \"\" - mondja magában. ---FR En français, cela signifie : \"elle dit dans sa tête\". Cette phrase montre qu'Emely pense quelque chose sans le dire à haute voix. Le verbe ---HU “mond” ---FR signifie “dire”, et ---HU “magában” ---FR signifie “dans sa tête”. C'est une façon de montrer ce que l'on ressent ou pense intérieurement. Par exemple, si vous voyez quelque chose de beau, vous pouvez également dire  “c’est magnifique!” ---HU magában. \n\n---FR En résumé, cette phrase nous permet de comprendre ce que ressent Emely sans qu'elle le dise à voix haute."""
        
          },
        ]
      },

      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text":  f""" "{sentence}" // Baselanguage: "{baselanguage}" Targetlanguage "{targetlanguage}" """
          }
        ]
      },



    ]
  )
  return message.content
