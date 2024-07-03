import itertools as it

from meza.io import read_csv, IterStringIO
from csv2ofx import utils
from csv2ofx.ofx import OFX
#from csv2ofx.mappings.stone import mapping
from decimal import Decimal
from operator import itemgetter


Stone_mapping = {
    "has_header": True,
    "is_split": False,
    "bank": "Stone",
    "currency": "BRL",
    "delimiter": ";",
    "account": itemgetter("BANDEIRA"),
    #"account_id": itemgetter("Field"),
    "date": itemgetter("DATA DE VENCIMENTO"),
    #"type": itemgetter("TIPO"),
    "amount": itemgetter("VALOR LÍQUIDO"),
    #"balance": itemgetter("Field"),
    "desc": itemgetter("DESCONTO DE MDR"),
    "payee": itemgetter("BANDEIRA"),
    "notes": itemgetter("N° CARTÃO"),
    #"class": itemgetter("Field"),
    "id": itemgetter("STONE ID"),
    #"check_num": itemgetter("Field"),
}

def value_formatting(value):
    """
    This function is used to format the amoounts to replace the comma with a dot.
    """	
    return value.replace(",", ".")

def round_amount(amount, decimals):
    """
    This function is used to round the amount to the number of decimals informed.
    """
    return f'{float(value_formatting(amount)):.{decimals}f}'

def records_fix(records):
    fixed_records = []
    for record in records:
        record["VALOR LÍQUIDO"] = round_amount(record["VALOR LÍQUIDO"], 2) 
        fixed_records.append(record)
    return fixed_records

    
#csv_path = input("Please enter the path to the CSV file: ")
ofx = OFX(Stone_mapping)
records = read_csv(r"202406_Stone_Recebimentos_parcial_DEBITO.csv", has_header=True, delimiter=";")

    
groups = ofx.gen_groups(records_fix(records))
trxns = ofx.gen_trxns(groups)
cleaned_trxns = ofx.clean_trxns(trxns)
data = utils.gen_data(cleaned_trxns)
content = it.chain([ofx.header(), ofx.gen_body(data), ofx.footer()])

with open(r"teste.ofx", "wb") as f:
    for line in IterStringIO(content):
        f.write(line)

for line in IterStringIO(content):
    print(line)

print("done...")