import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go
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
        k = st.selectbox("Sélectionnez k :", [ 2, 3])

        # Affichage du résultat
        #if st.button("Afficher les résultats"):
        # Exécution de la fonction mcommon avec la valeur k sélectionnée
        result = mcommon(k)
        # Création d'un DataFrame à partir des résultats
        #df_result = pd.DataFrame(result, columns=["Produits", "Fréquences"])
        # Affichage du DataFrame
        #st.dataframe(df_result,hide_index=True)
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
with st.expander("Data"):
        st.write(df_selection)
st.markdown("""---""")

st.header("Analyse par Mois et Ville")


# Sélection de l'option dans le menu déroulant
option0 = st.selectbox("Choisir une option :", ["Quantité", "Chiffres d'affaires"])

# Affichage du graphique correspondant en fonction de l'option sélectionnée
if option0 == "Quantité":
    Show_Sales_by(df_selection,'Quantity Ordered' )
else:
    Show_Sales_by(df_selection,'chiffres_daffaires' )
#
###########################################
st.header("Analyse par Produit")
df_clean = df_selection.copy()
# Sélection de l'option dans le menu latéral
option = st.selectbox("Choisir une option :", ["Quantité", "Chiffre d'affaires"])

# Affichage du graphique correspondant en fonction de l'option sélectionnée
if option == "Quantité":
    show_quantity_chart(df_clean)
elif option == "Chiffre d'affaires":
    show_revenue_chart(df_clean)
##################################
chiffre_affaire_heure = df_clean.groupby('heure')['chiffres_daffaires'].sum()

# Tri des données par index (heure)
chiffre_affaire_heure = chiffre_affaire_heure.sort_index()

# Création de la trace de ligne avec Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=chiffre_affaire_heure.index, y=chiffre_affaire_heure.values, mode='lines'))

# Ajout de titres et de libellés d'axes
fig.update_layout(
    title="Chiffre d'affaires par heure",
    xaxis_title="Heure",
    yaxis_title="Chiffre d'affaires",
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        #gridcolor='rgba(255,255,255,1)',
        tickmode='array',
        tickvals=list(range(25))  # Positions des ticks de 0 à 24
    )
)


st.plotly_chart(fig, use_container_width=True)