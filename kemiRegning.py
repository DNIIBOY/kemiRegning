from rich import *
from rich.table import Table
from rich.console import Console
from rich import pretty
from molmass import Formula
import re
from sympy import Matrix, lcm
import os
import sys
import xlsxwriter

fileName = "kemi"
decimals = 4

os.system('mode con: cols=80 lines=15')
pretty.install()
console = Console()


def addToMatrix(element, index, count, side):
    if index == len(elementMatrix):
        elementMatrix.append([])
        for _ in elementList:
            elementMatrix[index].append(0)
    if element not in elementList:
        elementList.append(element)
        for i in range(len(elementMatrix)):
            elementMatrix[i].append(0)
    column = elementList.index(element)
    elementMatrix[index][column] += count * side


def findElements(segment, index, multiplier, side):
    elementsAndNumbers = re.split('([A-Z][a-z]?)', segment)
    i = 0
    while i < len(elementsAndNumbers) - 1:
        i += 1
        if len(elementsAndNumbers[i]) > 0:
            if elementsAndNumbers[i + 1].isdigit():
                count = int(elementsAndNumbers[i + 1]) * multiplier
                addToMatrix(elementsAndNumbers[i], index, count, side)
                i += 1
            else:
                addToMatrix(elementsAndNumbers[i], index, multiplier, side)


def compoundDecipher(compound, index, side):
    segments = re.split('(\([A-Za-z0-9]*\)[0-9]*)', compound)
    for segment in segments:
        if segment.startswith("("):
            segment = re.split('\)([0-9]*)', segment)
            multiplier = int(segment[1])
            segment = segment[0][1:]
        else:
            multiplier = 1
        findElements(segment, index, multiplier, side)


def balance(substancesSym, molMass, substances):
    global console
    console.print("Skal reaktionsskemaet automatisk afstemmes? ([green]j[/green]/[red]n[/red]): ", end="")
    autoBalance = input()
    if autoBalance.lower() == "j":
        global elementMatrix
        for i in range(len(reactants)):
            compoundDecipher(reactants[i], i, 1)
        for i in range(len(products)):
            compoundDecipher(products[i], i + len(reactants), -1)
        elementMatrix = Matrix(elementMatrix)
        elementMatrix = elementMatrix.transpose()
        solution = elementMatrix.nullspace()[0]
        multiple = lcm([val.q for val in solution])
        solution = multiple * solution
        coEffi = solution.tolist()
        return [coEffi[i][0] for i in range(len(reactants))] + [coEffi[i + len(reactants)][0] for i in
                                                                range(len(products))]
    elif autoBalance.lower() == "n":
        console.clear()
        x = Table(show_header=True, header_style="cyan")
        x.add_column("Af: Daniel Nettelfield")
        for i in substancesSym:
            x.add_column(i)
        x.add_row(*(["Molare Masse [g/mol]"] + [str(round(i, decimals)) for i in molMass]))
        x.add_row(*(["Index Værdi"] + [str(i + 1) for i in range(len(substances))]))
        console.print(x)
        return [int(input(f"Indsæt koefficient {i}: ")) for i in range(1, len(substances) + 1)]
    else:
        consider(autoBalance)
        console.print("Ugyldigt input")
        return balance(substancesSym, molMass, substances)


def export(substancesSym, coEffiList, n, molMass, massList, inputIndex):
    try:
        book = xlsxwriter.Workbook(fileName + ".xlsx")
        sheet = book.add_worksheet("Daniels Ting")
        sheet.set_column("A:A", 20)
        col1 = ["Af: Daniel Nettelfield", "Koefficienter", "Stofmængde [mol]", "Molare Masse [g/mol]", "Masse [g]"]
        for i, e in enumerate(col1):
            sheet.write(i, 0, e)

        for x in substancesSym:
            y = substancesSym.index(x)
            z = [x, int(coEffiList[y])]
            for i, e in enumerate(z):
                sheet.write(i, y + 1, e)
            sheet.write(3, y + 1, float(round(molMass[y], decimals)))
            if y == inputIndex - 1:
                sheet.write(4, y + 1, float(round(massList[y], decimals)))
                sheet.write_formula(2, y + 1, f"={chr(y + 66)}5/{chr(y + 66)}4")
            else:
                sheet.write_formula(2, y + 1, f"={chr(y + 66)}2/{chr(inputIndex + 65)}2*{chr(inputIndex + 65)}3")
                sheet.write_formula(4, y + 1, f"={chr(y + 66)}3*{chr(y + 66)}4")

        book.close()
        os.system(f"{fileName}.xlsx")
        input(f"Skema eksporteret til {str(fileName + '.xlsx')}")


    except Exception as e:
        print(f"\nDer skete en fejl", 2 * "\n", e, 2 * "\n",
              "Enter for prøve igen, [blue]c[/blue] for at genstarte programmet", end="", sep="")
        re = input()
        if consider(re) == "c":
            return
        else:
            return export(substancesSym, coEffiList, n, molMass, massList, inputIndex)


