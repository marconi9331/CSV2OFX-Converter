import itertools as it

from meza.io import read_csv, IterStringIO
from csv2ofx import utils
from csv2ofx.ofx import OFX
from csv2ofx.mappings.stone import mapping
from decimal import Decimal
from operator import itemgetter

Stone_mapping = {
    #"has_header": True,
    #"is_split": False,
    #"currency": "BRL",
    #"delimiter": ";",
    "account": itemgetter("BANDEIRA"),
    "date": itemgetter("DATA DE VENCIMENTO"),
    "amount": itemgetter("VALOR LÍQUIDO")    
    }


def round_amount(amount, decimals):
    return f'{float(amount.replace(",", ".")):.{decimals}f}'.replace(".", ",")

#csv_path = input("Please enter the path to the CSV file: ")
ofx = OFX(Stone_mapping)
records = read_csv(r"C:\teste.csv", has_header=True, delimiter=";")

for record in records:
    record["VALOR LÍQUIDO"] = round_amount(record["VALOR LÍQUIDO"], 2)    
    print(f'{record["DATA DE VENCIMENTO"]}, {record["VALOR LÍQUIDO"]}, {record["BANDEIRA"]}')

    
groups = ofx.gen_groups(records)
trxns = ofx.gen_trxns(groups)
cleaned_trxns = ofx.clean_trxns(trxns)
data = utils.gen_data(cleaned_trxns)
content = it.chain([ofx.header(), ofx.gen_body(data), ofx.footer()])

#with open(r"C:\Users\marco\Downloads\teste.ofx", "w") as f:
#    for line in IterStringIO(content):
#        f.write(line.__str__())

for line in IterStringIO(content):
    print(line)