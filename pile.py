
class Element:
    def __init__(self, info, pointeur):
        self.info = info
        self.pointeur = pointeur   # element en dessous dans la pile


class Pile:
    def __init__(self):
        self.tete = None
        self.nb_elements = 0

    def Empiler(self, info):
        # le nouvel element devient le sommet
        self.tete = Element(info, self.tete)
        self.nb_elements = self.nb_elements + 1

    def Depiler(self):
        if self.Est_vide():
            return None
        info = self.tete.info
        self.tete = self.tete.pointeur
        self.nb_elements = self.nb_elements - 1
        return info

    def Sommet(self):
        if self.Est_vide():
            return None
        return self.tete.info

    def Est_vide(self):
        return self.tete == None

    def Est_pleine(self):
        return False