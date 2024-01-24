from typing import List
from constante import Constante


class Paquet () :
    def __init__(self) -> None:
        self.lst : List[List[int]] = []

    def create_cards (self) :
        for i in range (5) :
            self.lst.append(-2)
        for j in range (15) :
            self.lst.append(0)
        for k in range (10) :
            self.lst.append(-1)
            for h in range (12) :
                self.lst.append(h)
        return self.lst
    
    def print_paquet(self)->None :
        print(self.lst)

    def longueur_paquet(self)->None :
        print(len(self.lst))

    def give_cards(self)->List[List[int]] :
        lst = []
        for i in range (Constante.WIDTH) : #have column instead of line
            lst.append([])
            for j in range (Constante.HEIGHT) :
                lst[i].append(self.lst.pop(0)) 
        return lst