def titration():
    try:
        console.clear()
        console.print("Indsæt titrant, husk store og små bogstaver.", "[blue]Titrant: [/blue]", sep="\n", end="")
        titrant = input()
        if consider(titrant) == "c":
            return
        console.print("Indsæt titrator, husk store og små bogstaver.", "[blue]Titrator: [/blue]", sep="\n", end="")
        titrator = input()
        if consider(titrator) == "c":
            return
        console.clear()
        console.print(f"Titrant volumen i [blue]liter[/blue] ([green]{titrant}[/green]): ", end="")
        v_titrant = input()
        if consider(v_titrant) == "c":
            return
        else:
            v_titrant = fixfloat(v_titrant)

        console.print(f"Titrator volumen i [blue]liter[/blue] ([green]{titrator}[/green]): ", end="")
        v_titrator = input()
        if consider(v_titrator) == "c":
            return
        else:
            v_titrator = fixfloat(v_titrator)

        console.print(f"Titrator koncentration i [blue]mol/L[/blue] ([green]{titrator}[/green]): ", end="")
        c_titrator = input()
        if consider(c_titrator) == "c":
            return
        else:
            c_titrator = fixfloat(c_titrator)

        n_tit = c_titrator * v_titrator
        c_titrant = n_tit / v_titrant
        titrationTable(titrant, titrator, v_titrant, v_titrator, float(c_titrant), float(c_titrator), n_tit)

    except ValueError:
        console.print("Skal være et tal, prøv igen")
        input()
        return titration()
    except Exception as e:
        console.print(f"Der skete en fejl", 2 * "\n", e, "\n")
        input("Tryk enter for at prøve igen")


def titrationTable(titrant, titrator, v_titrant, v_titrator, c_titrant, c_titrator, n_tit):
    # print([type(x) for x in [v_titrant, v_titrator, c_titrator, c_titrator, n_tit]])
    v_titrant, v_titrator, c_titrator, c_titrator, n_tit = [round(x, decimals) for x in [v_titrant, v_titrator,
                                                                                         c_titrator, c_titrator, n_tit]]
    titTable = Table(show_header=True, header_style="cyan")
    [titTable.add_column(x) for x in ["Af: Daniel Nettelfield", "Titrator", "Titrant"]]
    titTable.add_row(*(["Stof", str(titrator), str(titrant)]))
    titTable.add_row(*(["Stofmængde \[mol]", str(n_tit), str(n_tit)]))
    titTable.add_row(*(["Volumen \[L]", str(v_titrator), str(v_titrant)]))
    titTable.add_row(*(["Koncentration \[mol/L]", str(c_titrator), str(c_titrant)]))
    console.clear()
    console.print(titTable)
    option = input("\nTast (e) for at eksportere. Tryk enter for at starte igen: ")
    consider(option)
    if option.lower() == "e":
        return exportTitration(titrant, titrator, v_titrant, v_titrator, c_titrator)


def exportTitration(titrant, titrator, v_titrant, v_titrator , c_titrator):
    try:
        book = xlsxwriter.Workbook(fileName + ".xlsx")
        sheet = book.add_worksheet("Titrering")
        sheet.set_column("A:A", 24)
        col1 = ["Af: Daniel Nettelfield", "Stof", "Stofmængde [mol]", "Volumen [L]", "Koncentration [mol/L]"]
        for y, x in enumerate(col1):
            sheet.write(y, 0, x)

        for y, x in enumerate(["Titrator", titrator, "=B5*B4", v_titrator, c_titrator]):
            sheet.write(y, 1, x)

        for y, x in enumerate(["Titrant", titrant, "=B3", v_titrant, "=C3/C4"]):
            sheet.write(y, 2, x)

        book.close()
        os.system(f"{fileName}.xlsx")
        input(f"Skema eksporteret til {str(fileName + '.xlsx')}")

    except Exception as e:
        print(f"\nDer skete en fejl", 2 * "\n", e, 2 * "\n",
              "Enter for prøve igen, [blue]c[/blue] for at genstarte programmet", end="", sep="")
        re = input()
        if consider(re) == "c":
            return
        else:
            return exportTitration(titrant, titrator, v_titrant, v_titrator, c_titrator)


