import os
import pandas as pd

import fitz
import frontend


def reduire_tableau(nom_tableau):
    # Charger le tableau CSV
    df = pd.read_csv(nom_tableau, header=None)

    # Supprimer les lignes redondantes ou vides dans la première colonne
    df[0] = df[0].drop_duplicates().dropna()

    # Sauvegarder le DataFrame modifié dans un nouveau fichier CSV
    nouveau_tableau = 'nouveau_tableau.csv'
    df.to_csv(nouveau_tableau, index=False)

    # Afficher le chemin du nouveau tableau
    print(f"Le nouveau tableau a été créé : {nouveau_tableau}")


# Exemple d'utilisation de la fonction reduire_tableau avec le nom du fichier CSV
reduire_tableau('./Contrat/Result_tableau/table_4.csv')



def reduire_le_tableau(nom_tableau):
    # Charger le tableau CSV récemment créé dans un DataFrame pandas
    df = pd.read_csv(nom_tableau)

    # Réduire les lignes du tableau
    df = df.iloc[::2]  # Garder uniquement une ligne sur deux

    # Créer un dossier pour le tableau réduit
    dossier_sortie = 'tableau_reduit'
    os.makedirs(dossier_sortie, exist_ok=True)

    # Sauvegarder le DataFrame réduit dans un nouveau fichier CSV
    tableau_reduit = os.path.join(dossier_sortie, 'tableau_reduit.csv')
    df.to_csv(tableau_reduit, index=False)

    print(f"Le fichier '{tableau_reduit}' a été créé dans le dossier '{dossier_sortie}'.")

# Exemple d'utilisation de la fonction reduire_tableau avec le nom du fichier CSV
reduire_tableau('./Contrat/Result_tableau/table_4.csv')

# Lire le fichier CSV
df = pd.read_csv('nouveau_tableau.csv', delimiter='\t')

# Transposer les lignes et colonnes
df = df.transpose()

# Enregistrer le DataFrame transposé dans un nouveau fichier CSV
df.to_csv('nouveau_fichier.csv', index=False)
