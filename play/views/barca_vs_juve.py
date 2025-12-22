import time
import random
from django.http import HttpResponse

from ..models import Player
from . import barca_squad, juve_squad
from .utils import *

 

# նախնական ստատիկ տվյալների ներմուծում //////////////////////////////////////////////////
Barca_ID = list(Player.objects.filter(team='Barcelona', is_starting=True).values_list('id', flat=True))
Juve_ID = list(Player.objects.filter(team='Juventus', is_starting=True).values_list('id', flat=True))
Barca_Bench_ID = list(Player.objects.filter(team='Barcelona', is_starting=False).values_list('id', flat=True))
Juve_Bench_ID = list(Player.objects.filter(team='Juventus', is_starting=False).values_list('id', flat=True))

first_half_team = 'Barcelona'
second_half_team = 'Juventus'

team = first_half_team
Versions = ["Pass", "Shoot"]
# ////////////////////////////////////////////////////////////////////////////////////////
# Գլխավոր ֆունկցիա //////////////////////////////////////////////////////////////////////
def barca_vs_juve(request):
    initial_state = save_initial_state()
    team = 'Barcelona' # Առաջին խաղակեսը սկսում է Բարսելոնան
    output = [] # output on browser screen
    score =[0, 0]
    Ratings = {}
    for i in list(range(2, 13)) + list(range(23, 34)):
        Ratings[f"{Player.objects.get(id=i).name}"] = 5

    inital_barca_player = Player.objects.get(id=4) # Դաշտի կենտրոնից խաղը միշտ սկսում ա կենտրոնական հարձակվողը
    inital_target_barca_player = Player.objects.get(id=random.choice([n for n in Barca_ID if n != inital_barca_player.id])) # Փոխանցում ստացող ֆուտբոլիստ

    inital_juve_player = Player.objects.get(id=24) # Դաշտի կենտրոնից խաղը միշտ սկսում ա կենտրոնական հարձակվողը
    inital_target_juve_player = Player.objects.get(id=random.choice([n for n in Juve_ID if n != inital_juve_player.id])) # Փոխանցում ստացող ֆուտբոլիստ
    
    barca_squad(request) # Բարսելոնայի կազմը
    juve_squad(request) # Յուվետնուսի կազմը
    output += barca_squad(request)
    output += juve_squad(request)
    time.sleep(3)

    print("\n")
    output.append("</br>")
#//////////////////////////////////////////////////////////////
# Առաջին խաղակես
    print("We are starting the 1st half\nBarcelona starts from centre\n")
    output.append("We are starting the 1st half</br>Barcelona starts from centre</br>")
    for i in range(1, 46): # 45 անգամ կրկնություն այսինքն 45 րոպե
        version = random.choices(Versions, weights=[90, 10], k=1)[0] # Կատարվելիք գործողության որոշում
        res = random.choices(['ok', 'fail'], weights=[85, 15], k=1)[0] # Փոխանցումի հաջող լինելու հավանականությունն է որոշում
        res1 = random.choices(['ok', 'fail'], weights=[20, 80], k=1)[0]

        if team == 'Barcelona': # Թիմը Բարսելոնան է, փոխանցման հաջողության դեպքում կրկին փոխանցում է ձեռնարկվում, հակառակ դեպքում գնդակը անցնում է մրցակցին 
            P1_barca = inital_barca_player
            P2_barca = inital_target_barca_player
            if version == "Pass":
                if res == 'ok':
                    inital_barca_player, inital_target_barca_player, Ratings = correct_pass(P1_barca, P2_barca, i, output, Barca_ID, Ratings)
                else:
                    team = 'Juventus' 
                    inital_juve_player, inital_target_juve_player, Ratings = wrong_pass(inital_barca_player, inital_juve_player, inital_target_juve_player, i, output, Juve_ID, team, Ratings)
            elif version == "Shoot":
                if res1 == 'ok':
                    score, inital_juve_player, team, Ratings = goal_kicking(P1_barca, team, output, score, i, Ratings) 
                else:
                    team, inital_juve_player, Ratings = miss_kicking(output, P1_barca, team, i, Ratings)
                version = "Pass"


        elif team == 'Juventus':  # Թիմը Յուվենտուսն է, փոխանցման հաջողության դեպքում կրկին փոխանցում է ձեռնարկվում, հակառակ դեպքում գնդակը անցնում է մրցակցին 
            P1_juve = inital_juve_player
            P2_juve = inital_target_juve_player
            if version == "Pass":
                if res == 'ok':
                    inital_juve_player, inital_target_juve_player, Ratings = correct_pass(P1_juve, P2_juve, i, output, Juve_ID, Ratings)
                else:
                    team = 'Barcelona'
                    inital_barca_player, inital_target_barca_player, Ratings = wrong_pass(inital_juve_player, inital_barca_player, inital_target_barca_player, i, output, Barca_ID, team, Ratings)
            elif version == "Shoot":
                if res1 == 'ok':
                    score, inital_barca_player, team, Ratings = goal_kicking(P1_juve, team, output, score, i, Ratings)
                else:
                    team, inital_barca_player, Ratings = miss_kicking(output, P1_juve, team, i, Ratings)
                version = "Pass"

        time.sleep(0.5)

    adding_time(i, output)

    print(f'\n/////FIRST HALF IS ENDED/////')
    print(f'/////BARCELONA {score[0]} - {score[1]} JUVENTUS/////')
    output.append(f'</br>/////FIRST HALF IS ENDED/////')
    output.append(f'/////BARCELONA {score[0]} - {score[1]} JUVENTUS /////')
