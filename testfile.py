from rich import *
from rich.console import Console
from rich import pretty
from molmass import Formula
import os
import sys
from balance import balance
from tables import titrationTable, molarTable, manualBalance, indexTable, substanceTable
from exports import export, exportTitration


fileName = "kemi"
decimals = 4

os.system('mode con: cols=80 lines=15')
pretty.install()
console = Console()


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
        titTable = titrationTable(titrant, titrator, v_titrant, v_titrator, float(c_titrant), float(c_titrator), n_tit)
        console.clear()
        console.print(titTable)
        option = input("\nTast (e) for at eksportere. Tryk enter for at starte igen: ")
        consider(option)
        if option.lower() == "e":
            return exportTitration(titrant, titrator, v_titrant, v_titrator, c_titrator)

    except ValueError:
        console.print("Skal være et tal, prøv igen")
        input()
        return titration()
    except Exception as e:
        console.print(f"Der skete en fejl", 2 * "\n", e, "\n")
        input("Tryk enter for at prøve igen")


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
                mTable = molarTable(reactants)
                console.clear()
                console.print(mTable)
                consider(input("Tryk enter for at starte igen: "))
                continue

            reactants = reactants.replace(' ', '').split("+")
            products = products.replace(' ', '').split("+")
            substancesSym = ["+ " + i if reactants.index(i) != 0 else i for i in reactants] + [
                "+ " + x if products.index(x) != 0 else "-> " + x for x in products]

            substances = reactants + products
            molMass = [Formula(x).mass for x in substances]

            console.print("Skal reaktionsskemaet automatisk afstemmes? ([green]j[/green]/[red]n[/red]): ", end="")
            autoBalance = input()
            if autoBalance.lower() == "j":

                coEffiList = balance(reactants, products)

            elif autoBalance.lower() == "n":
                manualTable = manualBalance(substancesSym, molMass)
                console.clear()
                console.print(manualTable)
                coEffiList = [int(input(f"Indsæt koefficient {i}: ")) for i in range(1, len(substances) + 1)]

            else:
                consider(autoBalance)
                console.print("Ugyldigt input")
                continue

            console.clear()
            table = indexTable(substancesSym, coEffiList, molMass)
            console.print(table)

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

            console.clear()
            table = substanceTable(substancesSym, coEffiList, n, molMass, massList)
            console.print(table)

            option = input("\nTast (e) for at eksportere. Tryk enter for at starte igen: ")
            if consider(option) == "c":
                continue
            elif option.lower() == "e":
                export(substancesSym, coEffiList, n, molMass, massList, knownMassIndex + 1)

        except Exception as e:
            console.print(f"Der skete en fejl", 2 * "\n", e, "\n")
            input("Tryk enter for at prøve igen")
