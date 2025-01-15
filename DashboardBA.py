import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Dashboard Interactif des Performances de Vente")

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("data_dashboard_large - data_dashboard_large(1)", type=["csv"])

if uploaded_file is not None:
    # Lecture du fichier CSV
    df = pd.read_csv(uploaded_file)
    
    # Affichage du dataframe
    st.write("Données du fichier CSV:")
    st.dataframe(df)
    
    # Calcul des KPI globaux
    total_ventes = df['Montant'].sum()
    total_transactions = df.shape[0]
    montant_moyen = df['Montant'].mean()
    satisfaction_moyenne = df['Satisfaction_Client'].mean()
    
    # Affichage des KPI globaux
    st.subheader("Vue d'ensemble (Section Résumé)")
    st.write(f"Total des ventes (€): {total_ventes:.2f}")
    st.write(f"Nombre total de transactions: {total_transactions}")
    st.write(f"Montant moyen par transaction (€): {montant_moyen:.2f}")
    st.write(f"Satisfaction client moyenne (score de 1 à 5): {satisfaction_moyenne:.2f}")
    
    # Graphique des ventes quotidiennes
    df['Date_Transaction'] = pd.to_datetime(df['Date_Transaction'])
    ventes_quotidiennes = df.groupby(df['Date_Transaction'].dt.date)['Montant'].sum()
    
    fig, ax = plt.subplots()
    ventes_quotidiennes.plot(kind='line', ax=ax)
    ax.set_title('Ventes Quotidiennes')
    ax.set_xlabel('Date')
    ax.set_ylabel('Montant (€)')
    
    st.pyplot(fig)
    
    # Analyse par magasin
    st.subheader("Analyse par magasin")
    
    # Répartition des ventes par magasin
    ventes_par_magasin = df.groupby('Magasin')['Montant'].sum()
    fig, ax = plt.subplots()
    ventes_par_magasin.plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_ylabel('')
    ax.set_title('Répartition des Ventes par Magasin')
    
    st.pyplot(fig)
    
    # Montant moyen par transaction pour chaque magasin
    montant_moyen_par_magasin = df.groupby('Magasin')['Montant'].mean()
    fig, ax = plt.subplots()
    montant_moyen_par_magasin.plot(kind='bar', ax=ax)
    ax.set_title('Montant Moyen par Transaction par Magasin')
    ax.set_xlabel('Magasin')
    ax.set_ylabel('Montant Moyen (€)')
    
    st.pyplot(fig)
    
    # Tableau des ventes totales et nombre de transactions par magasin
    ventes_et_transactions_par_magasin = df.groupby('Magasin').agg({
        'Montant': 'sum',
        'ID_Client': 'count'
    }).rename(columns={'Montant': 'Ventes Totales (€)', 'ID_Client': 'Nombre de Transactions'})
    
    st.write("Ventes Totales et Nombre de Transactions par Magasin:")
    st.dataframe(ventes_et_transactions_par_magasin)

# Pour exécuter l'application Streamlit:
# streamlit run votre_script.py

