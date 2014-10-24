from ListBio import ListBio
from ListBioType import ListBioType

class ListBioB(ListBio):
    def __init__(self, namefile):
        super(self.__class__, self).__init__(ListBioType.TypeB, namefile)
