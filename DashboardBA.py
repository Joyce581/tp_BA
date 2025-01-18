import pandas as pd
import altair as alt
import streamlit as st

# Charger les données
data = pd.read_csv('data_dashboard_large.csv')

# Calcul des KPI globaux
total_ventes = data['Montant'].sum()
total_transactions = data['ID_Client'].count()
montant_moyen = data['Montant'].mean()
satisfaction_moyenne = data['Satisfaction_Client'].mean()

# Interface utilisateur
st.title("Dashboard Interactif des Ventes")

# Section Résumé
st.header("Vue d'ensemble") col1, col2, col3, col4 = st.columns(4) 
col1.metric("Total des ventes (€)", f"{total_ventes:,.2f}")
col2.metric("Nombre total de transactions", f"{total_transactions:,}")
col3.metric("Montant moyen par transaction (€)", f"{montant_moyen:,.2f}")
col4.metric("Satisfaction client moyenne", f"{satisfaction_moyenne:.2f}"

# Graphique des ventes quotidiennes
st.subheader("Ventes quotidiennes") 
chart = alt.Chart(ventes_journalieres).mark_line().encode( 
    x='Date_Transaction:T',
    y='Montant:Q' ).properties(title='Ventes quotidiennes'
) st.altair_chart(chart, use_container_width=True)
# Mettre à jour les calculs et les graphiques avec les données filtrées
total_ventes = data_filtre['Montant'].sum() 
total_transactions = data_filtre['ID_Client'].count() 
montant_moyen = data_filtre['Montant'].mean() 
satisfaction_moyenne = data_filtre['Satisfaction_Client'].mean()

# Analyse par magasin
st.header("Analyse par magasin")
ventes_par_magasin = data.groupby('Magasin')['Montant'].sum().reset_index()
ventes_par_magasin_chart = alt.Chart(ventes_par_magasin).mark_arc().encode(
    theta=alt.Theta(field="Montant", type="quantitative"),
    color=alt.Color(field="Magasin", type="nominal")
).properties(title='Répartition des ventes par magasin')
st.altair_chart(ventes_par_magasin_chart, use_container_width=True)

# Montant moyen par transaction pour chaque magasin
montant_moyen_magasin = data.groupby('Magasin')['Montant'].mean().reset_index()
montant_moyen_magasin_chart = alt.Chart(montant_moyen_magasin).mark_bar().encode(
    x='Magasin:N',
    y='Montant:Q'
).properties(title='Montant moyen par transaction pour chaque magasin')
st.altair_chart(montant_moyen_magasin_chart, use_container_width=True)

# Table des ventes totales et nombre de transactions par magasin
st.subheader("Ventes totales et nombre de transactions par magasin")
transactions_magasin = data.groupby('Magasin')['Montant'].agg(['sum', 'count']).reset_index()
st.dataframe(transactions_magasin)
# Filtre par magasin 
magasins = data['Magasin'].unique().tolist() 
magasin_selection = st.sidebar.multiselect('Sélectionner le magasin', magasins, default=magasins)
# Filtrer les données en fonction de la sélection 
data_filtre = data[data['Magasin'].isin(magasin_selection)]

# Analyse des catégories de produits
st.header("Analyse des catégories de produits")
quantite_categorie = data.groupby('Categorie_Produit')['Quantite'].sum().reset_index()
quantite_categorie_chart = alt.Chart(quantite_categorie).mark_bar().encode(
    x='Categorie_Produit:N',
    y='Quantite:Q'
).properties(title='Quantités vendues par catégorie')
st.altair_chart(quantite_categorie_chart, use_container_width=True)

# Graphique empilé des montants des ventes par catégorie et magasin
ventes_categorie_magasin = data.groupby(['Categorie_Produit', 'Magasin'])['Montant'].sum().reset_index()
empile_chart = alt.Chart(ventes_categorie_magasin).mark_bar().encode(
    x='Categorie_Produit:N',
    y='Montant:Q',
    color='Magasin:N'
).properties(title='Montants des ventes par catégorie et magasin')
st.altair_chart(empile_chart, use_container_width=True)

# Top 5 des produits les plus vendus par catégorie
st.subheader("Top 5 des produits les plus vendus par catégorie")
top5_produits = data.groupby('Categorie_Produit').apply(
    lambda x: x.nlargest(5, 'Quantite')).reset_index(drop=True)
st.dataframe(top5_produits)

# Analyse des modes de paiement
st.header("Analyse des modes de paiement")
mode_paiement = data['Mode_Paiement'].value_counts().reset_index()
mode_paiement.columns = ['Mode_Paiement', 'Count']
paiement_chart = alt.Chart(mode_paiement).mark_arc().encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Mode_Paiement", type="nominal")
).properties(title='Répartition des transactions par mode de paiement')
st.altair_chart(paiement_chart, use_container_width=True)

# KPI mode de paiement le plus utilisé
st.metric("Mode de paiement le plus utilisé", mode_paiement.iloc[0]['Mode_Paiement'])

# Analyse de la satisfaction client
st.header("Analyse de la satisfaction client")
satisfaction_magasin = data.groupby('Magasin')['Satisfaction_Client'].mean().reset_index()
satisfaction_magasin_chart = alt.Chart(satisfaction_magasin).mark_bar().encode(
    x='Magasin:N',
    y='Satisfaction_Client:Q'
).properties(title='Satisfaction par magasin')
st.altair_chart(satisfaction_magasin_chart, use_container_width=True)

satisfaction_categorie = data.groupby('Categorie_Produit')['Satisfaction_Client'].mean().reset_index()
satisfaction_categorie_chart = alt.Chart(satisfaction_categorie).mark_bar().encode(
    x='Categorie_Produit:N',
    y='Satisfaction_Client:Q'
).properties(title='Satisfaction par catégorie')
st.altair_chart(satisfaction_categorie_chart, use_container_width=True)

# Distribution des scores de satisfaction
st.subheader("Distribution des scores de satisfaction")
distribution_satisfaction = data['Satisfaction_Client'].value_counts().sort_index().reset_index()
distribution_satisfaction.columns = ['Score', 'Count']
distribution_satisfaction_chart = alt.Chart(distribution_satisfaction).mark_bar().encode(
    x='Score:O',
    y='Count:Q'
).properties(title='Distribution des scores de satisfaction')
st.altair_chart(distribution_satisfaction_chart, use_container_width=True)

