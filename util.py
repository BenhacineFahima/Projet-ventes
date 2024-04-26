import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def Show_Sales_by(df_s,axe):
    #################
    # SALES BY MONTH
    # Groupement des données par mois et calcul du chiffre d'affaires total
    chiffra_affaire_par_mois = df_s.groupby('Mois_Fr')[f'{axe}'].sum().sort_values(ascending=False)

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
        title=f"{axe} par Mois",
        xaxis_title="Mois",
        yaxis_title=f"{axe}"
    )

    # SALES BY Ville [BAR CHART]
    # Groupement des données par ville et calcul du chiffre d'affaires total
    chiffra_affaire_par_ville = df_s.groupby('ville')[f'{axe}'].sum().sort_values(ascending = False)
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
        title=f"{axe} par Ville",
        xaxis_title="Ville",
        yaxis_title=f"{axe}"
    )
    ######################
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig1, use_container_width=True)
    right_column.plotly_chart(fig2, use_container_width=True)
    #


# Fonction pour afficher le graphique de quantité par produit
def show_quantity_chart(df_clean):
    produit_quantitie = df_clean.groupby('Product')['Quantity Ordered'].sum().sort_values(ascending=False)
    gradient_colors = ['#FF5733', '#FF6F33', '#FF8B33', '#FFA633', '#FFC233', '#FFDD33', '#FFFF33', '#DDFF33',
                       '#BFFF33', '#9BFF33']
    num_prod = len(produit_quantitie)
    adjusted_colors = [gradient_colors[i % len(gradient_colors)] for i in range(num_prod)]
    fig = go.Figure()
    for prod, quant, color in zip(produit_quantitie.index, produit_quantitie.values, adjusted_colors):
        fig.add_trace(go.Bar(
            x=[prod],
            y=[quant],
            marker=dict(color=color),
            name=prod
        ))
    fig.update_layout(
        title="Quantité par Produit",
        xaxis_title="Produit",
        yaxis_title="Quantité"
    )
    st.plotly_chart(fig,use_container_width=True)

# Fonction pour afficher le graphique de chiffre d'affaires par produit
def show_revenue_chart(df_clean):
    produit_chiffre = df_clean.groupby('Product')['chiffres_daffaires'].sum().sort_values(ascending=False)
    gradient_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                       '#bcbd22', '#17becf']
    num_prod = len(produit_chiffre)
    adjusted_colors = [gradient_colors[i % len(gradient_colors)] for i in range(num_prod)]
    fig = go.Figure()
    for prod, quant, color in zip(produit_chiffre.index, produit_chiffre.values, adjusted_colors):
        fig.add_trace(go.Bar(
            x=[prod],
            y=[quant],
            marker=dict(color=color),
            name=prod
        ))
    fig.update_layout(
        title="Chiffres d'affaires par Produit",
        xaxis_title="Produit",
        yaxis_title="Chiffres d'affaire"
    )
    st.plotly_chart(fig,use_container_width=True)






