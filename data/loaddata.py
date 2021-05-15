import pandas as pd

from sqlalchemy import create_engine

ENGINE = engine = create_engine('mysql://emautilisateur:By5hYFfky9CPN@J@db4free.net/emaappilis') #Connexion à la base de données
size=pd.read_sql_query("SHOW TABLES",ENGINE) #Nombre de tables dans la base de données

data=[]

#Récuperer les tables de la base de données et les enregistrer en dataframe
for i in range(0,len(size)):
    dfz = pd.read_sql_query(
        "SELECT * FROM data%s" % (i),
        ENGINE
    )
    dfz = dfz.drop(["index"], axis=1)
    data.append(dfz)
    print("Chargement data%s" % (i))