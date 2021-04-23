#!/usr/bin/env python3

# Code written on python 3.9.2, please observe the general compatibility rules
# motoqp.py is the file for classes, methods and variables

from random import gauss
from random import randint
from qfunctions import quantum_select_type_race, quantum_assign_specs, quantum_select_circuit_type

####################
## WrongParameter ##
####################
##-- this is intended to catch the errors and generate understandable messages
##-- and not braking the program because of wrong values that could be 
##-- corrected in the user interface
class WrongParameterValue(Exception) :
    def __init__(self, parametervalue, parametername) :
        self.message = "Error:  " + str(parametervalue) + "  is not a valid value for " + parametername
        super().__init__(self.message)

###############################
##  THE ONLY GLOBAL VARIABLE ##
###############################

ch2021 = None # That will be global

##############
## CIRCUITS ##
##############

class circuit():
    type_text = (
        'unknown',   # code 0
        'straight',  # code 1
        'uphills',   # code 2
        'downhills', # code 3
        'windy',     # code 4
        'rainy'      # code 5
    )
    __TOTAL_CIRCUITS = 0  # global & hidden variable to find out quickly the max value
    
    def __init__(self,cirtype=0, name=''):
        self.id = circuit.__TOTAL_CIRCUITS
        self.isfree = 1 # =0 if a race has already been scheduled in this circuit
        circuit.__TOTAL_CIRCUITS = circuit.__TOTAL_CIRCUITS + 1
        self.name = name 
        if (type(cirtype) == int) :
            if ( cirtype < 0 or cirtype > 5 ) :
                raise WrongParameterValue(cirtype,"cirtype - type of circuit")
            if ( cirtype == 0 ) :
                self.type = randint(1,5)  # this can be done with a QUANTUM function
            else :
                self.type = cirtype
        else :
            try :
                self.type = circuit.type_text.index(cirtype)
            except :
                raise WrongParameterValue(cirtype, "cirtype - type of circuit")

################
## MOTORBIKES ##
################

class bike():
    spec_text = (    
        'unknown' ,  # code 0 
        'worst'   ,  # code 1 
        'bad'     ,  # code 2
        'average' ,  # code 3
        'good'    ,  # code 4
        'best'       # code 5
    )
    __TOTAL_BIKES = 0 # global & hidden variable to find out quickly the max value
    
    def __gen_spec(self, quantum=0):        
        n = 0
        while ( n <= 0 or n > 5 ) : 
            if (quantum == 0) :
                n = int(gauss(3,1.6)) 
            else :
                n = bike.spec_text.index(quantum_assign_specs())
        return(n)

    def __assign_spec(self,spec, n, quantum=0) :
        if (type(n) == int) :
            if ( n == 0 ) : 
                n = self.__gen_spec(quantum)
            else :
                if (n < 0 or n > 5) :
                    raise WrongParameterValue(n, spec)
            self.specs.update( { spec   : n   } )
        else :
            try : 
                self.specs.update( { spec  : bike.spec_text.index(n)   } )
            except :
                raise WrongParameterValue(n, spec )
    
    def __init__(self, speed=0, power=0, braking=0, aerodyn=0, tyres=0, bikename='', quantum=0): 
        self.id = bike.__TOTAL_BIKES + 1
        bike.__TOTAL_BIKES = bike.__TOTAL_BIKES + 1
        self.isfree = 1 # =0 if a race has already been scheduled with this bike
        self.name = bikename
        self.quantum = quantum # = 1 if it is a quantum rider
        self.specs = {
            'speed'   : 0,
            'power'   : 0,
            'braking' : 0,
            'aerodyn' : 0,
            'tyres'   : 0
        }
        self.__assign_spec('speed', speed, self.quantum)
        self.__assign_spec('power', power, self.quantum)
        self.__assign_spec('braking', braking, self.quantum)
        self.__assign_spec('aerodyn', aerodyn, self.quantum)
        self.__assign_spec('tyres', tyres, self.quantum)
        
    
############        
## RIDERS ##
############

class rider():
    __TOTAL_RIDERS = 0 # global & hidden variable to find out quickly the max value
    
    def __init__(self,name,numbikes=5,quantum=0):
        self.id = rider.__TOTAL_RIDERS
        rider.__TOTAL_RIDERS = rider.__TOTAL_RIDERS + 1
        self.name = name
        self.quantum = quantum
        self.garage = [] # list of bikes
        self.points = 0  # score in championship
        for _ in range(numbikes) : 
            self.garage.append( bike(quantum=self.quantum) )     

