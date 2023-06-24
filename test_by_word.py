import os
import ocrmypdf
import pandas as pd
import pytesseract

import fitz

import tabula
import re
import spacy

"""_Bibliotheque _
Os permet==> d'interagir avec le système d'exploitation,
ocrmypdf est utilisé pour effectuer l'OCR (reconnaissance optique de caractères) sur les fichiers PDF,
pandas est une bibliothèque pour la manipulation de données, 
fitz est utilisé pour extraire le texte d'un fichier PDF, 
tabula est utilisé pour détecter et extraire les tableaux d'un fichier PDF
re est utilisé pour effectuer des opérations de recherche et de correspondance de motifs (regex).


   
"""

 

# Definition of the list of excluded words
black_list = ["de", "la", "par", "et", "le", "des",
              "à", "les", "au", "en", "du", "ou",
              "est", "l", "dans", "pour", "dont",
              "soit", "allianz", "d", "powered", "by",
              "org", "tel", "marketing", "toutes", "utilisons",
              "recueillons", "mais", "cachet", "cedex",
              "janvier", "une", "www", "que"]

stopwords = [
    "de", "la", "par", "et", "le", "des", "à", "les", "au", "en", "du", "ou",
    "est", "l", "dans", "pour", "dont", "soit", "allianz", "d", "powered", "by",
    "org", "tel", "marketing", "toutes", "utilisons", "recueillons", "mais",
    "cachet", "cedex", "janvier", "une", "www", "que", "sont", "sur", "avec",
    "il", "ne", "ce", "nous", "vous", "ils", "elles", "je", "j", "tu", "cette",
    "cet", "ces", "sa", "son", "ses", "notre", "nos", "votre", "vos", "leur",
    "leurs", "mon", "ma", "mes", "ton", "ta", "tes", "se", "qui", "quoi", "où",
    "quand", "comment", "pourquoi", "quel", "quelle", "quels", "quelles",
    "être", "avoir", "faire", "aller", "dire", "pouvoir", "vouloir", "venir",
    "voir", "savoir", "falloir", "devoir", "prendre", "donner", "trouver",
    "aimer", "dire", "partir", "venir", "temps", "jour", "année", "fois",
    "après", "avant", "pendant", "maintenant", "plus", "moins", "très", "peu",
    "trop", "aussi", "bien", "mal", "vraiment", "enfin", "alors", "ensuite",
    "donc", "mais", "car", "parce", "que", "si", "ou", "non", "avec", "sans",
    "chez", "vers", "pour", "jusque", "depuis", "avant", "après", "entre",
    "sous", "sur", "dans", "hors", "devant", "derrière", "autour", "tout",
    "tous", "toute", "toutes", "rien", "aucun", "chaque", "plusieurs", "autre",
    "autres", "quelque", "quelques", "beaucoup", "certains", "certaines",
    "ainsi", "alors", "alors", "lorsque", "alors", "autrement", "aussitôt",
    "auparavant", "aussi", "beaucoup", "bientôt", "cependant", "certes",
    "chaque", "d'abord", "davantage", "déjà", "demain", "dernièrement",
    "dès", "désormais", "devant", "dorénavant", "doucement", "d'un", "durant",
    "en", "encore", "ensemble", "ensuite", "entre", "environ", "et", "exactement",
    "fort", "franchement", "froidement", "généralement", "grâce", "hélas",
    "hier", "honnêtement", "immédiatement", "jamais", "jusqu'à", "là", "lentement",
    "maintenant", "mal", "malheureusement", "moins", "néanmoins", "nettement",
    "non", "nonchalamment", "nonobstant", "normalement", "notamment", "oui",
    "par", "parfois", "partout", "pas", "pauvrement", "peu", "peut-être",
    "plutôt", "précisément", "premièrement", "presque", "pourtant", "quand",
    "quant", "quasiment", "que", "quelquefois", "quoique", "rapidement",
    "rarement", "réellement", "régulièrement", "s'il", "sincèrement", "soi",
    "souvent", "strictement", "subitement", "surtout", "tantôt", "tard",
    "tellement", "tôt", "toujours", "tous", "toutefois", "très", "vite",
    "vivement", "volontiers", "vraiment", "maintenant"
]


# Definition of the function test_by_word


"""test_by_word()
 ==> prend un texte en entrée et renvoie une liste de mots avec leur pourcentage d'occurrence dans le texte.
 Elle utilise la liste d'exclusion des mots (black_list) pour exclure certains mots courants de l'analyse.
"""
def test_by_word(text, number):
    try:
        text_split = re.findall(r"[\w']+", text)
        dico = {}
        my_list = []

        for t in text_split:
            if t.lower() in black_list:
                continue
            if t.lower() not in dico:
                dico[t.lower()] = 0
            dico[t.lower()] += 1

        total = sum(dico.values())

        for word in dico:
            my_list.append((word, dico[word] / total * 100))
        my_list.sort(key=lambda x: x[1], reverse=True)

        print(f"Document numéro: {number}")
        print("")
        print(my_list)
        return my_list

    except Exception as e:
        print("Aucun mot", e)
        return None