#/////////////////////////////////////////////////////////////////////////////////////////////
# Առաջին խաղակեսի ավարտ
    time.sleep(5)


# Երկրորդ խաղակես
    print("We came back and starting the 2st half\nJuventus starts from centre\n")
    output.append("We came back and starting the 1st half</br>Juventus starts from centre</br>")
    for i in range(46,91):
        if i == 60:
            print('\n//////////////////////// Changes //////////////////////')
            output.append('<\br>//////////////////////// Changes //////////////////////')
            subs(Barca_ID, Barca_Bench_ID, Ratings, output)
            subs(Barca_ID, Barca_Bench_ID, Ratings, output)
            subs(Barca_ID, Barca_Bench_ID, Ratings, output)
            subs(Juve_ID, Juve_Bench_ID, Ratings, output)
            subs(Juve_ID, Juve_Bench_ID, Ratings, output)
            subs(Juve_ID, Juve_Bench_ID, Ratings, output)            
            print('///////////////////////////////////////////////////////\n')
            output.append('///////////////////////////////////////////////////////</br>')
            time.sleep(2)
        elif i == 75:
            print('\n//////////////////////// Changes //////////////////////')
            output.append('<\br>//////////////////////// Changes //////////////////////')
            subs(Barca_ID, Barca_Bench_ID, Ratings, output)
            subs(Barca_ID, Barca_Bench_ID, Ratings, output)
            subs(Juve_ID, Juve_Bench_ID, Ratings, output)
            subs(Juve_ID, Juve_Bench_ID, Ratings, output)
            print('///////////////////////////////////////////////////////\n')
            output.append('///////////////////////////////////////////////////////</br>')
            time.sleep(2)
        else:
            team = "Juventus"
            version = random.choices(Versions, weights=[70, 20], k=1)[0] # Կատարվելիք գործողության որոշում
            res = random.choices(['ok', 'fail'], weights=[85, 15], k=1)[0] # Փոխանցումի հաջող լինելու հավանականությունն է որոշում
            res1 = random.choices(['ok', 'fail'], weights=[20, 80], k=1)[0]
            if team == 'Barcelona': # Թիմը Բարսելոնան է, փոխանցման հաջողության դեպքում կրկին փոխանցում է ձեռնարկվում, հակառակ դեպքում գնդակը անցնում է մրցակցին 
                P1_barca = inital_barca_player
                P2_barca = inital_target_barca_player


                if version == "Pass":
                    if res == 'ok':
                        inital_barca_player, inital_target_barca_player, Ratings = correct_pass(P1_barca, P2_barca, i, output, Barca_ID, Ratings)
                    else:
                        team = 'Juventus' 
                        inital_juve_player, inital_target_juve_player, Ratings = wrong_pass(inital_barca_player, inital_juve_player, inital_target_juve_player, i, output, Juve_ID, team, Ratings)
                elif version == "Shoot":
                    if res1 == 'ok':
                        score, inital_juve_player, team, Ratings = goal_kicking(P1_barca, team, output, score, i, Ratings) 
                    else:
                        team, inital_juve_player, Ratings = miss_kicking(output, P1_barca, team, i, Ratings)
                    version = "Pass"


            elif team == 'Juventus':  # Թիմը Յուվենտուսն է, փոխանցման հաջողության դեպքում կրկին փոխանցում է ձեռնարկվում, հակառակ դեպքում գնդակը անցնում է մրցակցին 
                P1_juve = inital_juve_player
                P2_juve = inital_target_juve_player

                if version == "Pass":
                    if res == 'ok':
                        inital_juve_player, inital_target_juve_player, Ratings = correct_pass(P1_juve, P2_juve, i, output, Juve_ID, Ratings)
                    else:
                        team = 'Barcelona'
                        inital_barca_player, inital_target_barca_player, Ratings = wrong_pass(inital_juve_player, inital_barca_player, inital_target_barca_player, i, output, Barca_ID, team, Ratings)
                elif version == 'Shoot':
                    if res1 == 'ok':
                        score, inital_barca_player, team, Ratings = goal_kicking(P1_juve, team, output, score, i, Ratings)
                    else:
                        team, inital_barca_player, Ratings = miss_kicking(output, P1_juve, team, i, Ratings)
                    version = "Pass"

        time.sleep(0.5)

    adding_time(i, output)
    
    print(f'\n///// THE MATCH IS ENDED/////')
    print(f'/////BARCELONA {score[0]} - {score[1]} JUVENTUS/////')
    output.append(f'</br>/////THE MATCH IS ENDED/////')
    output.append(f'/////BARCELONA {score[0]} - {score[1]} JUVENTUS /////')

    if score[0] == score[1]:
        penality_shootout(output)
    

    print("\n************* Ratings of footballers *************")
    for player, rating in Ratings.items():
        output.append(f"{player} --> {rating}")
        print(f"{player} --> {rating}", end=' || ')

    best_player, best_rating = max(Ratings.items(), key=lambda x: x[1])
    print(f"\n************* MAN OF THE MACTH IS {best_player} - {best_rating} *************")
    output.append(f"</br>************* MAN OF THE MACTH IS {best_player} - {best_rating} *************")   

    restore_initial_state(initial_state)
    return HttpResponse("<br>".join([x.decode() if isinstance(x, bytes) else x for x in output]))


