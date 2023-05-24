from PyPDF2 import PdfReader
import re
from skllm.config import SKLLMConfig
from skllm import ZeroShotGPTClassifier




class Files():
    def __init__(self, filename):
        self.filename = filename
        self.parts = []

        if filename.endswith(".pdf"):
            reader = PdfReader(filename)
            for page_number, page in enumerate(reader.pages):
                extracted_text = page.extract_text()
                print(extracted_text)
                cleaned_text = self.remove_header_and_footer(extracted_text)
                
                # print(f"Page {page_number + 1}:")
                # print(cleaned_text)
                # print("--------------------")
                self.parts.append(cleaned_text)
        else:
            print("Le fichier n'a pas l'extension .pdf")

    def remove_header_and_footer(self, page_content):
        lines = page_content.split("\n")

        # Supprimer les lignes d'en-tête (par exemple, les 10 premières lignes)
        header_lines = lines[:10]
        clean_lines = lines[10:]

        # Supprimer les lignes de pied de page (par exemple, les 10 dernières lignes)
        footer_lines = clean_lines[-5:]
        clean_lines = clean_lines[:-5]

        # Retirer les phrases indésirables
        # undesired_phrases = ["92076 PARIS LA DEFENSE CEDEX", "N° d’Étude tarifaire : 1237439A l’Attention de",
        #                      "Etude tarifaire – Entreprise","S.A. au capital de 643 054 425 euros","JADIS ET ASSOCIES SAS","N° Siret : 92187904500018"]
        # clean_lines = [line for line in clean_lines if not any(phrase in line for phrase in undesired_phrases)]

        # Utiliser une expression régulière pour supprimer la partie spécifique du footer
        # regex_pattern = r"\d{5}\sPARIS\sLA\sDEFENSE\sCEDEX"
        # clean_lines = [re.sub(regex_pattern, "", line) for line in clean_lines]

        # Reconstituer le contenu de la page sans les en-têtes, les pieds de page et les phrases indésirables
        cleaned_content = "\n".join(clean_lines)
    

        return cleaned_content
    
    
    def visitor_body(self, text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 50 and y < 720:
            self.parts.append(text)
            
    #log a chaque boucle 
    
    #Trrouver des critere qui dit a chaque fois je suis dans le header faire ca et quand je suis dans le footer fait ca 
    #delimiter le header et le footer 
    
    
    #simple trouver un moyen de definir y et le passer en parametre 
    
            
    def without_some_word(self):
        not_this_world= ["S.A. au capital de 643 054 425 euros"]
        
            





file = Files("etude_tarifaire_sante_logo_(1).pdf")

reader = PdfReader(file.filename)
print("-----------------------------")
page = reader.pages[0]  # Première page, remplacez 0 par le numéro de la page souhaitée

page.extract_text(visitor_text=file.visitor_body)
text_body = "".join(file.parts)

print(text_body)


openAi=ZeroShotGPTClassifier()
openAi.fit(None, ['Honoraires', 'Forfait Journalier Hospitalier', 'Etablissements conventionnés',"Etablissements non conventionnés","Divers","Forfait Naissance","Honoraires Médicaux","Analyses et examens de laboratoires","Honoraires paramédicaux","Médicaments","Matériel Médical","Divers","Equipements 100% Santé *","Equipements de classe II ***","Optique,Equipements 100% Santé *","Equipements de classe B ou mixtes **","Autres","Dentaire","Soins et Prothèses 100% Santé *",
"Soins","Prothèses","Traitement d'orthodontie","Autres","Médecine douce / Prévention","Fonds Social/ Spécificités CCN","Services"])
x= file.parts
labels = openAi.predict(x)

for i in range(len(labels)):
    print(labels[i],x[i],"\n")


        

