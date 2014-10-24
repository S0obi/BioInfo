from enum import Enum

class ListBioType(Enum):
    TypeA = 1
    TypeB = 2

    def __str__(self):
        if self.value == 1:
            return "Liste miRNA Mediante (A)"
        elif self.value == 2:
            return "Liste miRNA FC/p-val (B)"
        else:
            return "Option not recognized"