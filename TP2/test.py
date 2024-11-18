import folium
import requests

url = 'https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/tco-parcsrelais-star-etat-tr/records?limit=20'
data = requests.get(url)

def parse_json(text):
    """
    Fonction pour convertir une chaîne JSON en dictionnaire ou liste Python.
    Arguments:
        text (str): Chaîne JSON.
    Retourne:
        dict | list | str | int | float | bool | None: Objet Python correspondant.
    """
    def parse_value(value):
        """Analyse une valeur JSON et la convertit en type Python."""
        value = value.strip()
        if value == "null":
            return None
        elif value == "true":
            return True
        elif value == "false":
            return False
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1].replace('\\"', '"').replace("\\u00e9", "é")  # Gère les chaînes
        elif '.' in value:
            return float(value)  # Convertit en float
        elif value.isdigit():
            return int(value)  # Convertit en int
        else:
            return value

    def parse_object(text):
        """Analyse un objet JSON (entre accolades {})."""
        obj = {}
        text = text.strip()[1:-1]  # Enlève les {}
        items = split_items(text)
        for item in items:
            key, value = item.split(":", 1)
            key = parse_value(key)
            obj[key] = parse_element(value.strip())
        return obj

    def parse_array(text):
        """Analyse un tableau JSON (entre crochets [])."""
        array = []
        text = text.strip()[1:-1]  # Enlève les []
        items = split_items(text)
        for item in items:
            array.append(parse_element(item.strip()))
        return array

    def parse_element(element):
        """Détecte le type d'un élément JSON (objet, tableau ou valeur)."""
        if element.startswith("{") and element.endswith("}"):
            return parse_object(element)
        elif element.startswith("[") and element.endswith("]"):
            return parse_array(element)
        else:
            return parse_value(element)

    def split_items(text):
        """Sépare les éléments d'un objet ou tableau JSON en respectant les guillemets."""
        items = []
        buffer = ""
        in_string = False
        bracket_count = 0
        for char in text:
            if char == '"' and (len(buffer) == 0 or buffer[-1] != "\\"):
                in_string = not in_string
            elif char in "{[" and not in_string:
                bracket_count += 1
            elif char in "]}" and not in_string:
                bracket_count -= 1
            elif char == "," and not in_string and bracket_count == 0:
                items.append(buffer)
                buffer = ""
                continue
            buffer += char
        if buffer:
            items.append(buffer)
        return items

    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return parse_object(text)
    elif text.startswith("[") and text.endswith("]"):
        return parse_array(text)
    else:
        return parse_value(text)


# Exemple d'utilisation
json_text = '''{"total_count": 8, "results": [{"idparc": "CVI", "nom": "Cesson-Viasilva", "coordonnees": {"lon": -1.620879, "lat": 48.13259}, "lastupdate": "2024-11-18T14:15:10+00:00", "capaciteparking": 808, "etatouverture": "OUVERT", "etatremplissage": "LIBRE", "capacitesoliste": 777, "jrdinfosoliste": 136, "capaciteve": 11, "jrdinfoelectrique": 1, "capacitecovoiturage": 0, "jrdinfocovoiturage": 171, "capacitepmr": 17, "jrdinfopmr": 16, "jrdmentionligne1": "OUVERT", "jrdmentionligne2": null}]}'''
result = parse_json(data.text)
print(result)
