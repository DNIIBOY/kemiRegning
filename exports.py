import xlsxwriter
import os

fileName = "kemi"
decimals = 4

def export(substancesSym, coEffiList, n, molMass, massList, inputIndex):
    try:
        book = xlsxwriter.Workbook(fileName + ".xlsx")
        sheet = book.add_worksheet("Daniels Ting")
        sheet.set_column("A:A", 20)
        col1 = ["Af: Daniel Nettelfield", "Koefficienter", "Stofmængde [mol]", "Molare Masse [g/mol]", "Masse [g]"]
        for i, e in enumerate(col1):
            sheet.write(i, 0, e)

        for y, x in enumerate(substancesSym):
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
              "[blue](P)[/blue] for prøve igen, [blue]enter[/blue] for at genstarte programmet", end="", sep="")
        if input() == "p":
            return export(substancesSym, coEffiList, n, molMass, massList, inputIndex)


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
              "[blue](P)[/blue] for prøve igen, [blue]enter[/blue] for at genstarte programmet", end="", sep="")
        if input() == "p":
            return exportTitration(titrant, titrator, v_titrant, v_titrator, c_titrator)