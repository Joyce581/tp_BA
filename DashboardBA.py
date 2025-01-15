
import pandas as pd
import matplotlib.pyplot as plt 
# Lire le fichier Excel
df = pd.read_excel('data_dashboard_large-data_dashboard')

# Calculer le total des ventes
total_ventes = df['Ventes_en_euros'].sum()

# Afficher le total des ventes
print(f"Total des ventes en euros : {total_ventes}")

  