"""determine_document_type()

prend une liste de mots avec leur pourcentage d'occurrence et détermine le type de document en fonction des mots clés et des scores associés.
Elle utilise les dictionnaires mots_cles_contrat_sante, mots_cles_contrat_iard et mots_cles_contrat_assurance_vie pour définir les mots clés 
et les scores associés à chaque type de contrat.

Elle calcule ensuite des scores pour chaque type de contrat en fonction de la correspondance des mots clés dans la liste de mots
et renvoie le type de document le plus probable.
"""




def determine_document_type(word_list):
    mots_cles_contrat_sante = {
        "Particulier": {
            "hospitalisation": 0.9,
            "consultation": 0.7,
            "médecin": 0.8,
            "spécialiste": 0.8,
            "chirurgie": 0.7,
            "médicaments": 0.6,
            "frais médicaux": 0.7,
            "remboursement": 0.7,
            "assurance maladie": 0.8,
            "garantie": 0.6,
            "couverture": 0.7,
            "mutuelle": 0.6,
            "pharmacie": 0.6,
            "hospitalier": 0.7,
            "maternité": 0.6,
            "dentaire": 0.6,
            "optique": 0.6,
        },
        "professionnels": {
            "salariés": 10,
            "entreprise": 10,
            "hospitalisation": 0.9,
            "consultation": 0.7,
            "médecin": 0.8,
            "spécialiste": 0.8,
            "chirurgie": 0.7,
            "médicaments": 0.6,
            "frais médicaux": 0.7,
            "remboursement": 0.7,
            "assurance maladie": 0.8,
            "garantie": 0.6,
            "couverture": 0.7,
            "mutuelle": 0.6,
            "pharmacie": 0.6,
            "hospitalier": 0.7,
            "dentaire": 0.6,
            "optique": 0.6,
        },
    }

    mots_cles_contrat_iard = {
        "habitation": {
            "maison": 0.8,
            "appartement": 0.7,
            "logement": 0.6,
            "dommages": 0.7,
            "assurance habitation": 0.9,
            "biens immobiliers": 0.7,
            "propriété": 0.6,
            "responsabilité civile" : 0.8,
            "sinistre" : 0.7,
            "vol" : 0.7,
            "dégât des eaux" : 0.7,
            "catastrophes naturelles" : 0.7,
            "protection juridique" : 0.6,
            "assurance automobile" : 0.8,
            "assurance moto" : 0.7,
            "assurance voyage" : 0.6,
            "assurance responsabilité professionnelle" : 0.7
        },
    }

    mots_cles_contrat_assurance_vie = {
        "capital décès": {
            "bénéficiaire": 0.8,
            "succession": 0.7,
            "capital décès": 0.9,
            "épargne": 0.7,
            "rente" : 0.7,
            "succession" : 0.8,
            "investissement" : 0.6,
            "bénéficiaire" : 0.7,
            "rendement" : 0.6,
            "clause bénéficiaire" : 0.8,
            "capitalisation" : 0.6,
            "transmission" : 0.7,
            "fiscalité": 0.6
        },
    }

    contrat_sante_score = 0
    contrat_iard_score = 0
    contrat_assurance_vie_score = 0
    contrat_sante_part_score = 0
    contrat_sante_pro_score = 0

    if word_list is None:
        return None

    for word, percentage in word_list:
        for contrat_type, mots_cles in mots_cles_contrat_sante.items():
            if word.lower() in mots_cles:
                score = mots_cles[word.lower()]
                contrat_sante_score += percentage * score
                if contrat_type == "Particulier":
                    contrat_sante_part_score += percentage * score
                elif contrat_type == "professionnels":
                    contrat_sante_pro_score += percentage * score

        for mots_cles in mots_cles_contrat_iard.values():
            if word.lower() in mots_cles:
                score = mots_cles[word.lower()]
                contrat_iard_score += percentage * score

        for mots_cles in mots_cles_contrat_assurance_vie.values():
            if word.lower() in mots_cles:
                score = mots_cles[word.lower()]
                contrat_assurance_vie_score += percentage * score

    print(f"Score contrat santé: {contrat_sante_score}")
    print(f"Score contrat IARD: {contrat_iard_score}")
    print(f"Score contrat assurance vie: {contrat_assurance_vie_score}")

    if contrat_sante_score > 0:
        if contrat_sante_part_score > contrat_sante_pro_score:
            return "Contrat Santé Particulier"
        elif contrat_sante_pro_score > contrat_sante_part_score:
            return "Contrat Santé Professionnel"
        else:
            return "Contrat Santé"
    elif contrat_iard_score > contrat_sante_score and contrat_iard_score > contrat_assurance_vie_score:
        return "Contrat IARD"
    elif contrat_assurance_vie_score > contrat_sante_score and contrat_assurance_vie_score > contrat_iard_score:
        return "Contrat Assurance Vie"
    else:
        return "Type de contrat indéterminé"


"""le directory fdp

   définissent le répertoire contenant les fichiers PDF à traiter et 
   créent une liste de fichiers PDF se terminant par l'extension ".pdf" dans ce répertoire.
    """
