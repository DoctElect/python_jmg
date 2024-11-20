"""
    Matthéo FERTE
    CIPA5 - Jean Marie GUYADER
"""

import folium
import requests
import json

url = 'https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/tco-parcsrelais-star-etat-tr/records?limit=20'
data = requests.get(url)



def getColor(fillrate):
    # Calcul des composantes rouge et vert
    red = int(255 * (1 - fillrate))  # Diminue à mesure que le fillrate augmente
    green = int(255 * (fillrate))   # Augmente à mesure que le fillrate augmente
    
    # Couleur en format hexadécimal
    return f'#{red:02x}{green:02x}00'

def get_color(fillrate):
    if not (0 <= fillrate <= 100):
        raise ValueError("fillrate must be between 0 and 100")

    if fillrate <= 33:
        return "green"
    elif fillrate <= 66:
        return "yellow"
    else:
        return "red"

def getDateElements(dateString):
    dict = {}
    dict['annee'] = dateString.split(':')[1][:5]
    dict['mois'] = dateString.split(':')[1][6:8]
    dict['jour'] = dateString.split(':')[1][9:11]
    dict['heure'] = dateString.split(':')[1][12:14]
    dict['minute'] = dateString.split(':')[2]
    return dict
#Test fonction getDateElements
#print(getDateElements('2024-11-18T14:09:00+08:00'))
def getParkInformation(apiString):
    dictio = {}
    data = apiString[32:-3].replace('"',"").split("}, {")
    for elem in data:
        dictio2 = {}
        #print(elem)
        x = elem.split(',')
        nom = x[1].split(':')[1][1:]
        dictio2['heure'] = f"{getDateElements(x[4])['heure']}h{getDateElements(x[4])['minute']}"
        #print(dictio2['heure'])
        dictio2['etat'] = x[6].split(':')[1].replace(' ','')
        dictio2['lon'] = float(x[2].split(':')[2])
        dictio2['lat'] = float(x[3].split(':')[1][:-1])
        dictio2['capa'] = int(x[8].split(':')[1])
        dictio2['capaPMR'] = int(x[14].split(':')[1])
        dictio2['dispo'] = int(x[9].split(':')[1])
        dictio2['dispoPMR'] = int(x[15].split(':')[1])
        dictio2['occ']= int(x[8].split(':')[1])-int(x[9].split(':')[1])
        dictio2['occPMR']= int(x[14].split(':')[1])-int(x[15].split(':')[1])
        dictio[nom]=dictio2
    return dictio

# Affichage formaté avec JSON
#print(json.dumps(getParkInformation(data.text), indent=4, ensure_ascii=False))

dico = getParkInformation(data.text)


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
m.save("TP2/carte.html")