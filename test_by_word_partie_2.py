



### faire les calcules en fonction du 2

### reperr les garantie 

### Convertir ou adapter en fonction du inclus ou pas 


#### les comparers

### determiner le meilleur contrat en fonction  de la demande

#===>ok fdp


from test_by_word import process_document, determine_document_type

def ok_comparaison(contrat_1, contrat_2):
    contrat1_type = determine_document_type(contrat_1)
    contrat2_type = determine_document_type(contrat_2)
    
    if contrat1_type == contrat2_type:
        return f"Ces contrats sont comparables car ils ont le même type de contrat ==> {contrat1_type}"
    else:
        return "Ce ne sont pas le même type de contrat."
    
    
    

def extract_garanties(contrat):
    return contrat.get("garanties", [])



def convertir_garantie_incluse_en_excluse(garantie):
    # Effectuer les calculs nécessaires pour convertir une garantie incluse en une garantie excluse
    garantie_convertie = garantie + " (convertie de incluse à excluse)"  # Exemple de conversion
    print(garantie_convertie)
    return garantie_convertie

def convertir_garantie_excluse_en_incluse(garantie):
    # Effectuer les calculs nécessaires pour convertir une garantie excluse en une garantie incluse
    garantie_convertie = garantie + " (convertie de excluse à incluse)"  # Exemple de conversion
    return garantie_convertie

def comparer_garanties(garanties_1, garanties_2):
    # Effectuer la comparaison des garanties et renvoyer un résultat
    if set(garanties_1) == set(garanties_2):
        return "Les garanties sont identiques."
    else:
        return "Les garanties sont différentes."

def inclus_or_exclus(contrat_1, contrat_2):
    # Vérifier si les contrats sont du même type (inclus ou exclus)
    contrat1_type = determine_document_type(contrat_1)
    contrat2_type = determine_document_type(contrat_2)

    if contrat1_type != contrat2_type:
        return "Les contrats ne sont pas du même type."

    # Extraire les garanties de chaque contrat
    garanties_1 = extract_garanties(contrat_1)
    garanties_2 = extract_garanties(contrat_2)

    # Convertir les garanties pour les mettre sur un pied d'égalité
    if contrat1_type == "inclus":
        # Convertir les garanties incluses en garanties exclues
        garanties_1 = [convertir_garantie_incluse_en_excluse(garantie) for garantie in garanties_1]
    else:
        # Convertir les garanties exclues en garanties incluses
        garanties_2 = [convertir_garantie_excluse_en_incluse(garantie) for garantie in garanties_2]

    # Comparer les garanties entre les deux contrats
    resultat_comparaison = comparer_garanties(garanties_1, garanties_2)

    return resultat_comparaison








file_names = ['etude_tarifaire_sante_logo_(1).pdf']

# Traiter chaque fichier
for file_name in file_names:
    contrat = process_document(file_name)
    type_contrat = determine_document_type(contrat)
    print(f"Type de contrat dans le fichier {file_name}: {type_contrat}")

# Comparer les types de contrat
if len(file_names) >= 2:
    contrat1 = process_document(file_names[0])
    contrat2 = process_document(file_names[1])
    resultat = ok_comparaison(contrat1, contrat2)
    print(resultat)
else:
    raise ValueError("Il n'y a qu'un seul document")