# Chemin du répertoire contenant les fichiers PDF
directory = "./Contrat/"
# Liste des fichiers PDF à traiter
file_list = [f for f in os.listdir(directory) if f.endswith('.pdf')]



def ocr_pdf(file_path):
    
    # OCR du fichier PDF
    ocr_file_name = f'OCR_{os.path.basename(file_path)}'
    ocr_directory = os.path.join(directory, "./Contrat/OCR_Resultat")
    os.makedirs(ocr_directory, exist_ok=True)
    ocr_file_path = os.path.join(ocr_directory, ocr_file_name)
    ocrmypdf.ocr(file_path, ocr_file_path, output_type='pdf', skip_text=True, deskew=True)
    return ocr_file_path


## Extraction du texte OCRed et détection des tableaux

def extract_text_and_tables(ocr_file_path, file_path):
    # Extraction du texte OCRed en utilisant PyMuPDF
    extracted_text = ""
    doc = fitz.open(ocr_file_path)
    for page in doc:
        extracted_text += page.get_text()

        # Détection des tableaux sur la page
        tables = tabula.read_pdf(file_path, pages=str(page.number + 1), silent=True, lattice=True)
        if len(tables) > 0:
            print(f"Tableau détecté sur la page {page.number + 1} du document {os.path.basename(file_path)}\n")

            print("Contenu du tableau:")
            for table in tables:
                print(table)
            
            print("")

    return extracted_text


def extract_text_and_tables_csv(ocr_file_path, file_path):
    # Extraction du texte OCRed en utilisant PyMuPDF (fitz)
    doc = fitz.open(ocr_file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Détection et extraction des tableaux en utilisant tabula
    tables = tabula.read_pdf(file_path, pages='all')

    # Création d'un DataFrame pandas à partir des tables extraites
    df_tables = pd.concat(tables)

    # Sauvegarde du DataFrame dans un fichier CSV
    csv_file_path = f'./Contrat/Tableau garanties/tables_extracted.csv'
    df_tables.to_csv(csv_file_path, index=False)

    return csv_file_path


##Analyse des mots, détermination du type de document et affichage du contenu OCR
def process_document(file_name):
    try:
        # Chemin complet du fichier PDF
        file_path = os.path.join(directory, file_name)

        # OCR du fichier PDF
        ocr_file_path = ocr_pdf(file_path)

        # Extraction du texte OCRed et détection des tableaux
        extracted_text = extract_text_and_tables(ocr_file_path, file_path)
        extracted_text_csv = extract_text_and_tables_csv(ocr_file_path, file_path)

        # Analyse des mots
        
        word_list = test_by_word(extracted_text, file_name)
        if word_list == None:
            raise ValueError("Erreur lors de l'analyse par mot.")

        

        # Détermination du type de document
        document_type = determine_document_type(word_list)
        print("")
        print(f"Nom du document : {file_name} | Type de document : {document_type}")
        print("")

        # Affichage du contenu du document scanné en essayant différents encodages
        encodings = ['utf-8']

        for encoding in encodings:
            try:
                
                with open(ocr_file_path, 'rb') as f:
                    content = f.read().decode(encoding)
                print(f"Contenu du document OCR ({encoding}): {file_name}")
                print(content)
                print("")
                break
            except UnicodeDecodeError:
                return word_list

    except UnicodeDecodeError as e:
        print(f"Erreur de décodage : {file_name} - {e}")
    except FileNotFoundError as e:
        print(f"Fichier introuvable : {file_name} - {e}")
    except Exception as e:
        print(f"Une exception s'est produite lors du traitement du fichier : {file_name} - {e}")


def remove_stopwords(text):
    doc = nlp(text)
    tokens = [token.text for token in doc if token.text.lower() not in stopwords]
    return " ".join(tokens)

nlp = spacy.load('fr_core_news_sm')
stopwords = spacy.lang.fr.stop_words.STOP_WORDS






"""
    Je vais mettre la suite en commenttaire mais le fichier test by word est parfait 
    Si besoin pour le reendre parfait a nouveau il suffit d'enlever les commentaire a for file name et file_names
    
"""
# file_names = ['etude_tarifaire_sante_logo_(1).pdf','etude_tarifaire_sante_logo_(2).pdf']

# for file_name in file_names:
#      process_document(file_name)
    
    
















## Il faut fare un contrat qui compare deux contrats entre par type de contrat 
## Pour qu'on puisse comparer des des banane avec des banane 




# def compare_type_contrat(file_names):
#     types_contrat = {}  # Dictionnaire pour regrouper les contrats par type
    
#     for file_name in file_names:
#         contrat_type = determine_document_type(file_name)
        
#         if contrat_type in types_contrat:
#             types_contrat[contrat_type].append(file_name)
#         else:
#             types_contrat[contrat_type] = [file_name]
    
#     for contrat_type, contrats in types_contrat.items():
#         print(f"Type de contrat : {contrat_type}")
#         print(f"Contrats : {contrats}")
#         print("--------------------")



# Traitement de chaque document
# for file_name in file_names:
#     process_document(file_name)
    

# Comparaison des contrats par type
#compare_type_contrat(file_names)