def molarTable(subs):
    console.clear()
    x = Table(show_header=True, header_style="cyan")
    x.add_column("Af: Daniel Nettelfield")
    [x.add_column(i) for i in reactants]
    x.add_row(*(["Molarmasse"] + [str(round(Formula(i).mass, decimals)) for i in subs]))
    console.print(x)
    consider(input("Tryk enter for at starte igen: "))


def fixfloat(num):
    if "," in num:
        num = float(num.replace(",", "."))
    else:
        num = eval(num)
    return float(num)


def consider(inp):
    inp = inp.lower()
    if inp == "q":
        console.clear()
        sys.exit()
    elif inp == "c":
        return "c"


if __name__ == "__main__":
    while True:
        console.clear()
        try:
            elementList = []
            elementMatrix = []
            console.print("Indsæt reaktanter, husk store og små bogstaver og ingen koefficienter.",
                          "[blue]Reaktanter: [/blue]", sep="\n", end="")
            reactants = input()
            if consider(reactants) == "c":
                continue
            elif reactants == "t":
                titration()
                continue
            console.print("Indsæt Produkter, husk store og små bogstaver og ingen koefficienter.",
                          "[blue]Produkter: [/blue]", sep="\n", end="")
            products = input()

            if consider(products) == "c":
                continue

            elif products == "":
                reactants = reactants.replace(' ', '').split("+")
                molarTable(reactants)
                continue

            reactants = reactants.replace(' ', '').split("+")
            products = products.replace(' ', '').split("+")
            substancesSym = ["+ " + i if reactants.index(i) != 0 else i for i in reactants] + [
                "+ " + x if products.index(x) != 0 else "-> " + x for x in products]

            substances = reactants + products
            molMass = [Formula(x).mass for x in substances]

            coEffiList = balance(substancesSym, molMass, substances)

            x = Table(show_header=True, header_style="cyan")
            x.add_column("Af: Daniel Nettelfield")
            [x.add_column(i) for i in substancesSym]
            x.add_row(*(["Koefficient"] + [str(i) for i in coEffiList]))
            x.add_row(*(["Molarmasse [g/mol]"] + [str(round(i, decimals)) for i in molMass]))
            x.add_row(*(["Index Værdi"] + [str(i + 1) for i in range(len(substances))]))

            console.clear()
            console.print(x)

            knownMassIndex = input("Indsæt index værdi af stoffet med en kendt masse: ")
            if consider(knownMassIndex) == "c":
                continue

            knownMassIndex = int(knownMassIndex) - 1
            knownMass = input(f"Hvad er massen af {substances[knownMassIndex]} i gram?: ")
            if consider(knownMass) == "c":
                continue

            knownMass = fixfloat(knownMass)

            oneKnownMol = knownMass / molMass[knownMassIndex] / coEffiList[knownMassIndex]

            calcSub = substances.pop(knownMassIndex)
            calcCoEffi = coEffiList.pop(knownMassIndex)
            calcMolMass = molMass.pop(knownMassIndex)

            n = [sub * oneKnownMol for sub in coEffiList]
            massList = [n[i] * molMass[i] for i in range(len(substances))]

            substances.insert(knownMassIndex, calcSub)
            coEffiList.insert(knownMassIndex, calcCoEffi)
            molMass.insert(knownMassIndex, calcMolMass)
            massList.insert(knownMassIndex, knownMass)
            n.insert(knownMassIndex, knownMass / molMass[knownMassIndex])

            x = Table(show_header=True, header_style="cyan")
            x.add_column("Af: Daniel Nettelfield")
            [x.add_column(i) for i in substancesSym]
            x.add_row(*(["Koefficient"] + [str(i) for i in coEffiList]))
            x.add_row(*(["Stofmængde \[mol]"] + [str(round(i, decimals)) for i in n]))
            x.add_row(*(["Molarmasse \[g/mol]"] + [str(round(i, decimals)) for i in molMass]))
            x.add_row(*(["Masse \[g]"] + [str(round(i, decimals)) for i in massList]))

            console.clear()
            console.print(x)

            option = input("\nTast (e) for at eksportere. Tryk enter for at starte igen: ")
            if consider(option) == "c":
                continue
            elif option.lower() == "e":
                export(substancesSym, coEffiList, n, molMass, massList, knownMassIndex + 1)

        except Exception as e:
            console.print(f"Der skete en fejl", 2 * "\n", e, "\n")
            input("Tryk enter for at prøve igen")
