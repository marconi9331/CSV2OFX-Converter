import csv

# Ask for user path to a CSV
csv_path = input("Please enter the path to the CSV file: ")

mapFormPag = {"Crédito" : {} , "Débito" : {}}


def mapTipos(tipo):
    if tipo.startswith("Crédito"):
        return "Crédito"
    else:
        return "Débito"

def addTransaction(tipo, bandeira, row):
    if bandeira not in mapFormPag[tipo]:
        mapFormPag[tipo][bandeira] = []
    mapFormPag[tipo][bandeira].append(row)

# Load this CSV using CSV library
with open(csv_path, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=';', quotechar='"', doublequote=True)   
   
    for row in reader:
        tipo = mapTipos(row.get("TIPO"))
        addTransaction(tipo, row.get("BANDEIRA"), row)

    for tipo in mapFormPag:
        for bandeira in mapFormPag[tipo]:
            print(f"Count: {bandeira} - {tipo} - {len(mapFormPag[tipo][bandeira])}")