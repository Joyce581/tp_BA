import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Calcul du total des ventes et affichage en histogramme")

# Téléchargement du fichier Excel
uploaded_file = st.file_uploader("data_dashboard_large-data_dashboard_large", type=["xlsx"])

if uploaded_file is not None:
    # Lecture du fichier Excel
    df = pd.read_excel(uploaded_file)
    
    # Affichage du dataframe
    st.write("Données du fichier Excel:")
    st.dataframe(df)
    
    # Calcul du total des ventes
    df['Total des Ventes'] = df.sum(axis=1)
    
    # Affichage du total des ventes
    st.write("Total des ventes calculé pour chaque ligne:")
    st.dataframe(df[['Total des Ventes']])

import pandas as pd

# Lire le fichier Excel
df = pd.read_excel('votre_fichier.xlsx')

# Calculer le total des ventes
total_ventes = df['Ventes_en_euros'].sum()

# Afficher le total des ventes
print(f"Total des ventes en euros : {total_ventes}")

  

