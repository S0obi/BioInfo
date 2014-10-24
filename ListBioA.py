from ListBio import ListBio
from ListBioType import ListBioType

class ListBioA(ListBio):
    def __init__(self):
        super(self.__class__, self).__init__(ListBioType.TypeA)
