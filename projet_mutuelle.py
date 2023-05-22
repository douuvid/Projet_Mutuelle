from PyPDF2 import PdfReader
import re

class Files():
    def __init__(self, filename):
        self.filename = filename
        self.parts = []

        if filename.endswith(".pdf"):
            reader = PdfReader(filename)
            for page_number, page in enumerate(reader.pages):
                extracted_text = page.extract_text()
                cleaned_text = self.remove_header_footer(extracted_text)
                print(f"Page {page_number + 1}:")
                print(cleaned_text)
                print("--------------------")
                self.parts.append(cleaned_text)
        else:
            print("Le fichier n'a pas l'extension .pdf")
            
    def remove_header_footer(self, page_content):
        lines = page_content.split("\n")

        # Supprimer les lignes d'en-tête (par exemple, les 10 premières lignes)
        header_lines = lines[:10]
        clean_lines = lines[10:]

        # Supprimer les lignes de pied de page (par exemple, les 10 dernières lignes)
        footer_lines = clean_lines[-10:]
        clean_lines = clean_lines[:-10]

        # Retirer les phrases indésirables
        undesired_phrases = ["92076 PARIS LA DEFENSE CEDEX","N° d’Étude tarifaire : 1237439A l’Attention de","Etude tarifaire – Entreprise"]
        clean_lines = [line for line in clean_lines if not any(phrase in line for phrase in undesired_phrases)]

        # Utiliser une expression régulière pour supprimer la partie spécifique du footer
        regex_pattern = r"\d{5}\sPARIS\sLA\sDEFENSE\sCEDEX"
        clean_lines = [re.sub(regex_pattern, "", line) for line in clean_lines]

        # Reconstituer le contenu de la page sans les en-têtes, les pieds de page et les phrases indésirables
        cleaned_content = "\n".join(clean_lines)

        return cleaned_content

file = Files("etude_tarifaire_sante_logo_(1).pdf")
