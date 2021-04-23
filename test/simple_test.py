#!/usr/bin/env python3

# Code written on python 3.9.2, please observe the general compatibility rules

from random import randint
from motoqp import circuit,race,championship,rider,WrongParameterValue


######################
#### SIMPLE TEST #####
######################

def simple_test():

      #- create the riders and assign bikes in the background
    marc = rider('Marc Marquez', quantum=0)
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
    
    global ch2021

    ch2021 = championship (
        'Moto QP 2021',
        [usa, spain, italy, japan, australia],
        [marc,valentino] 
    )
    print('\n\n\n---------------------------------------------------') 
    print('------------     MOTO QP    -----------------------') 
    print('---------------------------------------------------\n\n\n') 

    print('The choices of',marc.name, "will be done randomly by normal python funtions")
    print('The choices of',valentino.name, "will be quantum-based by qiskit functions")
    print('')
  

    for i in range(len(ch2021.available_races)) :
        
        if ((i % 2) == 0) :
            # A QUANTUM choice for the circuit
            circuittype = ch2021.select_freecircuitrace(quantum=1) 
            # A random choice for normal/fool race          
            racetype = ch2021.races[i].select_racetype(quantum=0)           
        else :
            # alternate choices for odd numbers
            circuittype = ch2021.select_freecircuitrace(quantum=0)
            racetype = ch2021.races[i].select_racetype(quantum=1)

        # \033[1m = bold print on       \033[0m = bold print off
        print('Race #', i+1,  
            '\nCircuit: ' + ch2021.races[i].circuit.name ,
            '---\033[1m',  circuit.type_text[circuittype], '\033[0m---'  )
        print("The important spec for this circuit is: ###\033[1m", 
            race.win_criteria[ch2021.races[i].circuit.type_text[ch2021.races[i].circuit.type]],
            "\033[0m### ")
        print(marc.name + "'s bike: ", marc.garage[i].specs)
        print(valentino.name + "'s bike: ", valentino.garage[i].specs)
        print("...and this is a ***\033[1m", race.race_types[racetype], "\033[0m*** race")
             
        try :
            winner = ch2021.run (
                        ch2021.races[i],
                        racetype,
                        [ 
                            [marc, marc.garage[i]],
                            [valentino, valentino.garage[i]]
                        ]
            )
        except WrongParameterValue as e :
            print('Something went wrong')
            print(e.args[0])
            exit() # when the exception is caught, you must explicitly call exit() if you really want to exit
        if ( winner == 0 ) :
            print('-----> No winner in this race')
        else :
            print('------> The prize of the race goes to:', winner.name)
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

simple_test()
