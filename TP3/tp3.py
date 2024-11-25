"""
    Matthéo FERTE
    CIPA5 - Jean Marie GUYADER
"""

import folium
import requests
from datetime import datetime,timedelta
import pytz
from flask import Flask, render_template

url = 'https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/tco-parcsrelais-star-etat-tr/records?limit=20'
data = requests.get(url).json()

def get_color(fillrate):
    if not (0 <= fillrate <= 100):
        raise ValueError("fillrate must be between 0 and 100")

    if fillrate <= 33:
        return "green"
    elif fillrate <= 66:
        return "yellow"
    else:
        return "red"

def getDateElementsWithDatetime(dateString):  
    date_object = datetime.fromisoformat(dateString)
    
    # Fuseau horaire pour la France
    paris_tz = pytz.timezone('Europe/Paris')

    # Obtenir la date et l'heure actuelles dans le fuseau horaire de Paris
    now = datetime.now(paris_tz)

    # Vérifier si on est en heure d'été ou d'hiver
    if now.dst() != timedelta(0):
        return date_object
    else:
        return date_object+timedelta(hours=1)
    

def getParkInformationWithJSON(apiJSON):
    dictio = {}
    for parking in apiJSON['results']:
        dictio2 = {}   
        dictio2['heure'] =  getDateElementsWithDatetime(parking['lastupdate']).strftime("%Hh%M")
        dictio2['etat'] = parking['etatouverture']
        dictio2['lon'] = float(parking['coordonnees']['lon'])
        dictio2['lat'] = float(parking['coordonnees']['lat'])
        dictio2['capa'] = int(parking['capacitesoliste'])
        dictio2['capaPMR'] = int(parking['capacitepmr'])
        dictio2['dispo'] = int(parking['jrdinfosoliste'])
        dictio2['dispoPMR'] = int(parking['jrdinfopmr'])
        dictio2['occ']= dictio2['capa'] - dictio2['dispo']
        dictio2['occPMR']= dictio2['capaPMR'] - dictio2['dispoPMR']
        dictio[parking['nom']] = dictio2
    return dictio

app = Flask(__name__)

@app.route('/')
def home():
    dico = getParkInformationWithJSON(data)

    # Créer la carte
    m = folium.Map(location=[48.117102 , -1.677962], zoom_start=13)
    for cle, valeur in dico.items():
        # print(f"{cle}: {valeur}")
        str = f"Individuelles : {valeur['occ']}/{valeur['capa']}\nPMR : {valeur['occPMR']}/{valeur['capaPMR']}\n {valeur['heure']}"
        radius =250
        folium.Circle(
            location=[valeur["lat"], valeur["lon"]],
            radius=radius,
            fill=True,
            tooltip=cle,
            popup=folium.Popup(str),
            opacity=1,
            color="black",
        ).add_to(m)
        tx = (valeur["dispo"]+valeur["dispoPMR"])/(valeur["capa"]+valeur["capaPMR"])
        tx = 1-tx
        folium.Circle(
            location=[valeur["lat"], valeur["lon"]],
            radius=tx*radius,
            fill=True,
            tooltip=cle,
            popup=folium.Popup(str),
            color=get_color(tx*100),
            opacity=1,
        ).add_to(m)
        
    # Sauvegarde de la carte dans un fichier HTML
    m.save("map.html")

    # Render de la carte via un template Flask
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
