
# Imports the Google Cloud client library
from google.cloud import language_v1
from mutuelle import Files
from google.cloud import language_v1beta2
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/davidravin/Desktop/Projet Mutuelle/clef.json"
file = Files("./Contrat/etude_tarifaire_sante_logo_(1).pdf")
content="\n".join(file.parts)
# Instantiates a client
client = language_v1.LanguageServiceClient()

# The text to analyze
text = u"Hello, world!"
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

print("Text: {}".format(text))
print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))


def sample_classify_text():
    # Create a client
    client = language_v1.LanguageServiceClient()

    # Initialize request argument(s)
    document = language_v1.Document()
    document.content = content

    request = language_v1.ClassifyTextRequest(
        document=document,
    )

    # Make the request
    response = client.classify_text(request=request)

    # Handle the response
    print(response)

print("ca tourne 1")

def sample_analyze_entities():
    # Create a client
    client = language_v1beta2.LanguageServiceClient()
    
    # Initialize request argument(s)
    document = language_v1beta2.Document()
    document.content = "content_value"

    request = language_v1beta2.AnalyzeEntitiesRequest(
        document=document,
    )

    print("cool")
    # Make the request
    response = client.analyze_entities(request=request)
    
    # Handle the response
    print(response)


sample_analyze_entities()