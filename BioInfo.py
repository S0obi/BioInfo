from tkinter import Tk, Text, Frame, Toplevel, LabelFrame, Label, Entry, Button, OptionMenu, StringVar
from tkinter import LEFT, RIGHT, BOTTOM, TOP, VERTICAL, X, Y, INSERT, END, DISABLED, NORMAL, FALSE
from tkinter.ttk import Treeview, Scrollbar
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, showinfo

from ListComparator import ListComparator
from ListBioType import ListBioType
from TreeExportator import TreeExportator

class BioInfo(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.wm_title("BioInfo : comparaison des listes")
        self.resizable(width=FALSE, height=FALSE)
        self.SortDir = False

        # Lists Types
        self.typeList1 = None
        self.typeList2 = None

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

        #Liste n°1 selection
        self.frameList1 = Frame(self.frameLists)
        self.frameList1.pack()

        self.typeListStr1 = StringVar(self.frameList1)
        self.typeListStr1.set(str(ListBioType.TypeA))

        self.buttonTypeList1 = OptionMenu(self.frameList1, self.typeListStr1, str(ListBioType.TypeA), str(ListBioType.TypeB), "\t\t\t ").pack(side=LEFT)

        self.entrylist1 = Entry(self.frameList1, width=30)
        self.entrylist1.pack(side=LEFT)

        self.buttonBrowseList1 = Button(self.frameList1, text="Parcourir", command=self.load_fileList1, width=10)
        self.buttonBrowseList1.pack(side=LEFT, padx=5)

        # List n°2 selection
        self.frameList2 = Frame(self.frameLists)
        self.frameList2.pack(side=BOTTOM)

        self.typeListStr2 = StringVar(self.frameList2)
        self.typeListStr2.set(str(ListBioType.TypeB))

        self.buttonTypeList2 = OptionMenu(self.frameList2, self.typeListStr2, str(ListBioType.TypeA), str(ListBioType.TypeB), "\t\t\t ").pack(side=LEFT)

        self.entrylist2 = Entry(self.frameList2, width=30)
        self.entrylist2.pack(side=LEFT)

        self.buttonBrowseList2 = Button(self.frameList2, text="Parcourir", command=self.load_fileList2, width=10)
        self.buttonBrowseList2.pack(side=LEFT, padx=5)

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
        self.list1 = None
        self.list2 = None

    def load_fileList1(self):
        fname = askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*") ))
        if fname:
            self.entrylist1.delete(0, END)
            self.list1 = fname
            self.entrylist1.insert(0,fname)

            self.buttonComparer.config(state=NORMAL)


    def load_fileList2(self):
        fname = askopenfilename(filetypes=(("CSV files", "*.csv"),
                                           ("All files", "*.*") ))
        if fname:
            self.entrylist2.delete(0, END)
            self.list2 = fname
            self.entrylist2.insert(0,fname)

            self.buttonComparer.config(state=NORMAL)

        else:
            showerror("Erreur : fichier B", "La liste B est introuvable")


    def resetTree (self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def reset(self):
        self.list1 = None
        self.entrylist1.delete(0, END)

        self.list2 = None
        self.entrylist2.delete(0, END)

        self.entryPVal.delete(0,END)
        self.entryFoldC.delete(0, END)
        self.entryNote.delete(0, END)

        self.typeList1 = None
        self.typeList2 = None

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

        # Détermination type Listes

        # List 1

        if self.typeListStr1.get() == str(ListBioType.TypeA):
            self.typeList1 = ListBioType.TypeA
        elif self.typeListStr1.get() == str(ListBioType.TypeB):
            self.typeList1 = ListBioType.TypeB
        else:
            self.typeList1 = None

        # List 2
        if self.typeListStr2.get() == str(ListBioType.TypeA):
            self.typeList2 = ListBioType.TypeA
        elif self.typeListStr2.get() == str(ListBioType.TypeB):
            self.typeList2 = ListBioType.TypeB
        else:
            self.typeList2 = None


        if not self.isValidfoldC(self.entryFoldC.get()) and not self.entryFoldC.get() == "":
            showerror("Erreur : foldC","La valeur fold Change n'est pas un nombre")

        elif not self.isValidPValue(self.entryPVal.get()) and not self.entryPVal.get() == "":
            showerror("Erreur : pValue","La valeur pValue n'est pas un nombre compris entre 0 et 1")

        elif not self.isValidNote(self.entryNote.get()) and not self.entryNote.get() == "":
            showerror("Erreur : note", "La valeur note n'est pas un nombre entier")

        # (List A and No List) or (No List and List A)
        elif ((self.list1 is not None and self.typeList1 == ListBioType.TypeA) and (self.list2 is None)) or\
             ((self.list2 is not None and self.typeList2 == ListBioType.TypeA) and (self.list1 is None)):

            self.resetTree()

            try:
                listComp = ListComparator(self.list1, self.list2, self.entryPVal.get(), self.entryFoldC.get(), self.entryNote.get())
                for e in listComp.getFilterListA():
                    self.tree.insert('', 'end', values=e)

            except IndexError:
                showerror("Erreur : liste A invalide", "Le fichier liste A n'est pas un fichier valide")


        # (List B and No List) or (No List and List B)
        elif ((self.list1 is not None and self.typeList1 == ListBioType.TypeB) and (self.list2 is None)) or\
             ((self.list2 is not None and self.typeList2 == ListBioType.TypeB) and (self.list1 is None)):

            self.resetTree()

            try:
                listComp = ListComparator(self.list1, self.list2, self.entryPVal.get(), self.entryFoldC.get())
                for e in listComp.getFilterListB():
                    self.tree.insert('', 'end', values=e)
            
            except IndexError:
                showerror("Erreur : liste A invalide", "Le fichier liste A n'est pas un fichier valide")

        # (List A and List B) or (List B and List A)
        elif ((self.list1 is not None and self.typeList1 == ListBioType.TypeA) and \
             (self.list2 is not None and self.typeList2 == ListBioType.TypeB)) or \
             ((self.list1 is not None and self.typeList1 == ListBioType.TypeB) and \
             (self.list2 is not None and self.typeList2 == ListBioType.TypeA)):

            self.resetTree()

            listA = ""
            listB = ""
            if self.typeList1 == ListBioType.TypeA:
                listA = self.list1
            else:
                listA = self.list2

            if self.typeList1 == ListBioType.TypeB:
                listB = self.list1
            else:
                listB = self.list2
            try:
                listComp = ListComparator(listA, listB, self.entryPVal.get(), self.entryFoldC.get(), self.entryNote.get())
                for e in listComp.getDiffAandB():
                    self.tree.insert('', 'end', values=e)

            except IndexError:
                showerror("Erreur : liste A ou B invalide", "Le fichier liste A ou B n'est pas un fichier valide")

        # (List A and List A)
        elif ((self.list1 is not None and self.typeList1 == ListBioType.TypeA) and \
             (self.list2 is not None and self.typeList2 == ListBioType.TypeA)):

            self.resetTree()

            try:
                listComp = ListComparator(self.list1, self.list2, self.entryPVal.get(), self.entryFoldC.get(), self.entryNote.get())
                for e in listComp.getDiffAandA():
                    self.tree.insert('', 'end', values=e)

            except IndexError:
                showerror("Erreur : liste A ou B invalide", "Le fichier liste A ou B n'est pas un fichier valide")

        # (List B and List B)
        elif ((self.list1 is not None and self.typeList1 == ListBioType.TypeB) and \
             (self.list2 is not None and self.typeList2 == ListBioType.TypeB)):

            self.resetTree()

            try:
                listComp = ListComparator(self.list1, self.list2, self.entryPVal.get(), self.entryFoldC.get())
                for e in listComp.getDiffBandB():
                    self.tree.insert('', 'end', values=e)

            except IndexError:
                showerror("Erreur : liste A ou B invalide", "Le fichier liste A ou B n'est pas un fichier valide")
        else:
            print("No condition")
            print(str(self.typeList1))
            print(str(self.typeList2))


    def export(self):
        if len(self.tree.get_children()) == 0:
            showinfo("Export", "Il n'y a rien à exporter")
            return

        fname = asksaveasfilename(filetypes=(("CSV files", "*.csv"),
                                             ("All files", "*.*") ))

        if fname:
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