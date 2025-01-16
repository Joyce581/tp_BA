import streamlit as st
import pandas as pd
import altair as alt

# Titre de l'application
st.title("Dashboard Interactif des Performances de Vente")

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("data_dashboard_large-data_dashboard_large(1)", type=["csv"])

if uploaded_file is not None:
    # Lecture du fichier CSV
    df = pd.read_csv(uploaded_file)

    # Section Résumé
    st.header("Vue d'ensemble (Section Résumé)")

    # Calcul des KPI globaux
    total_ventes = df['Montant'].sum()
    total_transactions = df.shape[0]
    montant_moyen = df['Montant'].mean()
    satisfaction_moyenne = df['Satisfaction_Client'].mean()

    # Affichage des KPI globaux
    st.metric("Total des ventes (€)", f"{total_ventes:,.2f}")
    st.metric("Nombre total de transactions", total_transactions)
    st.metric("Montant moyen par transaction (€)", f"{montant_moyen:,.2f}")
    st.metric("Satisfaction client moyenne (score de 1 à 5)", f"{satisfaction_moyenne:.2f}")

    # Graphique des ventes quotidiennes
    st.subheader("Ventes Quotidiennes")
    df['Date_Transaction'] = pd.to_datetime(df['Date_Transaction'])
    ventes_quotidiennes = df.groupby(df['Date_Transaction'].dt.date)['Montant'].sum().reset_index()
    ventes_quotidiennes_chart = alt.Chart(ventes_quotidiennes).mark_line().encode(
        x='Date_Transaction:T',
        y='Montant:Q'
    )
    st.altair_chart(ventes_quotidiennes_chart, use_container_width=True)

    # Analyse par magasin
    st.header("Analyse par magasin")
    
    # Répartition des ventes par magasin
    st.subheader("Répartition des ventes par magasin")
    ventes_par_magasin = df.groupby('Magasin')['Montant'].sum().reset_index()
    ventes_par_magasin_chart = alt.Chart(ventes_par_magasin).mark_arc().encode(
        theta=alt.Theta(field="Montant", type="quantitative"),
        color=alt.Color(field="Magasin", type="nominal")
    )
    st.altair_chart(ventes_par_magasin_chart, use_container_width=True)

    # Montant moyen par transaction pour chaque magasin
    st.subheader("Montant moyen par transaction pour chaque magasin")
    montant_moyen_par_magasin = df.groupby('Magasin')['Montant'].mean().reset_index()
    montant_moyen_par_magasin_chart = alt.Chart(montant_moyen_par_magasin).mark_bar().encode(
        x='Magasin:N',
        y='Montant:Q',
        color='Magasin:N'
    )
    st.altair_chart(montant_moyen_par_magasin_chart, use_container_width=True)

    # Tableau des ventes totales et nombre de transactions par magasin
    ventes_et_transactions_par_magasin = df.groupby('Magasin').agg({
        'Montant': 'sum',
        'ID_Client': 'count'
    }).rename(columns={'Montant': 'Ventes Totales (€)', 'ID_Client': 'Nombre de Transactions'}).reset_index()
    
    st.write("Ventes Totales et Nombre de Transactions par Magasin")
    st.dataframe(ventes_et_transactions_par_magasin)
    
    # Analyse des catégories de produits
    st.header("Analyse des catégories de produits")
    
    # Quantités vendues par catégorie
    st.subheader("Quantités vendues par catégorie")
    quantites_par_categorie = df.groupby('Categorie_Produit')['Quantite'].sum().reset_index()
    quantites_par_categorie_chart = alt.Chart(quantites_par_categorie).mark_bar().encode(
        x='Categorie_Produit:N',
        y='Quantite:Q',
        color='Categorie_Produit:N'
    )
    st.altair_chart(quantites_par_categorie_chart, use_container_width=True)
    
    # Montants des ventes par catégorie et magasin
    st.subheader("Montants des ventes par catégorie et magasin")
    ventes_categorie_magasin = df.groupby(['Categorie_Produit', 'Magasin'])['Montant'].sum().reset_index()
    ventes_categorie_magasin_chart = alt.Chart(ventes_categorie_magasin).mark_bar().encode(
        x='Magasin:N',
        y='Montant:Q',
        color='Categorie_Produit:N'
    )
    st.altair_chart(ventes_categorie_magasin_chart, use_container_width=True)
    
    # Top 5 des produits les plus vendus par catégorie
    st.subheader("Top 5 des produits les plus vendus par catégorie")
    top_5_produits = df.groupby(['Categorie_Produit', 'ID_Client']).agg({'Quantite': 'sum'}).reset_index().sort_values(by='Quantite', ascending=False).groupby('Categorie_Produit').head(5)
    st.write("Top 5 produits")
    st.dataframe(top_5_produits)

    # Analyse des modes de paiement
    st.header("Analyse des modes de paiement")

    # Répartition des transactions par mode de paiement
    st.subheader("Répartition des transactions par mode de paiement")
    transactions_par_paiement = df.groupby('Mode_Paiement')['ID_Client'].count().reset_index().rename(columns={'ID_Client': 'Nombre de Transactions'})
    transactions_par_paiement_chart = alt.Chart(transactions_par_paiement).mark_arc().encode(
        theta=alt.Theta(field="Nombre de Transactions", type="quantitative"),
        color=alt.Color(field="Mode_Paiement", type="nominal")
    )
    st.altair_chart(transactions_par_paiement_chart, use_container_width=True)
    
    # Mode de paiement le plus utilisé
    st.subheader("Mode de paiement le plus utilisé")
    mode_de_paiement_max = transactions_par_paiement.loc[transactions_par_paiement['Nombre de Transactions'].idxmax()]['Mode_Paiement']
    st.write(f"Le mode de paiement le plus utilisé est : {mode_de_paiement_max}")

    # Analyse de la satisfaction client
    st.header("Analyse de la satisfaction client")

    # Moyenne de satisfaction par magasin
    st.subheader("Moyenne de satisfaction par magasin")
    satisfaction_par_magasin = df.groupby('Magasin')['Satisfaction_Client'].mean().reset_index()
    satisfaction_par_magasin_chart = alt.Chart(satisfaction_par_magasin).mark_bar().encode(
        x='Magasin:N',
        y='Satisfaction_Client:Q',
        color='Magasin:N'
    )
    st.altair_chart(satisfaction_par_magasin_chart, use_container_width=True)
    
    # Moyenne de satisfaction par catégorie
    st.subheader("Moyenne de satisfaction par catégorie")
    satisfaction_par_categorie = df.groupby('Categorie_Produit')['Satisfaction_Client'].mean().reset_index()
    satisfaction_par_categorie_chart = alt.Chart(satisfaction_par_categorie).mark_bar().encode(
        x='Categorie_Produit:N',
        y='Satisfaction_Client:Q',
        color='Categorie_Produit:N'
    )
    st.altair_chart(satisfaction_par_categorie_chart, use_container_width=True)

    # Distribution des scores de satisfaction
    st.subheader("Distribution des scores de satisfaction")
    distribution_satisfaction = df['Satisfaction_Client'].value_counts().reset_index().rename(columns={'index': 'Score', 'Satisfaction_Client': 'Nombre'})
    distribution_satisfaction_chart = alt.Chart(distribution_satisfaction).mark_bar().encode(
        x='Score:N',
        y='Nombre:Q',
        color='Score:N'
    )
    st.altair_chart(distribution_satisfaction_chart, use_container_width=True)

