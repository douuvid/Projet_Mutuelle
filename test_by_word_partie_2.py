from test_by_word import determine_document_type, process_document

### Objectif valider que les contrats comparer entre eux sont du meme type
### --- Fait-----
### voir si le scripte voie le insclus ou non inclus

### faire les calcules en fonction du 2

### reperr les garantie 

####comparee 


### determiner le meilleur contrat en fonction  de la demande

#### les comparers



#===>ok fdp



def ok_comparaison(contrat_1, contrat_2):
    contrat1_type = determine_document_type(contrat_1)
    contrat2_type = determine_document_type(contrat_2)
    
    if contrat1_type == contrat2_type:
        return "Ces contrats sont comparables car ils ont le même type de contrat."
    else:
        return "Ce ne sont pas le même type de contrat."

file_names = ['etude_tarifaire_sante_logo_(1).pdf','etude_tarifaire_sante_logo_(2).pdf']  # Liste des noms de fichiers à traiter

# Traiter chaque fichier
for file_name in file_names:
    contrat = process_document(file_name)  # Extraire les informations du fichier et stocker dans un dictionnaire
    type_contrat = determine_document_type(contrat)  # Déterminer le type de contrat à partir du dictionnaire
    print(f"Type de contrat dans le fichier {file_name}: {type_contrat}")

# Comparer les types de contrat
if len(file_names) == 2:  # S'assurer qu'il y a exactement deux fichiers à comparer
    contrat1 = process_document(file_names[0])
    contrat2 = process_document(file_names[1])
    resultat = ok_comparaison(contrat1, contrat2)
    print(resultat)
