"""
    Matthéo FERTE
    CIPA5 - Jean Marie GUYADER
"""

import folium
import requests

url = 'https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/tco-parcsrelais-star-etat-tr/records?limit=20'
data = requests.get(url)

# Créer la carte
#m = folium.Map(location=[48.8, 2.3])

# Enregistrer la carte
#m.save("carte.html")

def getColor(fillrate):
    # Calcul des composantes rouge et vert
    red = int(255 * (1 - fillrate / 100))  # Diminue à mesure que le fillrate augmente
    green = int(255 * (fillrate / 100))   # Augmente à mesure que le fillrate augmente
    
    # Couleur en format hexadécimal
    return f'#{red:02x}{green:02x}00'

def getDateElements(dateString):
    dict = {}
    dict['annee'] = dateString[:4]
    dict['mois'] = dateString[5:7]
    dict['jour'] = dateString[8:10]
    dict['heure'] = dateString[11:13]
    dict['minute'] = dateString[14:16]
    return dict

def getParkInformation(apiString):
    dict = {}
    apiString
getParkInformation(data.text)