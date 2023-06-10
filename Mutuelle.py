from PyPDF2 import PdfReader
import csv
import os


class Files:
    def __init__(self, filename):
        self.filename = filename
        self.parts = []

        if filename.endswith(".pdf"):
            reader = PdfReader(filename)
            for page_number, page in enumerate(reader.pages):
                extracted_text = page.extract_text()
                self.parts.append(extracted_text)
        else:
            print("Le fichier n'a pas l'extension .pdf")

    def visitor_body(self, text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if 50 < y < 720:
            self.parts.append(text)

    def exporte_csv(self, file):
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['text', "label"])
            for element in self.parts:
                element_split = element.split("\n")
                for ligne in element_split:
                    writer.writerow([ligne, "Null"])


dossier = "./Contrat/"
filename_a = "etude_tarifaire_sante_logo_(1).pdf"
filename_b = "etude_tarifaire_sante_logo_(2).pdf"
filename_c = "etude_tarifaire_sante_logo_(3).pdf"
filename_d = "etude_tarifaire_sante_logo_(4).pdf"
filename_e = "etude_tarifaire_sante_logo_(5).pdf"
filename_f = "etude_tarifaire_sante_logo_(6).pdf"
filename_g = "etude_tarifaire_sante_logo_(7).pdf"

file = {
    "fichier_1": filename_a,
    "fichier_2": filename_b,
    "fichier_3": filename_c,
    "fichier_4": filename_d,
    "fichier_5": filename_e,
    "fichier_6": filename_f,
    "fichier_7": filename_g
}

for key, filename in file.items():
    path_complet = os.path.join(dossier, filename)
    file_instance = Files(path_complet)
    file_instance.exporte_csv(f"Resultat_csv/{filename}.csv")
    reader = PdfReader(file_instance.filename)
    page = reader.pages[0]  # Première page, remplacez 0 par le numéro de la page souhaitée
    page.extract_text(visitor_text=file_instance.visitor_body)
    text_body = "".join(file_instance.parts)

    