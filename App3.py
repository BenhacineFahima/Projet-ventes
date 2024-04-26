import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go

from itertools import combinations
from collections import Counter

from itertools import combinations
from collections import Counter
from util import *

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_csv(path,delimiter,index):
    df = pd.read_csv(path,delimiter=f"{delimiter}")
    df[f'{index}'] = pd.to_datetime(df[f'{index}'])
    df = df.set_index(f'{index}')
    return df

df = get_data_from_csv('data_clean.csv',',','Order Date')
################################
def concat_produit_par_order_id(liste : list):
    """concaténer les produits pour chaque commende avec ; comme séparateur"""
    return '; '.join(liste)
###############################################


# ---- SIDEBAR ----
st.sidebar.header("Filtrer içi:")
city = st.sidebar.multiselect(
    "Sélectionner la ville:",
    options=df["ville"].unique(),
    default=df["ville"].unique()
)

mois = st.sidebar.multiselect(
    "Sélectionner le mois:",
    options=df["Mois_Fr"].unique(),
    default=df["Mois_Fr"].unique(),
)


df_selection = df.query(
    "ville== @city & Mois_Fr ==@mois "
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["chiffres_daffaires"].sum())
average_sale_by_transaction = round(df_selection["chiffres_daffaires"].mean(), 2)
### COMMON PROD
df_duplique = df_selection[df_selection['Order ID'].duplicated(keep = False)]
ensemble_commandes = df_duplique.groupby('Order ID')['Product'].apply(concat_produit_par_order_id)
##################################################
def mcommon(k):
    count = Counter()
    # donner la frequence des k produits qui ont été acheté ensemble
    for achat in ensemble_commandes:
        prod = achat.split(';')
        count.update(Counter(combinations(prod,k)))
    return count.most_common(1)


#########################


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    with st.expander("**Les k produits les plus achetés ensemble**",expanded=False):
        # Sélection de la valeur k
        k = st.selectbox("Sélectionnez k :", [2, 3])
        result = mcommon(k)
        # Création d'un DataFrame à partir des résultats
        st.markdown('<div>', unsafe_allow_html=True)
        # Affichage de chaque produit dans un cadre
        for item in result:
            for produit in item[0]:
                st.markdown(f'<div style="border: 2px solid white; padding: 5px; margin: 5px; display: inline-block;border-radius: 5px;">{produit}</div>', unsafe_allow_html=True)
        # Fermeture de la div
        st.markdown('</div>', unsafe_allow_html=True)
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

 # Afficher le dataframe danzs un expander  
with st.expander("Data"):
        st.write(df_selection)
st.markdown("""---""") # ajouter une ligne de séparation horizontale


st.header("Analyse par Mois et Ville")

# SALES BY MONTH FIG1
# Groupement des données par mois et calcul du chiffre d'affaires total
chiffra_affaire_par_mois = df_selection.groupby('Mois_Fr')['chiffres_daffaires'].sum().sort_values(ascending=False)

# Création d'une palette de couleurs dégradée
gradient_colors = ['#FF5733', '#FF6F33', '#FF8B33', '#FFA633', '#FFC233', '#FFDD33', '#FFFF33', '#DDFF33', '#BFFF33', '#9BFF33']

# Calcul du nombre de mois et ajustement de la liste de couleurs
num_months = len(chiffra_affaire_par_mois)
adjusted_colors = [gradient_colors[i % len(gradient_colors)] for i in range(num_months)]

# Création du graphique à barres avec une palette de couleurs dégradée
fig1 = go.Figure()
for month, revenue, color in zip(chiffra_affaire_par_mois.index, chiffra_affaire_par_mois.values, adjusted_colors):
    fig1.add_trace(go.Bar(
        x=[month],
        y=[revenue],
        marker=dict(color=color),
        name=month
    ))

# Ajout des titres et des étiquettes d'axe
fig1.update_layout(
    title="Chiffre d'affaire par Mois",
    xaxis_title="Mois",
    yaxis_title="Chiffres d'affaires"
)

# SALES BY Ville [BAR CHART] FIG2
# Groupement des données par ville et calcul du chiffre d'affaires total
chiffra_affaire_par_ville = df_selection.groupby('ville')['chiffres_daffaires'].sum().sort_values(ascending = False)
# Création d'une palette de couleurs dégradée
gradient_colors = ['#FF5733', '#FF6F33', '#FF8B33', '#FFA633', '#FFC233', '#FFDD33', '#FFFF33', '#DDFF33', '#BFFF33', '#9BFF33']

# Calcul du nombre de mois et ajustement de la liste de couleurs
num_months = len(chiffra_affaire_par_ville )
adjusted_colors = [gradient_colors[i % len(gradient_colors)] for i in range(num_months)]

# Création du graphique à barres avec une palette de couleurs dégradée
fig2 = go.Figure()
for v, revenue, color in zip(chiffra_affaire_par_ville .index, chiffra_affaire_par_ville.values, adjusted_colors):
    fig2.add_trace(go.Bar(
        x=[v],
        y=[revenue],
        marker=dict(color=color),
        name=v,text=[f'{revenue}'],
        textfont=dict(color=f'{color}'),  # Couleur du texte en blanc
        textangle=0, # Orientation du texte de bas vers le haut
        textposition='outside'  # Positionnement automatique du texte
    ))

# Ajout des titres et des étiquettes d'axe
fig2.update_layout(
    title="Chiffre d'affaire par Ville",
    xaxis_title="Ville",
    yaxis_title="Chiffres d'affaires"
)

######################

viz_gauche , viz_droite = st.columns(2)
viz_gauche.plotly_chart(fig1,use_container_width=True)
viz_droite.plotly_chart(fig2,use_container_width=True)
