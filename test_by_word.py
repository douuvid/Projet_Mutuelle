import re
import mutuelle
import os

black_list=["de","la","par","et","le","des",
            "à","les","au","en","du","ou",
            'est',"l","dans","pour","dont",
            "soit","allianz","d","powered","by",
            "org","tel","marketing","toutes","utilisons",
            "recueillons","mais","cachet","11a_________________________________",
            "cedex","janvier","une","www","que"
            ]

def test_by_word(text, number):
    text_split = re.findall(r"[\w']+", text)

    dico = {}
    my_list = []

    for t in text_split:
        if t.lower() in black_list:
            continue
        if not t.lower() in dico:
            dico[t.lower()] = 0
        dico[t.lower()] = dico[t.lower()] + 1

    total = 0
    for word in dico:
        total += dico[word]

    for word in dico:
        my_list.append((word, dico[word] / total * 100))
    my_list.sort(key=lambda x: x[1], reverse=True)
    total += 1

    print("")
    print(f"Document numéro : {number} \n")
    print("")
    #print(my_list)
    
    return my_list


def word_segmentation(text, dictionary):
    segments = []
    max_length = len(max(dictionary, key=len))
    text_length = len(text)
    i = 0

    while i < text_length:
        j = min(i + max_length, text_length)
        while j > i:
            segment = text[i:j]
            if segment in dictionary:
                segments.append(segment)
                break
            j -= 1
        i = j

    return segments


def determine_type_document(my_list):
    score_sante = 0
    score_iard = 0
    
    for word, percentage in my_list:
        if word in mots_cles_contrat_sante:
            score_sante += 1
        if word in mots_cles_contrat_iard:
            score_iard += 1
    
    if score_sante > score_iard:
        return "Contrat Santé"
    elif score_iard > score_sante:
        return "Contrat IARD"
    else:
        return "Type de document indéterminé"


mots_cles_contrat_sante = ["soins", "prothèses", "santé", "hospitalisation", "consultation", "médecin", "br"]
mots_cles_contrat_iard = ["automobile", "habitation", "responsabilité", "dommage", "assurance"]

numbers = [1, 2, 3, 4]  # 567

for number in numbers:
    file = mutuelle.Files(f"./Contrat/etude_tarifaire_sante_logo_({number}).pdf")
    file = "\n".join(file.parts)
    my_list = test_by_word(file, number)
    document_type = determine_type_document(my_list)
    print(f"Document numéro : {number}")
    print("Type de document :", document_type)
