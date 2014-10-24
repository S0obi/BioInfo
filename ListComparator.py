import csv

class ListComparator:

    def __init__(self, listA, listB, pValLimit, foldCLimit, noteLimit=0):
        self.listA = listA
        self.listB = listB

        if not pValLimit == "":
            self.pValLimit = float(pValLimit)
        else:
            self.pValLimit = None
        
        if not foldCLimit == "":
            self.foldCLimit = int(foldCLimit)
        else:
            self.foldCLimit = None

        if not noteLimit == "":
            self.noteLimit = int(noteLimit)
        else:
            self.noteLimit = 0

    def calculNote (self, row):
        # list type A1
        if row[1] == "x" or row[1] == "-":
            note=0
            for e in row[1:]:
                if e == "x":
                    note += 1

            return str(note)
        # list type A
        else:
            return str(row[-1])

    def getFindDash(self, row):
        findD = row[0].find("-", 8)
        if not findD == -1:
            return findD
        else:
            return None

    def isGreaterthanFoldC(self, row):
        if row == "" or self.foldCLimit is None:
            return True

        try:
            return abs(float(row)) >= self.foldCLimit
        
        except:
            return False

    def isLessThanPValue(self, row):
        if row == "" or self.pValLimit is None:
            return True

        try:
            return float(row) <= self.pValLimit

        except:
            return False

    def getDiffListB(self):
        retComp = []
        with open(self.listB, newline="") as fListB:
            rListB = csv.reader(fListB, delimiter=";")

            rowsB = [row for row in rListB]

            for rowB in rowsB[1:]:
                if self.isGreaterthanFoldC(rowB[1].replace(",", ".")) and self.isLessThanPValue(rowB[2].replace(",", ".")):
                    retComp.append([rowB[0], "", rowB[1], rowB[2]])
        
        return retComp

    def getDiff (self):
        retComp = []
        with open(self.listA, newline="") as fListA, open(self.listB, newline="") as fListB:
            rListA = csv.reader(fListA, delimiter=",")
            rListB = csv.reader(fListB, delimiter=";")

            rowsA = [row for row in rListA]
            rowsB = [row for row in rListB]

            for rowA in rowsA[1:]:
                for rowB in rowsB[1:]:
                    note = self.calculNote(rowA)
                    if (rowA[0][0:self.getFindDash(rowA)] == rowB[0][0:self.getFindDash(rowB)]) and \
                        self.isGreaterthanFoldC(rowB[1].replace(",", ".")) and \
                        self.isLessThanPValue(rowB[2].replace(",", ".")) and int(note) >= self.noteLimit:

                        retComp.append([rowA[0], rowB[0], rowB[1], rowB[2], note])
        return retComp