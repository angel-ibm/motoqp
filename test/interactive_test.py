#!/usr/bin/env python3

# Code written on python 3.9.2, please observe the general compatibility rules

from random import randint
from motoqp import circuit,race,championship,rider,WrongParameterValue


########################
## DISPLAY GAME RULES ##
########################

def display_game_rules(ch2021,marc) :
    print("################## RULES OF THE GAME ###########################")
    print("You are about to compete against me in a motorbike championship")
    print("and I will demonstrate to you my quantum supremacy. ")
    print("Resistance is futile... but I like to see how humans lose. He he he...")
    print("")
    print("Five bikes have been assigned to you. They can only run in ONE race.")
    print("Did you understand it? They are NOT reusable, OK?")
    print("Here is a list of their specs (the bigger, the better). Remember them.")
    print("...well I know that you can't. Humans are weak. He he he...")
    print("So, I will have to show them again several times during the championship.")
    print("")
    print("Anyway, these are your bikes:")
    print("")
    for i in range(len(marc.garage)) :
        print("Marc's bike #", i)
        print("---------------")
        print(marc.garage[i].specs)
        print("\n\n")

    print("I also have five bikes. But you will not see them.")
    print("In this championship, we are going to run in five circuits:\n")
    for i in range(len(ch2021.races)) :
        print("  Circuit #", i, "....." ,ch2021.races[i].circuit.name, "\t(",ch2021.races[i].name, ")" )

    print("\n\n")
    print("For a given circuit, there is one and only one")
    print("specification of your bike that matters for winning the race.")
    print("These are:")

    for i in range(len(ch2021.races)) :
        print("  Circuit #", i, "..." ,ch2021.races[i].circuit.name, 
            "... this circuit is ...",circuit.type_text[ch2021.races[i].circuit.type], 
            "... So, the bike with the best...",race.win_criteria[circuit.type_text[ch2021.races[i].circuit.type]], "... will win" )

    print("")
    print("Yeah, I know that you can't remember this either. Let's try again:")
    for i in range(len(ch2021.races)) :
        print("   ", circuit.type_text[ch2021.races[i].circuit.type], "\t", race.win_criteria[circuit.type_text[ch2021.races[i].circuit.type]])

    print("")
    print("Now, it is time to collapse your brain. Pay attention now:")
    print("In this championship, there are two types of races:")
    print("\t- normal races" )
    print("\t- fool's races")
    print("In normal races, the winner gets the prize - as expected")
    print("but in fool's races, the loser gets the prize.")
    print("I told you that your brain would collapse. Am I right?")

    print("")
    print("You will always have to choose your bike for each race")
    print("but, in some races, you will choose the circuit")
    print("and, in other cases, you will choose if we'll run a normal race or a fool's race.")
    print("I will tell you what you can choose and when")
    print("I know that you will run to win and you want to beat me, no matter if we have a normal race or a fool's race.")
    print("I will do the same.")
    print("So, are you ready to bite the dust? [Y/n]")
    response = str(input())
    if (response == "n") :
        print("OK. I knew you were a fraidy cat. Bye")
        exit()

###################
## PICK_FREEBIKE ##
###################

def pick_freebike(currider,interactive='no') :
    if (interactive == 'interactive') :
        print("")
        print("These are your free bikes for the next race")
        response = -2 # no free bike found
        for i in range(len(currider.garage)) :
            if (currider.garage[i].isfree == 1 ) :
                print("Bike #",i, currider.garage[i].specs)
                response = -1 # at least one bike will be free
        if (response == -2) :
            return(-2)

        while (response == -1) :
            print("Enter the number of the bike you want to use")
            try :
                response = int(input())
            except:
                print("Please enter a valid number")
            else :
                if (response < 0 or (response > (len(currider.garage) - 1))) :
                    print("This bike does not exist. Enter a number between", 0 , "and", (len(currider.garage) - 1))
                    response = -1
                else :
                    if (currider.garage[response].isfree == 0) :
                        print("This bike is not free. Enter a number you are seeing")
                        response = -1
    else :
        for i in range(len(currider.garage)) :
            if (currider.garage[i].isfree == 1 ) :
                response = i # The first free
                break
    
    currider.garage[response].isfree = 0
    return(currider.garage[response])

#####################
## SELECT RACETYPE ##
#####################

def select_racetype(currace, interactive='no', quantum=0):
    if (interactive == 'interactive') :
        response = 0
        while (response == 0) :
            print("Select a type of race:")
            print("\t(1) NORMAL race: the WINNER gets the prize ")
            print("\t(2) FOOL'S race: the LOSER gets the prize ")
            print("Enter the number 1 or 2")
            try :
                response = int(input())
            except:
                print("Please enter a valid number")
                response = 0
            else :
                if (response < 1 or response > 2) :
                    print("Come on... it's easy. Just the number 1 or 2")
                    response = 0
    else :
        if (quantum == 0) :
            response = currace.select_racetype(quantum=0)    
        else :
            response = currace.select_racetype(quantum=1) 

    
    if (response == 1 ) :
        return ('normal')
    else :
        return ('fool')

####################
## SELECT CIRCUIT ##
####################

