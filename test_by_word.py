import os
import ocrmypdf
import pandas as pd
import fitz
import tabula
import re

# Definition of the list of excluded words
black_list = ["de", "la", "par", "et", "le", "des",
              "à", "les", "au", "en", "du", "ou",
              "est", "l", "dans", "pour", "dont",
              "soit", "allianz", "d", "powered", "by",
              "org", "tel", "marketing", "toutes", "utilisons",
              "recueillons", "mais", "cachet", "cedex",
              "janvier", "une", "www", "que"]

# Definition of the function test_by_word
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
        print("Une exception s'est produite lors de l'exécution de test_by_word:", e)
        return None

# Definition of the function determine_document_type
def determine_document_type(word_list):
    contrat_sante_score = 0
    contrat_iard_score = 0
    contrat_assurance_vie_score = 0

    for word, percentage in word_list:
        for contrat_type, mots_cles in mots_cles_contrat_sante.items():
            for mot_cle, score in mots_cles.items():
                if word.lower() == mot_cle.lower():
                    contrat_sante_score += percentage * score

        for contrat_type, mots_cles in mots_cles_contrat_iard.items():
            for mot_cle, score in mots_cles.items():
                if word.lower() == mot_cle.lower():
                    contrat_iard_score += percentage * score

        for contrat_type, mots_cles in mots_cles_contrat_assurance_vie.items():
            for mot_cle, score in mots_cles.items():
                if word.lower() == mot_cle.lower():
                    contrat_assurance_vie_score += percentage * score

    if contrat_sante_score > contrat_iard_score:
        return "Contrat Santé"
    elif contrat_iard_score > contrat_sante_score:
        return "Contrat IARD"
    elif contrat_assurance_vie_score > contrat_iard_score and contrat_assurance_vie_score > contrat_sante_score:
        return "Contrat Assurance Vie"
    else:
        return "Type de document indéterminé"

# Definition of keywords for health, IARD, and life insurance contracts
mots_cles_contrat_sante = {
    "soins": {
        "hospitalisation": 0.9,
        "consultation": 0.7,
        "médecin": 0.8,
        "spécialiste": 0.8,
        "chirurgie": 0.7,
        "médicaments": 0.6,
        "frais médicaux": 0.7
    },
    "prothèses": {
        "dentaires": 0.8,
        "auditives": 0.7,
        "orthopédiques": 0.6,
        "prothèses": 0.7,
        "remboursement": 0.6,
        "appareillage": 0.5
    },
    "dépenses de santé": {
        "remboursement": 0.7,
        "prestations": 0.6,
        "frais médicaux": 0.7,
        "dépenses de santé": 0.8,
        "couverture santé": 0.6
    },
    "optique": {
        "lunettes": 0.7,
        "verres": 0.6,
        "monture": 0.5,
        "ophtalmologie": 0.7,
        "remboursement": 0.6,
        "optique": 0.8
    },
    "maternité": {
        "grossesse": 0.8,
        "accouchement": 0.9,
        "prénatal": 0.7,
        "postnatal": 0.7,
        "maternité": 0.9
    },
    "dentaire": {
        "dentaire": 0.8,
        "soins dentaires": 0.7,
        "orthodontie": 0.6,
        "prothèses dentaires": 0.7,
        "dents": 0.7
    }
}

mots_cles_contrat_iard = {
    "habitation": {
        "maison": 0.8,
        "appartement": 0.7,
        "logement": 0.6,
        "dommages": 0.7,
        "assurance habitation": 0.9,
        "biens immobiliers": 0.7,
        "propriété": 0.6
    },
    "automobile": {
        "voiture": 0.9,
        "véhicule": 0.8,
        "collision": 0.7,
        "accident": 0.8,
        "assurance auto": 0.9,
        "véhicule motorisé": 0.8,
        "conduite": 0.7,
        "sinistre": 0.6
    },
    "responsabilité civile": {
        "indemnisation": 0.7,
        "préjudice": 0.8,
        "responsabilité": 0.7,
        "dommage": 0.6,
        "indemnité": 0.7,
        "dommage matériel": 0.8,
        "dommage corporel": 0.9
    }
}

mots_cles_contrat_assurance_vie = {
    "capital décès": {
        "bénéficiaire": 0.8,
        "succession": 0.7,
        "capital décès": 0.9
    },
    "épargne": {
        "fonds en euros": 0.7,
        "unités de compte": 0.6,
        "primes": 0.7,
        "rachat partiel": 0.8
    },
    "avance sur contrat": {
        "avance sur contrat": 0.9,
        "clause bénéficiaire": 0.8,
        "valeur de rachat": 0.7
    }
}

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

##Analyse des mots, détermination du type de document et affichage du contenu OCR
def process_document(file_name):
    try:
        # Chemin complet du fichier PDF
        file_path = os.path.join(directory, file_name)

        # OCR du fichier PDF
        ocr_file_path = ocr_pdf(file_path)

        # Extraction du texte OCRed et détection des tableaux
        extracted_text = extract_text_and_tables(ocr_file_path, file_path)

        # Analyse des mots
        word_list = test_by_word(extracted_text, file_name)

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
                continue

    except UnicodeDecodeError as e:
        print(f"Erreur de décodage : {file_name} - {e}")
    except FileNotFoundError as e:
        print(f"Fichier introuvable : {file_name} - {e}")
    except Exception as e:
        print(f"Une exception s'est produite lors du traitement du fichier : {file_name} - {e}")
