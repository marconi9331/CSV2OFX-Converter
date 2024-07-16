import itertools as it
from meza.io import read_csv, IterStringIO
from csv2ofx import utils
from csv2ofx.ofx import OFX
from CSV_splitter import CSV_splitter as splitter, CSV_cleaner as cleaner
from decimal import Decimal
from operator import itemgetter
from math import floor
from io import StringIO

Stone_mapping = {
    "has_header": True,
    "is_split": False,
    #"bank": "Stone",
    "currency": "BRL",
    "delimiter": ";",
    #"account": itemgetter("BANDEIRA"),
    #"account_id": itemgetter("Field"),
    "date": itemgetter("DATA DE VENCIMENTO"),
    #"type": itemgetter("TIPO"),
    "amount": itemgetter("VALOR LÍQUIDO"),
    #"balance": itemgetter("Field"),
    "desc": itemgetter("N° CARTÃO"),
    "payee": itemgetter("BANDEIRA"),    
    #"notes": itemgetter("N° CARTÃO"),
    #"class": itemgetter("Field"),
    "id": itemgetter("STONE ID"),
    "check_num": itemgetter("STONE ID"),
}

ofx = OFX(Stone_mapping)
#csv_path = input("Please enter the path to the CSV file: ")
csv_path = r"C:\repos\CSV2OFX Converter\202406_Stone_Recebimentos.csv"

def truncate(f, n):
    return floor(f * 10 ** n) / 10 ** n

def value_formatting(value):
    """
    This function is used to format the amoounts to replace the comma with a dot.
    """	
    newvalue = value.replace(".", "")
    return newvalue.replace(",", ".")

def round_amount(amount, decimals):
    """
    This function is used to round the amount to the number of decimals informed.
    """
    return f'{float(value_formatting(amount)):.{decimals}f}'

def records_fix(records):
    fixed_records = []
    for record in records:
        record["VALOR LÍQUIDO"] = str(truncate(float(value_formatting(record["VALOR LÍQUIDO"])), 2)) 
        fixed_records.append(record)
    return fixed_records

def OFX_writer(CSV, tipo, bandeira):
    records = read_csv(CSV, has_header=True, dayfirst=True, delimiter=";")
    records = records_fix(records)
    groups = ofx.gen_groups(records)
    trxns = ofx.gen_trxns(groups)
    cleaned_trxns = ofx.clean_trxns(trxns)
    data = utils.gen_data(cleaned_trxns)
    content = it.chain([ofx.header(), ofx.gen_body(data), ofx.footer()])

    #if bandeira == "AmericanExpress":
    #    print(list(content))
    
    with open(rf"{tipo}_{bandeira}.ofx", "wb") as f:
        for line in IterStringIO(content):                
            f.write(line)   

CSVs_list = splitter(csv_path)

for csv_tuple in CSVs_list:
    OFX_writer(csv_tuple[0], csv_tuple[1], csv_tuple[2])
    #cleaner(csv_tuple[0])

    
print("done...")