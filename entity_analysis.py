from google.cloud import language
import mutuelle


def analyze_text_entities(text: str):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_entities(document=document)
    print(type(response.entities))
    i= 0
    for entity in response.entities:
        if i > 5:
            break
        print("=" * 80)
        results = dict(
            name=entity.name,
            type=entity.type_.name,
            salience=f"{entity.salience:.1%}",
            wikipedia_url=entity.metadata.get("wikipedia_url", "-"),
            mid=entity.metadata.get("mid", "-"),
        )
        for key, value in results.items():
            print(f"{key:15}: {value}")
        i +=1
            
# file = mutuelle.Files("./Contrat/etude_tarifaire_sante_logo_(1).pdf")
# file="\n".join(file.parts)
# print()
# analyze_text_entities(file)


def analyze_text_syntax(text: str):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_syntax(document=document)

    line = "{:10}: {}"
    print(line.format("sentences", len(response.sentences)))
    print(line.format("tokens", len(response.tokens)))
    for token in response.tokens:
        print(line.format(token.part_of_speech.tag.name, token.text.content))     
            
            
# file = mutuelle.Files("./Contrat/etude_tarifaire_sante_logo_(1).pdf")
# file="\n".join(file.parts)
# analyze_text_syntax(file)


def classify_text(text: str):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.classify_text(document=document)

    for category in response.categories:
        print("=" * 80)
        print(f"category  : {category.name}")
        print(f"confidence: {category.confidence:.0%}")
            
            

file = mutuelle.Files("./Contrat/etude_tarifaire_sante_logo_(1).pdf")
file="\n".join(file.parts)        
classify_text(file)






