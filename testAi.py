from PyPDF2 import PdfReader
import re
from skllm.config import SKLLMConfig
from skllm import ZeroShotGPTClassifier
from keras.models import Sequential
from keras.layers import Dense

# Configuration SKLLM


class Files():
    def __init__(self, filename):
        self.filename = filename
        self.parts = []

        if filename.endswith(".pdf"):
            reader = PdfReader(filename)
            for page_number, page in enumerate(reader.pages):
                extracted_text = page.extract_text()
                cleaned_text = self.remove_header_and_footer(extracted_text)
                self.parts.append(cleaned_text)
        else:
            print("Le fichier n'a pas l'extension .pdf")

    def remove_header_and_footer(self, page_content):
        lines = page_content.split("\n")
        header_lines = lines[:10]
        clean_lines = lines[10:]
        footer_lines = clean_lines[-5:]
        clean_lines = clean_lines[:-5]
        cleaned_content = "\n".join(clean_lines)
        return cleaned_content

    def without_some_word(self):
        not_this_word = ["S.A. au capital de 643 054 425 euros"]
        # Ajoutez votre code pour supprimer certains mots ici

# Initialisation de l'objet Files
file = Files("etude_tarifaire_sante_logo_(1).pdf")

# Extraction du texte et création du corpus
reader = PdfReader(file.filename)
for page_number, page in enumerate(reader.pages):
    extracted_text = page.extract_text()
    cleaned_text = file.remove_header_and_footer(extracted_text)
    file.parts.append(cleaned_text)

text_body = "".join(file.parts)

# Initialisation du modèle ZeroShotGPTClassifier
openAi = ZeroShotGPTClassifier()
openAi.fit(None, ['Honoraires', 'Forfait Journalier Hospitalier', 'Etablissements conventionnés', 'Etablissements non conventionnés', 'Divers', 'Forfait Naissance', 'Honoraires Médicaux', 'Analyses et examens de laboratoires', 'Honoraires paramédicaux', 'Médicaments', 'Matériel Médical', 'Divers', 'Equipements 100% Santé *', 'Equipements de classe II ***', 'Optique, Equipements 100% Santé *', 'Equipements de classe B ou mixtes **', 'Autres', 'Dentaire', 'Soins et Prothèses 100% Santé *', 'Soins', 'Prothèses', 'Traitement d\'orthodontie', 'Autres', 'Médecine douce / Prévention', 'Fonds Social/ Spécificités CCN', 'Services'])

# Prédiction des étiquettes pour chaque partie du texte
x = file.parts
labels = openAi.predict(x)

# Initialisation du modèle Keras
keras_model = Sequential()
# Ajoutez les couches souhaitées à votre modèle Keras ici
keras_model.add(Dense(units=..., activation=..., input_shape=(...)))
keras_model.add(Dense(units=..., activation=...))
# ... Ajoutez les autres couches nécessaires selon votre architecture

# Compilation du modèle Keras
keras_model.compile(loss=..., optimizer=..., metrics=[...])  # Spécifiez les valeurs appropriées pour chaque paramètre

# Entraînement du modèle Keras avec vos données d'entraînement
X_train = ...  # Remplacez par vos données d'entraînement
y_train = ...  # Remplacez par vos étiquettes d'entraînement
keras_model.fit(X_train, y_train, epochs=..., batch_size=...)  # Spécifiez le nombre d'époques et la taille du batch appropriés

# Prédiction du modèle Keras pour de nouvelles données
X_test = ...  # Remplacez par vos données de test
predictions = keras_model.predict(X_test)

# Affichage des prédictions et du texte associé
for i in range(len(labels)):
    print(labels[i], x[i], "\n")
    # Utilisez les prédictions et le texte associé selon vos besoins

