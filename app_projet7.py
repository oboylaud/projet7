import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import datetime
import plotly.graph_objects as go
import os

#https://github.com/oboylaud/nprojet7.git

def fig_compteur(proba_def_cust):
    color="gray"
    if proba_def_cust>=50:
        color="red"
    elif (proba_def_cust>=45 and proba_def_cust<50):
        color="orange"
    elif proba_def_cust<45:
        color="green"
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = proba_def_cust,
    mode = "gauge+number",
    title = {'text': "Risque de défaut"},
    gauge = {'axis': {'range': [None, 100]},
             'bar': {'color': color},
             'steps' : [
                 {'range': [0, 45], 'color': "white"},
                 {'range': [45, 50], 'color': "white"},
                 {'range': [50, 100], 'color': "white"}],
             'threshold' : {'line': {'color': color, 'width': 8}, 'thickness': 0.75, 'value': proba_def_cust}}))
    fig.update_layout(autosize=False,width=400, height=400)
    
    return fig

def fig_histo(s_ext1, s_ext2, s_ext3):
    #colors = ["grey", "orange", "green"]
    colors = ["grey", "grey", "grey"]

    fig = go.Figure(data=[go.Bar(
        x=['Source externe 1', 'Source externe 2', 'Source externe 3'],
        y=[s_ext1, s_ext2, s_ext3],
        marker_color=colors
    )])
    fig.update_layout(title=' ',autosize=False,width=500, height=400)
    return fig


def fig_comp(ratio_cust, ratio_comp, indi_rat):
    colors = ["grey", "blue"]
    fig = go.Figure(data=[go.Bar(
        x=['client', 'selection'],
        y=[ratio_cust, ratio_comp],
        marker_color=colors        
    )])
    fig.update_layout(title=indi_rat,autosize=False,width=400, height=400)
    return fig


# About
expander_bar = st.beta_expander("About this app")
expander_bar.markdown("""
* **Projet 7** 
* **Librairies Python utilisées:** pandas, streamlit, numpy, matplotlib, seaborn, time
* **Source des données :** voir note.
""")



# mise en cache du fichier avec les données
@st.cache
def load_data():   
   data = pd.read_csv('df.csv')
   return data

df = load_data()
#df=pd.read_pickle('/home/olivier/Documents/ProjetsOpenclassrooms/Projet7/df.plk')
st.sidebar.header('Identifiant du client')
with st.sidebar.beta_expander("En savoir plus"):
        st.write("""
             Le numéro d'identifiant du client est un numéro unique composé de 6 chiffres.
         """)
id_client = st.sidebar.number_input("SAISIR LE CODE IDENTIFIANT DU CLIENT = ", min_value = 100000, max_value = 999999)
#st.sidebar.write('id_client =', id_client)
#st.dataframe(df) 


df_mask=df['SK_ID_CURR']==id_client
df_cust = df[df_mask]


if df_cust.shape[0] == 0 : 
    st.title("Le N° d'identifiant du client est inconnu")
else : 
    #st.write('client connu') 
    #st.title('Client :')
    #st.title('TABLEAU DE BORD')
    col1, col2 = st.beta_columns(2)
    with col1 :
        st.markdown('# Client n° :')        
    with col2 : 
        st.title(id_client)
        #st.write('type de contrat :')
        #st.header(contract_type)