def select_circuit(chmp, interactive='no', quantum=0):
  
    curraces = chmp.available_races 
    if (interactive == 'interactive') :
        print("These are the free circuits for the next race")
        response = -2 # no free circuit found
        for i in range(len(curraces)) :
            if (curraces[i].circuit.isfree == 1) :
                print("Circuit #", i, curraces[i].circuit.name, ': \033[1m', circuit.type_text[curraces[i].circuit.type], '\033[0m')
                response = -1 # at least one free circuit found
        if (response == -2):
            return (-2)
        
        while (response == -1) :
            print("Enter the number of the circuit")
            try :
                response = int(input())
            except :
                print("Please enter a valid number")
            else :
                if (response < 0 or (response > (len(curraces) - 1))) :
                    print("This circuit does not exist. Enter a number between 0 and", len(curraces) - 1 )
                    response = -1
                else :
                    if (curraces[response].circuit.isfree == 0) :
                        print("This circuit is not free. Enter one of the numbers you are seeing")
                        response = -1
        chmp.races.append(curraces[response])
    else :
        if (quantum == 0 ):
            for i in range(len(curraces)) :
                if (curraces[i].circuit.isfree == 1) :
                    response = i # The first free
                    break
            chmp.races.append(curraces[i])

        else :
            chmp.select_freecircuitrace(quantum=1) 

    return(chmp.races[-1]) # The race just added now

###########################
#### INTERACTIVE TEST #####
###########################

def interactive_test():

    #- create the riders and assign bikes in the background
    marc = rider('Marc Márquez',quantum=0)
    valentino = rider('Valentino Rossi', quantum=1)

     #- create the circuits
    americas = circuit('straight', 'Americas')
    jerez = circuit('uphills', 'Jerez')
    mugello = circuit('downhills', 'Mugello')
    motegi = circuit('windy', 'Motegi')
    phillip = circuit('rainy', 'Phillip Island')

    #- create the races, just assigning the circuit by the moment
    usa = race('USA', americas)
    spain = race('Spain', jerez)
    italy = race('Italy', mugello)
    japan = race('Japan', motegi)
    australia = race('Australia', phillip)

    #- create the new championship by defining the races and 
    #- which rider is the current champion (last winner)

    ch2021 = championship (
        'Moto QP 2021',
        [usa, spain, italy, japan, australia],
        [marc,valentino] 
    )

    human = marc
    quantum = valentino

    print("\n\n")
    print("Hello human. I am a quantum computer. My name is", quantum.name)
    print("If you don't mind, I will call you", human.name)
    print("...and if you do mind, get used to it. He he he...")
    print("")

    print("Do you want to read the rules? [N/y]")
    response = str(input())
    if (response == 'y') :
        display_game_rules(ch2021, marc)
        
    print("\n\n")

    print('The choices of',human.name, "will be done randomly by normal python funtions")
    print('The choices of',quantum.name, "will be quantum-based by qiskit functions")
    print('')

   
    print("First of all, you need to pick one of your bikes")
    print("Then, you will either select a circuit OR the type of race (normal/fool's)")

    for i in range(len(ch2021.available_races)) :

        human_bike = pick_freebike(human,'interactive')
        quantum_bike = pick_freebike(quantum, 'automatic')
        if (human_bike == -2 or quantum_bike == -2) :
            print("Sorry, no more bikes free. Something went wrong")
            exit()

        if ((i % 2) == 0) : 
            circuitrace = select_circuit(ch2021, 'automatic', quantum = 1)
            racetype = select_racetype(circuitrace,'interactive')
            
        else :
            circuitrace = select_circuit(ch2021,'interactive')
            racetype = select_racetype(circuitrace, 'automatic', quantum = 1)
   
        try :
            result = ch2021.run (
                        circuitrace,
                        racetype,
                        [ 
                            [human, human_bike],
                            [quantum, quantum_bike]
                        ]
            )
        except WrongParameterValue as e :
            print('Something went wrong')
            print(e.args[0])
            exit() # you must explicitly call exit() if the exception is caught, if you want to exit
        
        print("---------------------------------------------------------------------------------------")
        print('Race #', i+1,  
            '\nCircuit: ' + ch2021.races[i].circuit.name ,
            '---\033[1m',  circuit.type_text[ch2021.races[i].circuit.type], '\033[0m---'  )
        print("The important spec for this circuit is: ###\033[1m", 
            race.win_criteria[ch2021.races[i].circuit.type_text[ch2021.races[i].circuit.type]],
            "\033[0m### ")
        print(human.name + "'s bike: ", human_bike.specs)
        print(quantum.name + "'s bike: ", quantum_bike.specs)
        print("...and this is a ***\033[1m", racetype, "\033[0m*** race")

        if (result == 0) :
            print("The race #", i+1, "has no winner. Each rider gets 1 point")
        else :
            print("-------> The prize of the race #", i+1, "goes to \033[1m", result.name, "\033[0m. 2 points for this rider")
        print("The current championship scores are:")
        print("Human:",human.name, "score:", human.points, "points")
        print("Quantum:",quantum.name, "score:", quantum.points, "points")
        print("---------------------------------------------------------------------------------------")
        print("")

    
    print ('\nFinal Score:', marc.name +':', marc.points, 'points. ',  valentino.name +': ' , valentino.points, 'points. \n')
    if (marc.points == valentino.points ) :
        final_winner = []
    elif (marc.points > valentino.points) :
        final_winner = marc
    else :
        final_winner = valentino
                
    print('---------------------------------------------------')
    if ( final_winner == []) :
        print("No winner in this Championship")
    else:
        print("The winner of the Championship is: \033[1m", final_winner.name.upper(),'\033[0m')
    print('---------------------------------------------------\n\n\n')   
    
###############
#### MAIN #####
###############

interactive_test()
