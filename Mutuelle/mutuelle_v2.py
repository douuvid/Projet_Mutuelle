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
            
    def visitor_body(self, text, cm, tm, fontDict, fontSize):
        y = tm[5]
        print(f"Text: {text}")
        print(f"Vertical Coordinate: {y}")
        print("--------------------")

    def remove_header_footer(self, page_content):
        # Votre code de suppression d'en-tête et de pied de page ici
        pass

 
        
        
file = Files("etude_tarifaire_sante_logo_(1).pdf")


        
            
    