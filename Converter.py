import csv

# Ask for user path to a CSV
csv_path = input("Please enter the path to the CSV file: ")

# Load this CSV using CSV library
with open(csv_path, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=';', quotechar='"', doublequote=True)
    for fieldname in reader.fieldnames:
        print(fieldname)
    
    # Find header with text "BANDEIRA"
    if "BANDEIRA" in reader.fieldnames:
        print("Header 'BANDEIRA' found.")
    else:
        print("Header 'BANDEIRA' not found.")
    
    # Find header "TIPO"
    if "TIPO" in reader.fieldnames:
        print("Header 'TIPO' found.")
    else:
        print("Header 'TIPO' not found.")