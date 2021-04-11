from rich.table import Table
from molmass import Formula

decimals = 4

subscripts = {
        "0": "\u2080",
        "1": "\u2081",
        "2": "\u2082",
        "3": "\u2083",
        "4": "\u2084",
        "5": "\u2085",
        "6": "\u2086",
        "7": "\u2087",
        "8": "\u2088",
        "9": "\u2089"
    }

def subscripter(subs):
    global subscripts
    for z, x in enumerate(subs):
        for y in x:
            if y.isnumeric():
                try:
                    subs[z] = subs[z].replace(y, subscripts[y])
                except:
                    pass
    return subs

def indexTable(substancesSym, coEffiList, molMass):
    table = Table(show_header=True, header_style="cyan")
    table.add_column("Af: Daniel Nettelfield")
    [table.add_column(i) for i in subscripter(substancesSym)]
    table.add_row(*(["Koefficient"] + [str(i) for i in coEffiList]))
    table.add_row(*(["Molarmasse [g/mol]"] + [str(round(i, decimals)) for i in molMass]))
    table.add_row(*(["Index Værdi"] + [str(i + 1) for i in range(len(substancesSym))]))
    return table


def substanceTable(substancesSym, coEffiList, n, molMass, massList):
    table = Table(show_header=True, header_style="cyan")
    table.add_column("Af: Daniel Nettelfield")
    print(substancesSym)
    [table.add_column(i) for i in subscripter(substancesSym)]
    table.add_row(*(["Koefficient"] + [str(i) for i in coEffiList]))
    table.add_row(*(["Stofmængde \[mol]"] + [str(round(i, decimals)) for i in n]))
    table.add_row(*(["Molarmasse \[g/mol]"] + [str(round(i, decimals)) for i in molMass]))
    table.add_row(*(["Masse \[g]"] + [str(round(i, decimals)) for i in massList]))
    return table


def titrationTable(titrant, titrator, v_titrant, v_titrator, c_titrant, c_titrator, n_tit):
    v_titrant, v_titrator, c_titrator, c_titrator, n_tit = [round(x, decimals) for x in [v_titrant, v_titrator,
                                                                                         c_titrator, c_titrator, n_tit]]
    titTable = Table(show_header=True, header_style="cyan")
    [titTable.add_column(x) for x in ["Af: Daniel Nettelfield", "Titrator", "Titrant"]]
    titTable.add_row(*(["Stof", str(titrator), str(titrant)]))
    titTable.add_row(*(["Stofmængde \[mol]", str(n_tit), str(n_tit)]))
    titTable.add_row(*(["Volumen \[L]", str(v_titrator), str(v_titrant)]))
    titTable.add_row(*(["Koncentration \[mol/L]", str(c_titrator), str(c_titrant)]))
    return titTable


def molarTable(subs):
    mTable = Table(show_header=True, header_style="cyan")
    mTable.add_column("Af: Daniel Nettelfield")
    [mTable.add_column(i) for i in subscripter(subs)]
    mTable.add_row(*(["Molarmasse"] + [str(round(Formula(i).mass, decimals)) for i in subs]))
    return mTable


def manualBalance(substancesSym, molMass):
    balanceTable = Table(show_header=True, header_style="cyan")
    balanceTable.add_column("Af: Daniel Nettelfield")
    for i in subscripter(substancesSym):
        balanceTable.add_column(i)
    balanceTable.add_row(*(["Molare Masse [g/mol]"] + [str(round(i, decimals)) for i in molMass]))
    balanceTable.add_row(*(["Index Værdi"] + [str(i + 1) for i in range(len(substancesSym))]))
    return balanceTable