if df_cust.shape[0] == 1 :
    gender = df_cust.at[df_cust.index[0],'CODE_GENDER']
    family_status = df_cust.at[df_cust.index[0],'NAME_FAMILY_STATUS']
    education_type = df_cust.at[df_cust.index[0],'NAME_EDUCATION_TYPE']
    income_type = df_cust.at[df_cust.index[0],'NAME_INCOME_TYPE']
    occupation_type = df_cust.at[df_cust.index[0],'OCCUPATION_TYPE']
    organization_type = df_cust.at[df_cust.index[0],'ORGANIZATION_TYPE']
    age =  df_cust.at[df_cust.index[0],'APP_NEW_AGE'].round(1)
    tr_age =  df_cust.at[df_cust.index[0],'APP_NEW_AGE_CAT']
    tr_revenu =  df_cust.at[df_cust.index[0],'APP_NEW_INCOME_BAND']
    family_members =  df_cust.at[df_cust.index[0],'CNT_FAM_MEMBERS']
    s_ext1 =  df_cust.at[df_cust.index[0], 'EXT_SOURCE_1']
    s_ext2 = df_cust.at[df_cust.index[0], 'EXT_SOURCE_2']
    s_ext3 = df_cust.at[df_cust.index[0], 'EXT_SOURCE_3']
    proba_def_cust=df_cust.at[df_cust.index[0], 'TARGET_1']*100
    rat1_cust = df_cust['CREDIT_INCOME_PERCENT'].mean()
    rat2_cust = df_cust['ANNUITY_INCOME_PERCENT'].mean()*100
    rat3_cust = df_cust['CREDIT_TERM'].mean()*100
    rat4_cust = df_cust['APP_NEW_CREDIT_GOODS_PRICE_RATIO'].mean()
    if gender =='F' :
        sc = 'Le client est une femme '
    if gender =='M' :
        sc = 'Le client est un homme '
    # st.markdown("Risque de défaut:")
    with st.beta_expander ('Caractéristiques générales') :
        caract_gen = ['CODE_GENDER', 'NAME_FAMILY_STATUS', 'APP_NEW_AGE', 'CNT_FAM_MEMBERS', 'NAME_EDUCATION_TYPE',  'NAME_INCOME_TYPE', 'OCCUPATION_TYPE', 'ORGANIZATION_TYPE']
        carac1 = df_cust[caract_gen]
        carac1.rename(columns={'CODE_GENDER': 'Sexe', 'NAME_FAMILY_STATUS': 'Status', 'APP_NEW_AGE': 'Age', 'CNT_FAM_MEMBERS': 'Taille du foyer','NAME_EDUCATION_TYPE': 'Scolarité', 'NAME_INCOME_TYPE': 'Origine des revenus', 'OCCUPATION_TYPE': 'Profession', 'ORGANIZATION_TYPE': 'Secteur'}, inplace=True)
        carac1['Age']=carac1['Age'].round(1)
        st.table(carac1.T)
        if st.checkbox("Guide de lecture") :
            st.write(sc, family_status, ' de ', age, 'ans. Son foyer est composé de ', family_members, 'personne(s). Ses revenus sont du type ',income_type, '. Il est ', occupation_type, ' dans le secteur', organization_type)
    with st.beta_expander ('Revenus, patrimoine et crédits') :
        caract_fin = ['AMT_INCOME_TOTAL', 'AMT_GOODS_PRICE','AMT_CREDIT', 'AMT_ANNUITY' ]
        carac2 = df_cust[caract_fin]
        carac2.rename(columns={'AMT_INCOME_TOTAL': 'Montant des revenus', 'AMT_GOODS_PRICE': 'Montant du patrimoine', 'AMT_CREDIT': 'Montant du ou des crédits', 'AMT_ANNUITY':'Montant des annuités'}, inplace=True)
        st.table(carac2.T)
        if st.checkbox("Ratios associés") :
            ratio1 = ['CREDIT_INCOME_PERCENT', 'ANNUITY_INCOME_PERCENT', 'CREDIT_TERM', 'APP_NEW_CREDIT_GOODS_PRICE_RATIO']
            carac3 = df_cust[ratio1]
            carac3.rename(columns={'CREDIT_INCOME_PERCENT': 'montant des crédits / revenus', 'ANNUITY_INCOME_PERCENT': 'montant des annuités / revenus', 'CREDIT_TERM': 'Montant des annuités / crédits', 'APP_NEW_CREDIT_GOODS_PRICE_RATIO':'Montant des crédits / patrimoine'}, inplace=True)
            st.table(carac3.T)

        st.write(" ")

    st.markdown("## Risque de défaut et évaluations externes")
    with st.beta_expander("En savoir plus"):
    		st.markdown("Voir la note ")
    col1, col2 = st.beta_columns(2)
    with col1 :
    	fig1=fig_compteur(proba_def_cust)
    	st.plotly_chart(fig1)
    with col2 :
    	fig2=fig_histo(s_ext1, s_ext2, s_ext3)
    	st.write(fig2)
    with col2 :
        if st.checkbox("Précisions sur les sources externes") : 
            st.write("La source externe 1 est.... La source externe 2 est .... Attention 0 signifie que l'évaluation est manquante")	
    #st.write(tr_age)
    #st.write(tr_revenu)
    #st.write(family_members)

    st.sidebar.header('Faire une comparaison')
    with st.sidebar.beta_expander("En savoir plus"):
        st.write("Cliquer sur le bouton 'oui' pour pouvoir comparer la probabilité de défaut du client avec l'ensemble ou une selection de clients")
    compar = st.sidebar.radio("SELECTIONNER",('Non', 'Oui'))
    if compar == 'Oui' :
        st.sidebar.header('Choix des clients pour la comparaison')
        compar1 = st.sidebar.selectbox("SELECTIONNER LE PERIMETRE",('Ensemble des clients', 'Clients similaires', 'Choix libre'))
        if compar1 == "Ensemble des clients" :
            #st.sidebar.header('Ensemble des clients')
            if st.sidebar.button('Cliquer pour valider') :
                df_compar = df
                #st.write(df_compar.head(10))
                st.markdown("## Risque de défaut pour l'ensemble des clients")
                st.write('Nombre de client(s) pris en compte pour la comparaison :', df_compar.shape[0])   
                proba_mean_ens = df_compar['TARGET_1'].mean()*100
                fig4=fig_compteur(proba_mean_ens)
                st.plotly_chart(fig4)
                rat1_comp = df_compar['CREDIT_INCOME_PERCENT'].mean()
                rat2_comp = df_compar['ANNUITY_INCOME_PERCENT'].mean()*100
                rat3_comp = df_compar['CREDIT_TERM'].mean()*100
                rat4_comp = df_compar['APP_NEW_CREDIT_GOODS_PRICE_RATIO'].mean()
                fig_c1 = fig_comp(rat1_cust, rat1_comp,'Crédits/Revenus' )
                fig_c2 = fig_comp(rat2_cust, rat2_comp,'Annuités/Revenus')
                fig_c3 = fig_comp(rat3_cust, rat3_comp,'Annuités/Crédits')
                fig_c4 = fig_comp(rat4_cust, rat4_comp,'Crédits/Patrimoine')
                col1, col2 = st.beta_columns(2)
                with col1 :
                    st.write(fig_c1)
                    st.write(fig_c2)
                with col2 :
                    st.write(fig_c3)
                    st.write(fig_c4)               
                #st.write('ok')                
        if compar1 == "Clients similaires" :
            #st.sidebar.header('Clients similaires pour :')
            st.sidebar.write('Clients similaires pour les critères (cocher les critères)')
            c1 = st.sidebar.checkbox('Même type de revenus')
            c2 = st.sidebar.checkbox('Même tranche des revenus')
            c3 = st.sidebar.checkbox("Même classe d'age")
            c4 = st.sidebar.checkbox('Même éducation')
            c5 = st.sidebar.checkbox('Même profession')
            c6 = st.sidebar.checkbox("Même secteur d'activité")
            if st.sidebar.button('Cliquer pour valider') :
                df_compar = df.copy()
                st.header("Clients avec la ou les même caractéristiques :")
                if c1 :
                    df_compar = df_compar[df_compar['NAME_INCOME_TYPE'] == income_type]
                    st.write('Revenu du type :', income_type)
                if c2 :
                    df_compar = df_compar[df_compar['APP_NEW_INCOME_BAND'] == tr_revenu]
                    if tr_revenu == 1 : 
                        t_revenu = " Revenu inferieur à 30 k "
                    if tr_revenu == 2 :
                        t_revenu = " Revenu compris entre 30 et 65 k "
                    if tr_revenu == 3 : 
                        t_revenu = " Revenu compris entre 65 et 95 k "
                    if tr_revenu == 4 :
                        t_revenu = " Revenu compris entre 95 et 130 k "
                    if tr_revenu == 5 : 
                        t_revenu = " Revenu compris entre 130 et 160 k "
                    if tr_revenu == 6 :
                        t_revenu = " Revenu compris entre 160 et 190 k "
                    if tr_revenu == 7 : 
                        t_revenu = " Revenu compris entre 190 et 220 k "
                    if tr_revenu == 8 :
                        t_revenu = " Revenu compris entre 220  et 275 k "
                    if tr_revenu == 9 : 
                        t_revenu = " Revenu compris entre 275 et 325 k "
                    if tr_revenu == 10 :
                        t_revenu = " Revenus supérieur à 325 k " 
                    st.write(t_revenu)
                if c3 :
                    df_compar = df_compar[df_compar['APP_NEW_AGE_CAT'] == tr_age]
                    st.write("Trange d'age :", tr_age,'ans')
                if c4 :
                    df_compar = df_compar[df_compar['NAME_EDUCATION_TYPE'] == education_type]
                    st.write("Niveau éducation :", education_type)
                if c5 :
                    df_compar = df_compar[df_compar['OCCUPATION_TYPE'] == occupation_type]
                    st.write("Activités :", occupation_type)
                if c6 :
                    df_compar = df_compar[df_compar['ORGANIZATION_TYPE'] == organization_type]
                    st.write("Secteur :", organization_type)
                #st.write(df_compar.head(10))
                st.write('Nombre de client(s) pris en compte pour la comparaison :', df_compar.shape[0])
                if df_compar.shape[0]==0 :
                    st.write('Information pour le client non disponible pour un critère (nan)')
                proba_mean = df_compar['TARGET_1'].mean()*100
                fig3=fig_compteur(proba_mean)
                st.plotly_chart(fig3)
                rat1_comp = df_compar['CREDIT_INCOME_PERCENT'].mean()
                rat2_comp = df_compar['ANNUITY_INCOME_PERCENT'].mean()*100
                rat3_comp = df_compar['CREDIT_TERM'].mean()*100
                rat4_comp = df_compar['APP_NEW_CREDIT_GOODS_PRICE_RATIO'].mean()
                fig_c1 = fig_comp(rat1_cust, rat1_comp,'Crédits/Revenus' )
                fig_c2 = fig_comp(rat2_cust, rat2_comp,'Annuités/Revenus')
                fig_c3 = fig_comp(rat3_cust, rat3_comp,'Annuités/Crédits')
                fig_c4 = fig_comp(rat4_cust, rat4_comp,'Crédits/Patrimoine')
                col1, col2 = st.beta_columns(2)
                with col1 :
                    st.write(fig_c1)
                    st.write(fig_c2)

                with col2 :
                    st.write(fig_c3)
                    st.write(fig_c4)                   
                st.write(' ')
        if compar1 == 'Choix libre' :
            #st.sidebar.header('Libre choix des critères pour la comparaison')
            st.sidebar.write('Choix du ou des critéres')
            df_compar = df
            d1 = st.sidebar.checkbox('Type de revenus')
            if d1 :
                typ_rev = st.sidebar.selectbox('SELECTIONNER LE TYPE DE REVENUS',('Working', 'State servant', 'Commercial associate', 'Pensioner', 'Unemployed', 'Student', 'Businessman', 'Maternity leave'))
            d2 = st.sidebar.checkbox('Revenus')
            if d2 :
                #st.sidebar.write('INTERVALE DES REVENUS')
                rev_min = st.sidebar.number_input("Minimum", min_value=0, value=10000, step=5000)
                rev_max = st.sidebar.number_input("Maximum", min_value=10000, max_value=1000000, value=1000000, step=5000)
                if rev_min > rev_max:
                    st.error("Veuillez saisir une plage valide")
            d3 = st.sidebar.checkbox("Age")
            if d3 :
                age_start, age_end =st.sidebar.slider('AGE : ',0, 100, (20,80))
                st.sidebar.write('Entre ',age_start, ' et ', age_end, ' ans')
                #st.sidebar.write('fin',age_end)
            d4 = st.sidebar.checkbox('Education')
            if d4:
                education_type =st.sidebar.selectbox('SELECTIONNER LE NIVEAU',sorted(df['NAME_EDUCATION_TYPE'].unique()))
            d5 = st.sidebar.checkbox('Secteur')
            if d5 :
                sector = st.sidebar.selectbox('SELECTIONNER LE SECTEUR',(df['ORGANIZATION_TYPE'].unique()))
            d6 = st.sidebar.checkbox("Profession")
            if d6 :
                prof = ['Laborers', 'Core staff', 'Accountants', 'Managers', 'Drivers', 'Sales staff', 'Cleaning staff', 'Cooking staff', 'Private service staff', 'Medicine staff', 'Security staff', 'High skill tech staff', 'Waiters/barmen staff', 'Low-skill Laborers', 'Realty agents', 'Secretaries', 'IT staff', 'HR staff']
                # remarque : la modalité nan n'est pa sreprise dans la liste 
                occ_type = st.sidebar.selectbox("SELECTIONNER LA PROFESSION",sorted(prof))
            d7 = st.sidebar.checkbox('Sexe')
            if d7 :
                gend = ['F', 'M']
                gender = st.sidebar.selectbox('sexe',gend)
            d8 = st.sidebar.checkbox('Etat matrimonial')
            if d8 :
                family_status = st.sidebar.selectbox("SELECTIONNER LE STATUT MATRIMONIAL",df['NAME_FAMILY_STATUS'].unique())
            d9 = st.sidebar.checkbox('Taille du foyer')
            if d9 :
                #family_members = st.sidebar.selectbox("SELECTIONNER LA TAILLE DU FOYER",df['CNT_FAM_MEMBERS'].unique())
                cnt_family_start, cnt_family_end =st.sidebar.slider('Taille : ',1, 22, (1,22))
                st.sidebar.write('Entre ',cnt_family_start, ' et ', cnt_family_end, ' personne(s)')
            if st.sidebar.button('Cliquer pour valider') :
                df_compar = df
                if d1 :
                    df_compar = df_compar[df_compar['NAME_INCOME_TYPE'] == typ_rev]
                if d2 :
                    df_compar = df_compar[(df_compar['AMT_INCOME_TOTAL'] >= rev_min) & (df_compar['AMT_INCOME_TOTAL'] <= rev_max)]
                if d3 :
                    df_compar = df_compar[df_compar['APP_NEW_AGE'] >= age_start]
                    df_compar = df_compar[df_compar['APP_NEW_AGE'] <= age_end]
                if d4 :
                    df_compar = df_compar[df_compar['NAME_EDUCATION_TYPE'] == education_type]
                if d5 :
                    df_compar = df_compar[df_compar['ORGANIZATION_TYPE'] == sector]
                if d6 :
                    df_compar = df_compar[df_compar['OCCUPATION_TYPE'] == occ_type]
                if d7 :
                    df_compar = df_compar[df_compar['CODE_GENDER'] == gender]
                if d8 :
                    df_compar = df_compar[df_compar['NAME_FAMILY_STATUS'] == family_status]
                if d9 :
                    df_compar = df_compar[df_compar['CNT_FAM_MEMBERS'] >= cnt_family_start]
                    df_compar = df_compar[df_compar['CNT_FAM_MEMBERS'] <= cnt_family_end]
                proba_mean = df_compar['TARGET_1'].mean()*100
                st.header("Comparaison avec libre choix des critères ")
                st.write('Nombre de client(s) :', df_compar.shape[0])
                if df_compar.shape[0]==0 :
                    st.write('Attention aucun client')                    
                fig3=fig_compteur(proba_mean)
                st.plotly_chart(fig3)
                rat1_comp = df_compar['CREDIT_INCOME_PERCENT'].mean()
                rat2_comp = df_compar['ANNUITY_INCOME_PERCENT'].mean()*100
                rat3_comp = df_compar['CREDIT_TERM'].mean()*100
                rat4_comp = df_compar['APP_NEW_CREDIT_GOODS_PRICE_RATIO'].mean()
                fig_c1 = fig_comp(rat1_cust, rat1_comp,'Crédits/Revenus' )
                fig_c2 = fig_comp(rat2_cust, rat2_comp,'Annuités/Revenus')
                fig_c3 = fig_comp(rat3_cust, rat3_comp,'Annuités/Crédits')
                fig_c4 = fig_comp(rat4_cust, rat4_comp,'Crédits/Patrimoine')
                col1, col2 = st.beta_columns(2)
                with col1 :
                    st.write(fig_c1)
                    st.write(fig_c2)
                with col2 :
                    st.write(fig_c3)
                    st.write(fig_c4)                   
                st.write('')
            
            st.write('')
    st.write(' ')

            
            
        










