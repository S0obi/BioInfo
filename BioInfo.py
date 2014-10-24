from tkinter import Tk, Text, Frame, Toplevel, LabelFrame, Label, Entry, Button
from tkinter import LEFT, RIGHT, BOTTOM, TOP, VERTICAL, X, Y, INSERT, END, DISABLED, NORMAL, FALSE
from tkinter.ttk import Treeview, Scrollbar
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, showinfo

from ListComparator import ListComparator
from TreeExportator import TreeExportator

class BioInfo(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.wm_title("BioInfo : comparaison des listes")
        self.resizable(width=FALSE, height=FALSE)
        self.SortDir = False

        # Frame content
        self.frameContent = Frame(self)
        self.frameContent.pack(side=TOP, fill=X)

        # ScrollBar
        scrollbar = Scrollbar(self.frameContent, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Result Content
        self.dataCols = ('microArn_A', 'microArn_B', 'FoldC', 'p-Value', 'Note')
        self.tree = Treeview(self.frameContent, columns=self.dataCols, show = 'headings', yscrollcommand=scrollbar.set)

        # configure column headings
        for c in self.dataCols:
            self.tree.heading(c, text=c, command=lambda c=c: self.columnSort(c, self.SortDir))
            self.tree.column(c, width=10)

        self.tree.pack(side=LEFT, fill=X, expand="yes")

        scrollbar.config(command=self.tree.yview)

        # Frame Lists
        self.frameLists = Frame(self)
        self.frameLists.pack(side=LEFT)

        # Frame Forms
        self.frameForms = Frame(self)
        self.frameForms.pack(side=LEFT, padx=20)

        #Liste A selection
        self.frameListA = Frame(self.frameLists)
        self.frameListA.pack()
        
        Label(self.frameListA, text="Liste A : ").pack(side=LEFT)

        self.entryListA = Entry(self.frameListA, width=30)
        self.entryListA.pack(side=LEFT)

        self.buttonListA = Button(self.frameListA, text="Parcourir", command=self.load_fileListA, width=10)
        self.buttonListA.pack(side=LEFT, padx=5)

        # List B selection
        self.frameListB = Frame(self.frameLists)
        self.frameListB.pack(side=BOTTOM)

        Label(self.frameListB, text="Liste B : ").pack(side=LEFT)

        self.entryListB = Entry(self.frameListB, width=30)
        self.entryListB.pack(side=LEFT)

        self.buttonListB = Button(self.frameListB, text="Parcourir", command=self.load_fileListB, width=10)
        self.buttonListB.pack(side=LEFT, padx=5)

        # Form pValue
        self.framePVal = Frame(self.frameForms)
        self.framePVal.pack()

        Label(self.framePVal, text="pValue").pack(side=LEFT)
        self.entryPVal = Entry(self.framePVal, width=6)
        self.entryPVal.pack(side=LEFT)

        # Form foldC
        self.frameFoldC = Frame(self.frameForms)
        self.frameFoldC.pack()

        Label(self.frameFoldC, text="foldCh").pack(side=LEFT)
        self.entryFoldC = Entry(self.frameFoldC, width=6)
        self.entryFoldC.pack(side=LEFT)

        # Form note
        self.frameNote = Frame(self.frameForms)
        self.frameNote.pack()

        Label(self.frameNote, text="note    ").pack(side=LEFT)
        self.entryNote = Entry(self.frameNote, width=6)
        self.entryNote.pack(side=LEFT)

        # Bouton comparer
        self.buttonComparer = Button(self, text="Comparer", command=self.compare, width=10, state=DISABLED)
        self.buttonComparer.pack(fill= X, expand="yes", padx=20, pady=(10,0))

        #Bouton exporter
        self.buttonExport = Button(self, text="Exporter", command=self.export, width=10, state=DISABLED)
        self.buttonExport.pack(fill= X, expand="yes", padx=20)

        # Réinitialiser
        self.buttonReset = Button(self, text="Réinitialiser", command=self.reset, width=10)
        self.buttonReset.pack(fill= X, expand="yes", padx=20, pady=(0,10))

        # file members
        self.listA = None
        self.listB = None

    def load_fileListA(self):
        fname = askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*") ))
        if fname:
            self.entryListA.delete(0, END)
            self.listA = fname
            self.entryListA.insert(0,fname)


    def load_fileListB(self):
        fname = askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*") ))
        if fname:
            self.entryListB.delete(0, END)
            self.listB = fname
            self.entryListB.insert(0,fname)

            self.buttonComparer.config(state=NORMAL)

        else:
            showerror("Erreur : fichier B", "La liste B est introuvable")


    def resetTree (self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def reset(self):
        self.listA = None
        self.entryListA.delete(0, END)

        self.listB = None
        self.entryListB.delete(0, END)

        self.entryPVal.delete(0,END)
        self.entryFoldC.delete(0, END)
        self.entryNote.delete(0, END)

        self.buttonExport.config(state=DISABLED)
        self.buttonComparer.config(state=DISABLED)

        self.resetTree()

    def isValidfoldC(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def isValidPValue(self, s):
        try:
            f = float(s)
            if f >= 0 and f <= 1:
                return True
            else:
                return False
        except:
            return False

    def isValidNote (self, s):
        try:
            f = int(s)
            return True
        except:
            return False

    def compare(self):
        self.buttonExport.config(state=NORMAL)

        if not self.isValidfoldC(self.entryFoldC.get()) and not self.entryFoldC.get() == "":
            showerror("Erreur : foldC","La valeur fold Change n'est pas un nombre")

        elif not self.isValidPValue(self.entryPVal.get()) and not self.entryPVal.get() == "":
            showerror("Erreur : pValue","La valeur pValue n'est pas un nombre compris entre 0 et 1")

        elif not self.isValidNote(self.entryNote.get()) and not self.entryNote.get() == "":
            showerror("Erreur : note", "La valeur note n'est pas un nombre entier")

        elif self.listA is None and self.listB is not None:
            self.resetTree()

            try:
                listComp = ListComparator(self.listA, self.listB, self.entryPVal.get(), self.entryFoldC.get())
                for e in listComp.getDiffListB():
                    self.tree.insert('', 'end', values=e)
            
            except IndexError:
                showerror("Erreur : liste A invalide", "Le fichier liste A n'est pas un fichier valide")

        else:
            self.resetTree()

            try:
                listComp = ListComparator(self.listA, self.listB, self.entryPVal.get(), self.entryFoldC.get(), self.entryNote.get())
                for e in listComp.getDiff():
                    self.tree.insert('', 'end', values=e)

            except IndexError:
                showerror("Erreur : liste A ou B invalide", "Le fichier liste A ou B n'est pas un fichier valide")


    def export(self):
        if len(self.tree.get_children()) == 0:
            showinfo("Export", "Il n'y a rien à exporter")
            return

        fname = asksaveasfilename(filetypes=(("CSV files", "*.csv"),
                                             ("All files", "*.*") ))

        if  fname:
            resExp = []
            for it in self.tree.get_children():
                resExp.append(self.tree.item(it)["values"])

            expTabToCSV = TreeExportator(resExp, fname)
            expTabToCSV.export()

            showinfo("Export", "Exportation au format CSV réussi")

    def columnSort (self, col, descending=False):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)

        # reverse sort direction for next sort operation
        self.SortDir = not descending

if __name__ == "__main__":
    bioInf = BioInfo()
    bioInf.mainloop()