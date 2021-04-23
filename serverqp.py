#!/usr/bin/env python3

# The functions here capture the REST Api calls, combined with swagger.yaml

import json
import inspect
from flask import make_response, abort, request
from motoqp import circuit,race,championship,ch2021,rider,bike,WrongParameterValue

def init_post() :

    global ch2021

    if (ch2021 != None):
        abort(500, inspect.stack()[0].function + ": The Championship already exists")

    #- create the riders and assign bikes in the background
    marc = rider('Marc Marquez',quantum=0)
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

    return({'chname' : ch2021.name})

def init_get() :
    global ch2021
    if (ch2021 == None) :
        abort(500, inspect.stack()[0].function + ": The Championship does not exist yet")
    return({'chname' : ch2021.name})

def init_delete() :
    global ch2021
    
    if (ch2021 == None) :
        abort(500, inspect.stack()[0].function + ": The Championship does not exist yet")
   
    ch2021.finalize()
    ch2021 = None 

    return("Successfully deleted")

def circuit_getall(onlyfree=False) :
    global ch2021
   
    if (ch2021 == None) :
        abort(500, "The Championship does not exist yet")
    
    all_circuits = []
    
    for i in ch2021.available_races :
        if (onlyfree and i.circuit.isfree == 0) :
            continue
        all_circuits.append({'circuit_name': i.circuit.name, 
                             'circuit_type': i.circuit.type_text[i.circuit.type],
                             'circuit_id' : i.circuit.id})
    
    if (all_circuits == []):
        abort(501, "No free circuit")
    
    return(all_circuits)

def rider_getall() :
    global ch2021
   
    if (ch2021 == None) :
        abort(500, "The Championship does not exist yet")
    
    all_riders = []
    
    for i in ch2021.riders :
        all_riders.append({'rider_name': i.name, 
                             'rider_type': 'Quantum' if (i.quantum == 1) else 'Human' ,
                             'rider_id' : i.id})
    
    return(all_riders)

def bike_getall(onlyfree=False):
    global ch2021

    if (ch2021 == None) :
        abort(500, "The Championship does not exist yet")

    all_bikes = [] 

    for i in ch2021.riders :
        for j in i.garage:
            if (onlyfree and j.isfree == 0):
                continue
            all_bikes.append({'rider_id' : i.id,
                              'rider_name': i.name,
                              'bike_id': j.id,
                              'bike_specs' : j.specs
            })

    if (all_bikes == []):
        abort(501, "No bike free")

    return(all_bikes)

def bike_getone(bike_id=0):
    global ch2021

    if (ch2021 == None) :
        abort(500, "The Championship does not exist yet")

    for i in ch2021.riders :
        for j in i.garage:
            if (j.id == bike_id) :
                return ({'rider_id' : i.id,
                        'rider_name': i.name,
                        'bike_id': j.id,
                        'bike_specs' : j.specs
                })
    abort(501, "Bike not found")

def whatcanichoose():
    global ch2021

    if (ch2021 == None) :
        abort(500, "The Championship does not exist yet")

    if ((len(ch2021.races) % 2) == 0) :
        return "racetype"
    else :
        return "circuit"

def choice():
    global ch2021

    if (ch2021 == None) :
        abort(500, "The Championship does not exist yet")

    choice = request.get_json() # The body of the request

    # find the human and the quantum rider
    for i in ch2021.riders :
        if (i.quantum == 1 ) :
           quantum = i
        elif (i.quantum == 0) :
            human = i
    
    # assign the bikes
    human_bike = None
    for i in human.garage :
        if (i.id == choice['bike_id'] and i.isfree == 1) : 
            human_bike = i
            break
    if (human_bike == None) :
        abort(501, "The bike you have chosen is not free")
    quantum_bike = None
    for i in quantum.garage :
        if (i.isfree):
            quantum_bike = i # The first available... for the moment. That will be a quantum choice
            break
    if (quantum_bike == None) :
        abort(501, "Cannot choose a quantum bike")
   
   # assign the type of race and the circuit, depending on the turn
    if ((len(ch2021.races) % 2) == 0) :
        # Even turn : human chooses the racetype.... 
        if ( choice['race_type'] in ['normal', 'fool']) :
            racetype = choice['race_type']
        else :
            abort(501, "This choice for the race type is not possible")
        # ...and the quantum chooses the circuit
        ch2021.select_freecircuitrace(quantum=1)
        circuitrace = ch2021.races[-1]  # the last call appends a race with an assigned circuit
        
    else :
        # Uneven turn: human chooses the circuit....
        for i in ch2021.available_races :
            if ( (i.circuit.id == choice['circuit_id']) and 
               (i.circuit.isfree == 1) ) :
               ch2021.races.append(i)
               circuitrace = ch2021.races[-1]
               break

        if (circuitrace == None ) :
            abort(501, "This choice for the circuit is not possible")
        # ...and the quantum chooses the racetype
        if ( circuitrace.select_racetype(quantum=1) == 1 ) :
            racetype = 'normal'
        else :
            racetype = 'fool'

    # Now, we are ready to run        
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

    # Communicate the results
    response={}
    response['circuit_name'] = circuitrace.circuit.name
    response['circuit_type'] = circuitrace.circuit.type_text[circuitrace.circuit.type]
    response['critical_spec'] = circuitrace.win_criteria[circuitrace.circuit.type_text[circuitrace.circuit.type]]
    response['human_bike'] = human_bike.specs
    response['quantum_bike'] = quantum_bike.specs
    response['race_type'] = racetype
    if (result == 0) :
        response['race_prize_name'] = 'Both'
        response['race_prize_id'] = -1
    else :
        response['race_prize_name'] = result.name
        response['race_prize_id'] = result.id
    response['human_points'] = human.points
    response['quantum_points'] = quantum.points

    return(response)
 
