from rich import *
from rich.console import Console
from rich import pretty
from molmass import Formula
import os
import sys
from balance import balance
import tables
import exports


fileName = "kemi"
decimals = 4

os.system('mode con: cols=80 lines=15')
pretty.install()
console = Console()


class Reaction:
    def __init__(self, reactants, products):
        self.reactants = str(reactants).replace(' ', '').split("+")
        if products:
            self.products = products.replace(' ', '').split("+")
            self.substances = self.reactants + self.products
            self.substancesSym = ["+ " + i if self.reactants.index(i) != 0 else i for i in self.reactants] + [
                "+ " + x if self.products.index(x) != 0 else "-> " + x for x in self.products]
            self.molMass = [Formula(x).mass for x in self.substances]
            self.coEffiList, self.n, self.massList, self.inputIndex = [], [], [], 0

    def balance(self, coEfs=()):
        if len(coEfs) == 0:
            self.coEffiList = balance(self.reactants, self.products)
        else:
            self.coEffiList = [x for x in coEfs]
        return self.coEffiList

    def calculate(self, knownMassIndex, knownMass):
        substances = self.substances
        molMass = self.molMass
        coEffiList = self.coEffiList
        oneKnownMol = knownMass / molMass[knownMassIndex] / coEffiList[knownMassIndex]
        self.n = [sub * oneKnownMol for sub in coEffiList]
        self.massList = [self.n[i] * molMass[i] for i in range(len(substances))]
        self.massList[knownMassIndex] = knownMass
        self.inputIndex = knownMassIndex + 1

    def createManualBalanceTable(self):
        self.manualBalanceTable = tables.manualBalance(self.substancesSym, self.molMass)
        return self.manualBalanceTable

    def createIndexTable(self):
        self.indexTable = tables.indexTable(self.substancesSym, self.coEffiList, self.molMass)
        return self.indexTable

    def createSubstanceTable(self):
        self.subTable = tables.substanceTable(self.substancesSym, self.coEffiList, self.n, self.molMass, self.massList)
        return self.subTable

    def createMolarTable(self):
        self.molarTable = tables.molarTable(self.reactants)
        return self.molarTable

    def roundAll(self, deci):
        self.molMass = [round(x, deci) for x in self.molMass]
        if self.n:
            self.n = [round(x, deci) for x in self.n]
            self.massList = [round(x, deci) for x in self.massList]

    def exportSubstance(self):
        exports.export(self.substancesSym, self.coEffiList, self.n, self.molMass, self.massList, self.inputIndex)


class Titration:
    def __init__(self, titrant, titrator, v_titrant, v_titrator, c_titrator):
        self.titrant = titrant
        self.titrator = titrator
        self.v_titrant = v_titrant
        self.v_titrator = v_titrator
        self.c_titrator = c_titrator
        self.n_tit = self.c_titrator * self.v_titrator
        self.c_titrant = self.n_tit / v_titrant

    def roundAll(self, deci):
        self.v_titrant = round(self.v_titrant, deci)
        self.v_titrator = round(self.v_titrator, deci)
        self.c_titrator = round(self.c_titrator, deci)
        self.n_tit = round(self.n_tit, deci)
        self.c_titrant = round(self.c_titrant, deci)

    def createTable(self):
        self.titTable = tables.titrationTable(self.titrant, self.titrator, self.v_titrant, self.v_titrator,
                                              self.c_titrant, self.c_titrator, self.n_tit)
        return self.titTable

    def export(self):
        exports.exportTitration(self.titrant, self.titrator, self.v_titrant, self.v_titrator, self.c_titrator)


def titration():
    try:
        console.clear()
        console.print("Indsæt titrant, husk store og små bogstaver.", "[blue]Titrant: [/blue]", sep="\n", end="")
        titrant = consider(input())
        console.print("Indsæt titrator, husk store og små bogstaver.", "[blue]Titrator: [/blue]", sep="\n", end="")
        titrator = consider(input())
        console.clear()

        console.print(f"Titrant volumen i [blue]liter[/blue] ([green]{titrant}[/green]): ", end="")
        v_titrant = consider(input())
        console.print(f"Titrator volumen i [blue]liter[/blue] ([green]{titrator}[/green]): ", end="")
        v_titrator = consider(input())
        console.print(f"Titrator koncentration i [blue]mol/L[/blue] ([green]{titrator}[/green]): ", end="")
        c_titrator = consider(input())

        tit = Titration(titrant, titrator, v_titrant, v_titrator, c_titrator)
        tit.roundAll(decimals)
        tit.createTable()

        console.clear()
        console.print(tit.titTable)
        option = input("\nTast (e) for at eksportere. Tryk enter for at starte igen: ")
        consider(option)
        if option.lower() == "e":
            return tit.export()

    except ValueError:
        console.print("Skal være et tal, prøv igen")
        input()
        return titration()
    except Exception as e:
        console.print(f"Der skete en fejl", 2 * "\n", e, "\n")
        input("Tryk enter for at prøve igen")

def consider(inp):
    if inp.lower() == "q":
        console.clear()
        sys.exit()
    elif inp.lower() == "c":
        return run()
    else:
        try:
            if "," in inp:
                return float(inp.replace(",", "."))
            elif inp == "":
                return inp
            else:
                return eval(inp)
        except (ValueError, NameError):
            return inp


def run():
    console.clear()
    try:
        console.print("Indsæt reaktanter, husk store og små bogstaver og ingen koefficienter.",
                      "[blue]Reaktanter: [/blue]", sep="\n", end="")
        reactants = consider(input())

        if not reactants:
            return run()
        elif reactants == "t":
            titration()
            return run()
        console.print("Indsæt Produkter, husk store og små bogstaver og ingen koefficienter.",
                      "[blue]Produkter: [/blue]", sep="\n", end="")
        products = consider(input())
        react = Reaction(reactants, products)
        if not products:
            react.createMolarTable()
            console.clear()
            console.print(react.molarTable)
            consider(input("Tryk enter for at starte igen: "))
            return run()

        console.print("Skal reaktionsskemaet automatisk afstemmes? ([green]j[/green]/[red]n[/red]): ", end="")
        autoBalance = consider(input())
        if autoBalance.lower() == "j":
            react.balance()
        elif autoBalance.lower() == "n":
            manualTable = tables.manualBalance(react.substancesSym, react.molMass)
            console.clear()
            console.print(manualTable)
            coEffiList = [int(input(f"Indsæt koefficient {i}: ")) for i in range(1, len(react.substances) + 1)]
            react.balance([coEffiList])
        else:
            console.print("Ugyldigt input")

        print("mojn do")

        react.createIndexTable()
        console.clear()
        console.print(react.indexTable)

        knownMassIndex = int(consider(input("Indsæt index værdi af stoffet med en kendt masse: "))) - 1
        knownMass = consider(input(f"Hvad er massen af {react.substances[knownMassIndex]} i gram?: "))

        react.calculate(knownMassIndex, knownMass)
        react.roundAll(decimals)
        react.createSubstanceTable()

        console.clear()
        console.print(react.subTable)

        option = consider(input("\nTast (e) for at eksportere. Tryk enter for at starte igen: "))
        if option.lower() == "e":
            react.exportSubstance()

        return run()

    except Exception as e:
        console.print(f"Der skete en fejl", 2 * "\n", e, "\n")
        input("Tryk enter for at prøve igen")
        return run()


if __name__ == "__main__":
    run()
