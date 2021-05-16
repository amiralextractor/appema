import pandas as pd

####### Téléchargement des données
def download_data():
    url_metadata = "https://www.data.gouv.fr/fr/organizations/sante-publique-france/datasets-resources.csv"
    #url_opencovid = "https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv"
    url_vacsi_a_fra = "https://www.data.gouv.fr/fr/datasets/r/54dd5f8d-1e2e-4ccb-8fb8-eac68245befd"
    url_vacsi_a_dep = "https://www.data.gouv.fr/fr/datasets/r/83cbbdb9-23cb-455e-8231-69fc25d58111"
    
    # On récupère le metadata qui contient tous les liens des données à jours
    df_metadata = pd.read_csv(url_metadata,encoding='utf-8-sig',sep=";")
    print("Chargement de donnees metadata")
    
    # On récupères les liens de toutes les données dans le metadata
    url_data = "https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7"
    url_data_new = "https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c"
    #url_metropoles = df_metadata[df_metadata['url'].str.contains("/sg-metro-opendata")]["url"].max()
    url_incidence = df_metadata[df_metadata['url'].str.contains("/sp-pe-tb-quot")]["url"].values[0]
    url_sursaud = df_metadata[df_metadata['url'].str.contains("sursaud.*quot.*dep")]["url"].values[0]
    print("Chargement des liens du metadata")
    
    # On importe toutes les données qu'on a récupéré du metadata
    df_data=pd.read_csv(url_data,encoding='utf-8-sig',sep=";")
    print("Chargement de data",0)
    
    df_data_new=pd.read_csv(url_data_new,encoding='utf-8-sig',sep=";")
    print("Chargement de data",1)
    
    df_incidence=pd.read_csv(url_incidence,encoding='utf-8-sig',sep=";")
    print("Chargement de data",2)
    
    df_vacsi_a_fra=pd.read_csv(url_vacsi_a_fra,encoding='utf-8-sig',sep=";")
    print("Chargement de data",3)
        
    df_vacsi_a_dep=pd.read_csv(url_vacsi_a_dep,encoding='utf-8-sig',sep=";")
    print("Chargement de data",4)
    
    url_data_covid_syn = "https://www.data.gouv.fr/fr/datasets/r/d3a98a30-893f-47f7-96c5-2f4bcaaa0d71"
    df_data_covid_syn=pd.read_csv(url_data_covid_syn,encoding='utf-8-sig',sep=",")
    print("Chargement de data",5)
    
    df_sursaud=pd.read_csv(url_sursaud,encoding='utf-8-sig',sep=";")
    print("Chargement de data",6)
    
    return df_data, df_data_new, df_incidence, df_vacsi_a_fra, df_vacsi_a_dep, df_data_covid_syn, df_sursaud

data0=download_data()
####### Fin Téléchargement des données

####### Nettoyage des données
def Nettoyage(data):
    datafinal = []
    """
    Données hospitalieres COVID
    Le nombre actuellement hospitalisé... par jour
    """
    df = data[0][["dep","sexe","jour","hosp","rea","rad","dc"]]
    df.columns = ["Departement","Sexe","Date","Hospitalise","Reanime","Gueris","Decede"]
    df["Date"]= pd.to_datetime(df["Date"]).dt.date
    df["Departement"]=df["Departement"].astype(str)
    datafinal.append(df)
    
    """
    Données hospitalieres nouveaux hospitalisés... par jour
    """
    df = data[1]
    df.columns = ["Departement","Date","Nv Hospitalise","Nv Reanime","Nv Decede","Nv Gueris"]
    df["Date"]= pd.to_datetime(df["Date"]).dt.date
    df["Departement"]=df["Departement"].astype(str)
    datafinal.append(df)
    
    """
    Population et nombre positif covid
    Nombre test positif
    Classe age
    """
    df = data[2]
    df.columns = ["Departement","Date","Test Positif","Classe Age","Population"]
    df["Date"]= pd.to_datetime(df["Date"]).dt.date
    df["Departement"]=df["Departement"].astype(str)
    datafinal.append(df)
    
    """
    Data Vaccination
    """
    data = data0
    df = data[3]
    df.columns = ["France","Classe Age","Date","Dose 1","Dose complete","Cumul Dose 1","Cumul complet","Couverture Dose 1","Couverture complete"]
    df["Date"]= pd.to_datetime(df["Date"]).dt.date
    datafinal.append(df)
    
    df = data[4]
    df.columns = ["Departement","Classe Age","Date","Dose 1","Dose complete","Cumul Dose 1","Cumul complet","Couverture Dose 1","Couverture complete"]
    df["Date"]= pd.to_datetime(df["Date"]).dt.date
    df["Departement"]=df["Departement"].astype(str)
    datafinal.append(df)
    
    """
    Data Total
    """
    df = data[5]
    df = df[["date","total_cas_confirmes","total_deces_hopital","total_deces_ehpad","patients_reanimation",
               "patients_hospitalises","total_patients_gueris","nouveaux_patients_hospitalises","nouveaux_patients_reanimation"]]
    df.columns = ["Date","Total Cas","Total Deces","Total Deces Ehpad","Patients Reanimes","Patients Hospitalises",
                  "Patients gueris","Nouveaux hospitalises","Nouveaux Reanimes"]
    df["Date"]= pd.to_datetime(df["Date"]).dt.date
    datafinal.append(df)
    
    """
    Données des urgences
    Total urgence par jour
    Total suspecté Covid par jour
    Total hospitalisé des suspecté Covid par jour
    Classes ages:
        0= Tous les ages
        A= moins de 15 ans
        B= 15-44 ans
        C= 45-64 ans
        D= 65-74 ans
        E= 75 et plus
    On utilise pas mais on garde
    """
    df = data[6]
    df = data[6][["dep","date_de_passage","sursaud_cl_age_corona","nbre_pass_corona",
                  "nbre_pass_tot","nbre_hospit_corona","nbre_pass_corona_h","nbre_pass_corona_f",
                  "nbre_pass_tot_h","nbre_pass_tot_f","nbre_hospit_corona_h","nbre_hospit_corona_f"]]
    df.columns = ["Departement","Date","Classe Age","Suspicion","Urgence","Hospitalisation",
                  "Suspicion Homme","Suspicion Femme","Urgence Homme","Urgence Femme",
                  "Hospitalisation Homme","Hospitalisation Femme"]
    df["Date"]= pd.to_datetime(df["Date"]).dt.date
    df["Departement"]=df["Departement"].astype(str)
    datafinal.append(df)

    print("Nettoyage terminé")
    return datafinal
data=Nettoyage(data0)
####### Fin Nettoyage des données

####### Connexion et mise à jours de la base de données
"""
Cette partie on l'utilise qu'au moment de la mise à jour de la base de donnée
Il est important de la laisser en commentaire pour ne pas écraser les données de la bdd
"""
"""
from sqlalchemy import create_engine

#Pour des raisons de sécurité, pour avoir les indenfitiants, demandez aux auteurs de l'application
host=""
user=""
pswd=""
bdds=""

engine = create_engine('mysql://%s:%s@%s/%s' % (host,user,pswd,bdds))
print("Connexion réussie")

for i in range(0, len(data)):
    dataframe = data[i]
    df = "data%s" % (i)
    dataframe.to_sql(df,con=engine, if_exists='replace')
    print("Mise à jour éfféctuée pour la", df)

print("Fin mise à jour")"""
####### Fin Connexion et mise à jours de la base de données