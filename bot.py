from constante import Constante
from typing import List
from tas_carte import Paquet
import random

class Bot() :
    def __init__(self) -> None:
        self.cards : List[int] = [] #Cards of the player (can't see all of them)
        self.card_get : int = Constante.DEFAULT #Card drawed by the player
        self.see_cards : List[List[int]] = [] #Cards see by the bot
        self.waste : List = [] #Cards wasted by the player
        self.score : int = 0
        self.nb_col = Constante.NBCOLONNE
        

    def get_jeu (self, lst_cards : list)->list :
        """Get the hand of the player"""
        self.cards = lst_cards
        return self.cards

    def init_see_cards(self)-> List[List[int]] :
        for i in range (Constante.NBCOLONNE) :
            self.see_cards.append([])
            for j in range (Constante.NBLIGNE) :
                self.see_cards[i].append(Constante.DEFAULT)
        return self.see_cards
    
    def init_waste(self, deck : Paquet) ->List :
        self.waste.append(deck.lst.pop(0))
        return self.waste

    def start_game(self)->List[List[int]] :
        self.see_cards[0][0] = self.cards[0][0]
        self.see_cards[0][1] = self.cards[0][1]

        return self.see_cards

    def draw_card(self, lst_cards : List[int]) -> int:
        return lst_cards.pop(0), lst_cards
    
    def get_cards(self) ->int : 
        return self.cards.pop(0)

    def update_score(self)->int:
        self.score = 0
        for i in range (self.nb_col):
            for j in range (Constante.NBLIGNE) :
                if (self.see_cards[i][j] != Constante.DEFAULT) :
                    self.score += self.see_cards[i][j]

        return self.score
    
    def check_column_card (self, cards : int) ->tuple :
        """
            Check if a column can be complete
            Return True, column position, and line position if possible
            Return False, None, None else
        """
        for i in range (self.nb_col) :
            if (self.see_cards[i][0] == self.see_cards[i][1] == cards) :
                return (True, i, 2)
            elif (self.see_cards[i][1] == self.see_cards[i][2] == cards) :
                return (True, i, 0)
            elif (self.see_cards[i][0] == self.see_cards[i][2] == cards) :
                return (True, i, 1)
        return (False, None, None)
    
    def check_full_column(self) -> int :
        for i in range (self.nb_col) :
            if (self.see_cards[i][0] == self.see_cards[i][1] == self.see_cards[i][2] and self.see_cards[i][0] != Constante.DEFAULT) :
                return i
        return None

    def min_column(self, num : int, cards : int) ->int :
        val = Constante.DEFAULT
        pos = 0
        for i in range(Constante.NBLIGNE) :
            if (self.see_cards[num][i] <= val or val != Constante.DEFAULT) :
                if (self.see_cards[num][i]!= cards) :
                    val = self.see_cards[num][i]
                    pos = i
        return pos #return the positon of the card
    
    def max_game(self)->int :
        res = Constante.DEFAULT
        posx = 0 
        posy = 0
        for i in range (self.nb_col) :
            for j in range (Constante.NBLIGNE) :
                if (self.see_cards[i][j] != Constante.DEFAULT and (self.see_cards[i][j] > res or res == Constante.DEFAULT)) :
                    res = self.see_cards[i][j]
                    posx = i
                    posy = j 
        
        return posx, posy
    
    def choose_pos(self, cards : int) ->int :
        for i in range (self.nb_col) :
            for j in range (Constante.NBLIGNE) :
                if (self.see_cards[i][j] == cards) : #we start to create a new column with multiple similar cards
                    posy = self.min_column(i, cards)
                    return i, posy 
        #we change the card with the higher rate
        posx, posy = self.max_game()
        return posx, posy
                    
    def return_random_card (self) :
        posx = random.randint(0, self.nb_col-1)
        posy = random.randint(0, Constante.NBLIGNE-1)

        while (self.see_cards[posx][posy] != Constante.DEFAULT) :
            posx = random.randint(0, self.nb_col-1)
            posy = random.randint(0, Constante.HEIGHT-1)

        return posx, posy
    

    def turn (self, lst_cards : List[int]) ->int :
        """
            Fix : prendre si faible carte + pas faire colonne de -1/-2 
            Fix : Choix changement de carte + faible
        """
        res = self.check_column_card(self.waste[0]) #check if a column can be complete with the top card in the trash doesn't take count of -1/-2 
        if (res[0] == True) : #a column can be complete
            print("Waste")
            return self.waste.pop(0), res[1], res[2], lst_cards #return the card and the position to place the card
        else :
            card, lst_cards = self.draw_card(lst_cards) #draw a card
            print("Deck")
            return card, res[1], res[2], lst_cards #return the card, no position and deck updated
    
    def game_finish(self)->bool :
        if (len(self.see_cards) == 0) :
            return True
        for i in range (self.nb_col) :
            for j in range (Constante.HEIGHT) :
                if (self.see_cards[i][j] == Constante.DEFAULT) :
                    return False
        return True

        
    def play_game(self, deck : Paquet)->List[List[int]] :
        tour = 0
        while (self.game_finish() == False) : #check if the game is finished
            print(f"Trash : {self.waste}")
            self.card_get, posx, posy, deck.lst = self.turn(deck.lst) #play a turn
            print(f"Carte récupéré : {self.card_get}")
            if (posx and posy != None) : #take the card from the trash
                print("")
                self.waste.insert(0, self.cards[posx][posy]) 
                self.see_cards[posx][posy] = self.card_get
            else :
                if (self.card_get >= 2) : #don't keep the card /
                    """
                        Fix : Keep the card if can create a column, keep it if is very under an other value 
                        Fix : Choose between card and waste at start
                    """
                    self.waste.insert(0, self.card_get)
                    #need to return a card before continue
                    print("return random card")
                    posx, posy = self.return_random_card() #not enought good
                    self.see_cards[posx][posy] = self.cards[posx][posy]
                    print(self.see_cards)
                else : #keep the card and change with a current from the game
                    posx, posy = self.choose_pos(self.card_get)
                    self.waste.insert(0, self.cards[posx][posy])
                    self.see_cards[posx][posy] = self.card_get
            
            col_delete = self.check_full_column()
            if (col_delete != None) :
                for i in range(Constante.NBLIGNE) :
                    self.waste.insert(0, self.see_cards[col_delete][i])
                self.see_cards.pop(col_delete)
                self.nb_col -= 1

            #print(f"Deck : {deck.lst}")
            print(f"Cartes vues : {self.see_cards}")
            tour += 1
       
            self.score = self.update_score()
            if (tour > 20) :
                return self.see_cards, self.score
            self.waste.insert(0, deck.lst.pop(0))
        return self.see_cards, self.score
                    



        