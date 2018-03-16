import csv

def dictparse(csvfilename, keyfield):
    """
    prebere CSV file z imenom csvfilename,
    vrne dict of dicts.
    """
    table = {}
    with open(csvfilename, "rt", newline="") as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   skipinitialspace=True)
        for row in csvreader:
            table[row[keyfield]] = row
            print("vrstica")
    return table

def print_table(table):
    #print out dict_of dictionaries
    print(table)

table = dictparse("urniki_responses_1.csv", "id")
print(table)