###########
## RACES ##
###########

class race():
    win_criteria = {                #  "type of circuit"  :  "specification that matters to win"
        'unknown'   : 'unknown',
        'straight'  : 'speed',
        'uphills'   : 'power', 
        'downhills' : 'braking',
        'windy'     : 'aerodyn',
        'rainy'     : 'tyres'
    }
    race_types = (
            'unknown',   # 0
            'normal',    # 1
            'fool'       # 2
    )
    __TOTAL_RACES = 0
    
    def __init__(self,racename, racecircuit):
        self.id = race.__TOTAL_RACES
        race.__TOTAL_RACES = race.__TOTAL_RACES + 1
        self.name = racename
        self.racetype = 0
        self.circuit = racecircuit
        self.riders = [] 
        self.bikes = []
        self.winner = 0
        self.prize = 0

    def select_racetype (self,quantum=0) :
        if (quantum == 0) :
            self.racetype = randint(1,2) # a normal random choice
        else :
            # a QUANTUM choice
            self.racetype = race.race_types.index(quantum_select_type_race())
        return(self.racetype)    

    def run(self, racetype, ridersandbikes, quantum=0) :
        if (self.racetype == 0) :
            if (type(racetype) == int): 
                if (racetype < 0 or racetype > 2) :
                    self.prize = -1
                    raise WrongParameterValue(racetype, "racetype - type of race normal/fool")
                if (racetype == 0) :
                    self.racetype = self.select_racetype(quantum)  
                else :
                    self.racetype = racetype
            else :
                try :
                    self.racetype = race.race_types.index(racetype)
                except :
                    self.prize = -1
                    raise WrongParameterValue(racetype, "racetype - type of race normal/fool")

        for i in range(len(ridersandbikes)) :
            self.riders.append(ridersandbikes[i][0])
            self.bikes.append(ridersandbikes[i][1])
            self.bikes[i].isfree = 0 # mark the bike as used

        # extract the relevant specification of the bike by looking up in the circuit and race dictionaries
        bike0_score = self.bikes[0].specs[race.win_criteria[circuit.type_text[self.circuit.type]]]
        bike1_score = self.bikes[1].specs[race.win_criteria[circuit.type_text[self.circuit.type]]]

        # calculate the winner and who gets the prize
        if (bike0_score != bike1_score) :
            if (bike0_score > bike1_score) :
                self.winner = ridersandbikes[0][0]
                if (race.race_types[self.racetype] == 'normal') :
                    self.prize = self.winner
                else:
                    self.prize = ridersandbikes[1][0]
            else :
                self.winner = ridersandbikes[1][0]
                if (race.race_types[self.racetype] == 'normal') :
                    self.prize = self.winner
                else:
                    self.prize = ridersandbikes[0][0]

        # assign the points
        if (self.prize == 0) :
            self.riders[0].points += 1
            self.riders[1].points += 1
        else :
            self.prize.points += 2

        return(self.prize)

###############################
##  THE ONLY GLOBAL VARIABLE ##
###############################

ch2021 = None # That will be of class championship

##################        
## CHAMPIONSHIP ##
##################

class championship():
    def __init__(self, name, chraces, chriders):
        self.name = name
        self.available_races = chraces
        self.riders = chriders
        self.races = []
        self.final = []
    
    def select_freecircuitrace (self, quantum=0) :
        # warning - infinite loop if you don't take care of what you are doing
        # ... I was too lazy to protect it ;-)     
         while True:
            if (quantum == 0) :
                trytype = randint(1,5)
            else :
                trytype = circuit.type_text.index(quantum_select_circuit_type())
            for i in self.available_races :
                if (i.circuit.type == trytype and
                    i.circuit.isfree == 1 ) :
                    self.races.append(i)
                    return (trytype)
                 
    def run(self,currace, curracetype, ridersandbikes) :    
        raceresult = currace.run(curracetype,ridersandbikes)
        if (raceresult != -1 ):
            currace.circuit.isfree = 0
        return(raceresult)
        
    def finalize(self) :

        race._race__TOTAL_RACES = 0
        rider._rider__TOTAL_RIDERS = 0
        bike._bike__TOTAL_BIKES = 0
        circuit._circuit__TOTAL_CIRCUITS = 0
        del self.available_races
        del self.races
        del self.riders 
       
