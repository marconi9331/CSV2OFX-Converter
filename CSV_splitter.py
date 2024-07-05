import csv
import os

mapFormPag = {"Crédito" : {} , "Débito" : {}}
test_CSV = r"C:\repos\CSV2OFX Converter\202406_Stone_Recebimentos.csv"

def mapTipos(tipo):
    if tipo.startswith("Crédito"):
        return "Crédito"
    else:
        return "Débito"

def addTransaction(reader):
     for row in reader:
        tipo = mapTipos(row.get("TIPO"))    
        bandeira = row.get("BANDEIRA")
        if bandeira not in mapFormPag[tipo]:
            mapFormPag[tipo][bandeira] = []
        mapFormPag[tipo][bandeira].append(row)


def CSVGenerator(Mapped_CSV):
    CSV_list = []
    for tipo in Mapped_CSV:
        for bandeira in Mapped_CSV[tipo]:
            print(f"{tipo} - {bandeira} Transações listadas: {len(Mapped_CSV[tipo][bandeira])}")
            _fieldnames = Mapped_CSV[tipo][bandeira][0]
            with open(f"{tipo}_{bandeira}.csv", mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file,delimiter=';', quotechar='"', doublequote=True, quoting=csv.QUOTE_ALL)
                writer.writerow(_fieldnames)
                for line in Mapped_CSV[tipo][bandeira]:
                    writer.writerow(line.values())
                csv_tuple = (file.name , tipo, bandeira)
                CSV_list.append(csv_tuple)
    return CSV_list

def CSV_splitter(csv_path):
    with open(csv_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';', quotechar='"', doublequote=True)
        addTransaction(reader)
    
    CSV_list = CSVGenerator(mapFormPag)

    return CSV_list

def CSV_cleaner(processed_CSV):
   
        try:
            os.remove(processed_CSV)
        except OSError:
            pass


#CSV_splitter(test_CSV)