import csv

class TreeExportator:
    def __init__(self, res, fileCSV):
        self.res = res
        self.fileCSV = fileCSV

    def export(self):
        with open(self.fileCSV, 'w', newline="") as fList:
            writer = csv.writer(fList)
            for e in self.res:
                writer.writerow(e)
