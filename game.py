import random
from tas_carte import Paquet
from bot import Bot




def shuffle_cards(cartes) :
    for i in range (10) :
        random.shuffle(cartes.lst)
    return cartes.lst
    
def jeu() :
    lst_cards = []
    jbot = Bot()

    cartes = Paquet()
    cartes.lst = cartes.create_cards()
    
    cartes.lst = shuffle_cards(cartes)
    
    cartes.print_paquet()
    cartes.longueur_paquet()

    lst_cards = cartes.give_cards()
    jbot.cards = jbot.get_jeu(lst_cards)
    print(jbot.cards)
    jbot.waste = jbot.init_waste(cartes)
    jbot.see_cards = jbot.init_see_cards()
    print(jbot.see_cards)
    jbot.see_cards = jbot.start_game()
    print(jbot.see_cards)
    print(f"Resulat : {jbot.play_game(cartes)}") 

jeu()