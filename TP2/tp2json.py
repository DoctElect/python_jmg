"""
    Matthéo FERTE
    CIPA5 - Jean Marie GUYADER
"""

import folium
import requests
import json
from datetime import datetime

url = 'https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/tco-parcsrelais-star-etat-tr/records?limit=20'
data = requests.get(url).json()

def get_color(fillrate):
    """Fonction permettant de renvoyer une couleur entre le vert et le rouge en fontion d'un fillrate
    Args:
        fillrate (pourcentage): pourcentage du fillrate
    Returns:
        string: chaine couleur
    """
    if not (0 <= fillrate <= 100):
        raise ValueError("fillrate must be between 0 and 100")

    if fillrate <= 33:
        return "green"
    elif fillrate <= 66:
        return "yellow"
    else:
        return "red"

def getDateElementsWithDatetime(dateString):  
    """Focntion pour récupérer les information sur une date
    Args:
        dateString (string): chaine ISO d'une date

    Returns:
        Object: éléments d'une date dans un date_object
    """
    date_object = datetime.fromisoformat(dateString)
    return date_object

def getParkInformationWithJSON(apiJSON):
    """Fonction pour récupérer les informations de chaque parking 

    Args:
        apiJSON (JSON): string JSON issue du GET de l'API

    Returns:
        dictionary: dictionnaire contenant les informations sur chaque parking
    """
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

dico = getParkInformationWithJSON(data)
#print(json.dumps((dico), indent=4, ensure_ascii=False))

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
    # print(100*tx)
    #print(str)
    folium.Circle(
        location=[valeur["lat"], valeur["lon"]],
        radius=tx*radius,
        fill=True,
        tooltip=cle,
        popup=folium.Popup(str),
        color=get_color(tx*100),
        opacity=1,
    ).add_to(m)


# Enregistrer la carte
m.save("TP2/carte2.html")