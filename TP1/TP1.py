def readFile(pathFile):
    fichier = open(pathFile,'r',encoding="utf-8")
    lignes = fichier.readlines()
    fichier.close()
    return lignes

def totalSurface(lignes):
    total = 0
    for ligne in lignes[1:]:
        champ = ligne.strip().split(',')
        try:
            total = total+float(champ[5])
        except:
            print(f"Impossible de convertir en float : {champ[5]}")
    return total

def buildDictionary(lignes):
    dictionnaire = {}
    for ligne in lignes:
        try:
            valeurs = ligne.strip().split(',')
            code_depar = int(valeurs[9].replace('"',''))
            code_postal = int(valeurs[6].replace('"',''))
            gid = valeurs[0]
            surface = float(valeurs[5])

            if code_depar not in dictionnaire:
                dictionnaire[code_depar] = {}
            if code_postal not in dictionnaire[code_depar]:
                dictionnaire[code_depar][code_postal] = {'nomCommune': valeurs[7].replace('"',''), 'tableauParcelles': []}

            dictionnaire[code_depar][code_postal]['tableauParcelles'].append({'idParcelle': int(gid), 'surfaceParcelle': float(surface)})
        except:
            pass

    return dictionnaire

def sommeSurfacesParCommunes(dictionary):
    for code_region, communes in dictionary.items():
        for code_commune, details in communes.items():
            details['surfaceTotalesParcelles'] = 0
            for parcelle in details['tableauParcelles']:
                details['surfaceTotalesParcelles'] = details['surfaceTotalesParcelles'] + parcelle['surfaceParcelle']
    return dictionary

def getCommunePlusDeBioDepartement(dictionary, departementNumber):
    communePlusBio = ('',0)
    for code_region, communes in dictionary.items():
        if(code_region==departementNumber):
            for code_commune, details in communes.items():
                if(communePlusBio[1]<details['surfaceTotalesParcelles']):
                    communePlusBio = (details['nomCommune'],details['surfaceTotalesParcelles'])
                    
    return communePlusBio

def getCommunePlusDeBio(dictionary):
    communePlusBio = ('',0)
    for code_region, communes in dictionary.items():
        for code_commune, details in communes.items():
            if(communePlusBio[1]<details['surfaceTotalesParcelles']):
                communePlusBio = (details['nomCommune'],details['surfaceTotalesParcelles'])
    return communePlusBio

def classementCommunesBio(dictionary):
    list = []
    for code_region, communes in dictionary.items():
        for code_commune, details in communes.items():
            list.append((details['nomCommune'],details['surfaceTotalesParcelles'],code_commune))
    return sorted(list, key=lambda x: x[1],reverse=True)

def writeListToText(myList, filePath):
    file = open(filePath,'a')
    for element in myList:
        file.write(str(element[0])+','+str(element[1])+','+str(element[2])+'\n')
    file.close() 
    
print("[>> Tests liés à la fonction readFile :")
pathFileBretagne5 = "TP1/Bio_BZH.txt"
listeLignes = readFile(pathFileBretagne5)
print(listeLignes)
print(len(listeLignes))
print("*\n")

print("[>> Tests liés à la fonction totalSurface :")
surfaceTotale = totalSurface(listeLignes)
print(surfaceTotale)
print("*\n")

print("[>> Tests liés à la fonction buildDictionary :")
dictionnaire = buildDictionary(listeLignes)
print(dictionnaire)
print("*\n")

print("[>> Tests liés à la fonction sommeSufaceParCommunes :")
dictionnaire = sommeSurfacesParCommunes(dictionnaire)
print(dictionnaire)
print("*\n")

print("[>> Tests liés à la fonction getCommunePlusDeBioDepartement :")
print(getCommunePlusDeBioDepartement(dictionnaire,22))
print("*\n")

print("[>> Tests liés à la fonction getCommunePlusDeBio :")
print(getCommunePlusDeBio(dictionnaire))
print("*\n")

print("[>> Tests liés à la fonction classementCommunesBio :")
classement = classementCommunesBio(dictionnaire)
print(classement)
print("*\n")

print("[>> Tests liés à la fonction writeListToText :")
writeListToText(classement,'TP1/classement.txt')
print("*\n")

