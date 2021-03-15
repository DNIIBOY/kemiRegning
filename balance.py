import re
from sympy import Matrix, lcm


def addToMatrix(element, index, count, side, elementMatrix, elementList):
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


def findElements(segment, index, multiplier, side, elementMatrix, elementList):
    elementsAndNumbers = re.split('([A-Z][a-z]?)', segment)
    i = 0
    while i < len(elementsAndNumbers) - 1:
        i += 1
        if len(elementsAndNumbers[i]) > 0:
            if elementsAndNumbers[i + 1].isdigit():
                count = int(elementsAndNumbers[i + 1]) * multiplier
                addToMatrix(elementsAndNumbers[i], index, count, side, elementMatrix, elementList)
                i += 1
            else:
                addToMatrix(elementsAndNumbers[i], index, multiplier, side, elementMatrix, elementList)


def compoundDecipher(compound, index, side, elementMatrix, elementList):
    segments = re.split('(\([A-Za-z0-9]*\)[0-9]*)', compound)
    for segment in segments:
        if segment.startswith("("):
            segment = re.split('\)([0-9]*)', segment)
            multiplier = int(segment[1])
            segment = segment[0][1:]
        else:
            multiplier = 1
        findElements(segment, index, multiplier, side, elementMatrix, elementList)


def balance(reactants, products):
    global console
    elementMatrix, elementList = [], []
    for i in range(len(reactants)):
        compoundDecipher(reactants[i], i, 1, elementMatrix, elementList)
    for i in range(len(products)):
        compoundDecipher(products[i], i + len(reactants), -1, elementMatrix, elementList)
    elementMatrix = Matrix(elementMatrix)
    elementMatrix = elementMatrix.transpose()
    solution = elementMatrix.nullspace()[0]
    multiple = lcm([val.q for val in solution])
    solution = multiple * solution
    coEffi = solution.tolist()
    return [coEffi[i][0] for i in range(len(reactants))] + [coEffi[i + len(reactants)][0] for i in range(len(products))]


