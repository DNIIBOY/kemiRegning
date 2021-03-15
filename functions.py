def consider(inp):
    if inp.lower() == "q":
        console.clear()
        sys.exit()
    elif inp.lower() == "c":
        return run()
    else:
        try:
            if "," in inp:
                inp = float(inp.replace(",", "."))
            else:
                inp = eval(inp)
            return float(inp)
        except ValueError:
            return inp
        except NameError:
            return inp

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


    n_tit = c_titrator * v_titrator
    c_titrant = n_tit / v_titrant
    titTable = titrationTable(titrant, titrator, v_titrant, v_titrator, float(c_titrant), float(c_titrator), n_tit)