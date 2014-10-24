import csv

class ListComparator:

    def __init__(self, list1, list2, pValLimit, foldCLimit, noteLimit=0):
        self.list1 = list1
        self.list2 = list2

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

    def getFilterListA(self):
        listToUse = []
        if self.list1 is None and self.list2 is not None:
            listToUse = self.list2
        elif self.list1 is not None and self.list2 is None:
            listToUse = self.list1

        retComp = []
        with open(listToUse, newline="") as flistA:
            rlistA = csv.reader(flistA, delimiter=";")

            rowsA = [row for row in rlistA]

            for rowA in rowsA[1:]:
                note = int(self.calculNote(rowA))
                if note >= self.noteLimit:
                    retComp.append([rowA[0], "", "", "", note])

        return retComp

    def getFilterListB(self):
        listToUse = []
        if self.list1 is None and self.list2 is not None:
            listToUse = self.list2
        elif self.list1 is not None and self.list2 is None:
            listToUse = self.list1

        retComp = []
        with open(listToUse, newline="") as flistB:
            rlistB = csv.reader(flistB, delimiter=";")

            rowsB = [row for row in rlistB]

            for rowB in rowsB[1:]:
                if self.isGreaterthanFoldC(rowB[1].replace(",", ".")) and self.isLessThanPValue(rowB[2].replace(",", ".")):
                    retComp.append([rowB[0], "", rowB[1], rowB[2]])
        
        return retComp

    def getDiffAandB (self):
        retComp = []
        with open(self.list1, newline="") as flist1, open(self.list2, newline="") as flist2:
            rlist1 = csv.reader(flist1, delimiter=";")
            rlist2 = csv.reader(flist2, delimiter=";")

            rowsA = [row for row in rlist1]
            rowsB = [row for row in rlist2]

            for rowA in rowsA[1:]:
                for rowB in rowsB[1:]:
                    note = self.calculNote(rowA)
                    if (rowA[0][0:self.getFindDash(rowA)] == rowB[0][0:self.getFindDash(rowB)]) and \
                        self.isGreaterthanFoldC(rowB[1].replace(",", ".")) and \
                        self.isLessThanPValue(rowB[2].replace(",", ".")) and int(note) >= self.noteLimit:

                        retComp.append([rowA[0], rowB[0], rowB[1], rowB[2], note])
        return retComp

    def getDiffAandA(self):
        retComp = []
        with open(self.list1, newline="") as flist1, open(self.list2, newline="") as flist2:
            rlist1 = csv.reader(flist1, delimiter=";")
            rlist2 = csv.reader(flist2, delimiter=";")

            rowsA = [row for row in rlist1]
            rowsAbis = [row for row in rlist2]

            for rowA in rowsA[1:]:
                for rowAbis in rowsAbis[1:]:
                    note = self.calculNote(rowA)
                    if (rowA[0][0:self.getFindDash(rowA)] == rowAbis[0][0:self.getFindDash(rowAbis)]) and \
                        int(note) >= self.noteLimit:

                        retComp.append([rowA[0], rowAbis[0], "", "", note])
        return retComp

    def getDiffBandB(self):
        retComp = []
        with open(self.list1, newline="") as flist1, open(self.list2, newline="") as flist2:
            rlist1 = csv.reader(flist1, delimiter=";")
            rlist2 = csv.reader(flist2, delimiter=";")

            rowsB = [row for row in rlist1]
            rowsBbis = [row for row in rlist2]

            for rowB in rowsB[1:]:
                for rowBbis in rowsBbis[1:]:
                    if (rowB[0][0:self.getFindDash(rowB)] == rowBbis[0][0:self.getFindDash(rowBbis)]) and \
                        self.isGreaterthanFoldC(rowB[1].replace(",", ".")) and \
                        self.isLessThanPValue(rowB[2].replace(",", ".")):

                        retComp.append([rowB[0], rowBbis[0], rowB[1], rowB[2], ""])
        return retComp

