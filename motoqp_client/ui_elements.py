#!/usr/bin/env python3

# many weird definitions caused by the Flask macro handling in Adobe XD

class Championship():  
	def __init__(self): 
		self.chname = ''
		self.riders = {
			"Human" : {
				"rider_id" : -1,
				"rider_name" : ''
			},
			"Quantum" : {
				"rider_id" : -1,
				"rider_name" : ''
			}
		}
		self.bikes = {
			"Bike0": { # the current quantum bike
				"bike_id": 0,
				"used" : 0,
				"aerodyn": -1,
				"braking": -1,
				"power": -1,
				"speed": -1,
				"tyres": -1,
				"pic" : ""
			},
			"Bike1":  {
				"bike_id": 1,
				"used" : 0,
				"aerodyn": -1,
				"braking": -1,
				"power": -1,
				"speed": -1,
				"tyres": -1,
				"pic" : "Grupo_54_d"
			}, 
			"Bike2":  {
				"bike_id": 2,
				"used" : 0,
				"aerodyn": -1,
				"braking": -1,
				"power": -1,
				"speed": -1,
				"tyres": -1,
				"pic": "Rectngulo_35"
			}, 
			"Bike3":  {
				"bike_id": 3,
				"used" : 0,
				"aerodyn": -1,
				"braking": -1,
				"power": -1,
				"speed": -1,
				"tyres": -1,
				"pic" : "Grupo_88_ea"
			}, 
			"Bike4":  {
				"bike_id": 4,
				"used" : 0,
				"aerodyn": -1,
				"braking": -1,
				"power": -1,
				"speed": -1,
				"tyres": -1,
				"pic" : "Grupo_100"
			}, 
			"Bike5":  {
				"bike_id": 5,
				"used" : 0,
				"aerodyn": -1,
				"braking": -1,
				"power": -1,
				"speed": -1,
				"tyres": -1,
				"pic" : "Grupo_95_ee"
			}
		}
		self.circuits = {
			"Circuit0" :  {
				"circuit_id": 0,
      			"circuit_name": '',
      			"circuit_type": '',
				"pic" : 'Grupo_146_eu' ,
				"pic_type" : ''
			}, 
			"Circuit1" : {
				"circuit_id": 1,
      			"circuit_name": '',
      			"circuit_type": '',
				"pic" : 'Grupo_149_e' ,
				"pic_type" : ''
			}, 
			"Circuit2" : {
				"circuit_id": 2,
      			"circuit_name": '',
      			"circuit_type": '',
				"pic" : 'Grupo_152_e' ,
				"pic_type" : ''
			}, 
			"Circuit3" : {
				"circuit_id": 3,
      			"circuit_name": '',
      			"circuit_type": '',
				"pic" : 'Grupo_155_fc' ,
				"pic_type" : ''
			}, 
			"Circuit4" : {
				"circuit_id": 4,
      			"circuit_name": '',
      			"circuit_type": '',
				"pic" : 'Grupo_158_fi' ,
				"pic_type" : ''
			}
		}
		self.map_pics_circuit_types = {
			"straight"  : "Grupo_160",
			"uphills"   : "Grupo_165",
			"downhills" : "Grupo_170",
			"windy"     : "Grupo_175",
			"rainy"     : "Grupo_180"
		}	
		self.map_pics_racetypes = {
			"normal" : {
				"pic_racetype_logo"  : "Grupo_189_ga",
				"pic_racetype_title" : "Grupo_194"
			},
			"fool" : {
				"pic_racetype_logo"  : "Rectngulo_81_fv",
				"pic_racetype_title" : "Grupo_199"
			}
		}
		self.score = {
			"Race1": { 
				"Winner": '',
				"Prize": '',
				"HumanPoints": '',
				"QuantumPoints": ''
			},
			"Race2":{
				"Winner": '',
				"Prize": '',
				"HumanPoints": '',
				"QuantumPoints": ''
			},
			"Race3":{
				"Winner": '',
				"Prize": '',
				"HumanPoints": '',
				"QuantumPoints": ''
			},
			"Race4":{
				"Winner": '',
				"Prize": '',
				"HumanPoints": '',
				"QuantumPoints": ''
			},
			"Race5":{
				"Winner": '',
				"Prize": '',
				"HumanPoints": '',
				"QuantumPoints": ''
			},
			"Championship": {
				"HumanPoints": '',
				"QuantumPoints": ''
			}
		}
		self.freebike = { 
			"Bike1" : "yes",
			"Bike2" : "yes",
			"Bike3" : "yes",
			"Bike4" : "yes",
			"Bike5" : "yes"
		}
		self.freecircuit = {
			"Circuit0" : "yes",
			"Circuit1" : "yes",
			"Circuit2" : "yes",
			"Circuit3" : "yes",
			"Circuit4" : "yes"
		}
		self.last_winner = ''
		self.last_prize = ''
		self.choice = {"bike_id": -1, "circuit_id": -1, "race_type": ''}
		self.next_choice = ''
		self.message = 'Select one bike and '
		self.specs_bike_human = {"speed": -1,"power": -1,"braking": -1,"aerodyn": -1,"tyres": -1}
		self.specs_bike_quantum = {"speed": -1,"power": -1,"braking": -1,"aerodyn": -1,"tyres": -1}
		self.pic_bike_human=''
		self.pic_bike_quantum = ''
		self.pic_circuit=''
		self.pic_circuit_type=''
		self.pic_racetype_logo = ''
		self.pic_racetype_title = ''
		self.confirmed_selections = 'no'
		self.race_racetype = ''
		self.race_circuitype = ''
		self.race_circuitname = ''
		self.race_criticalspec = ''

		self.races = iter(("Race1", "Race2", "Race3", "Race4", "Race5", "Podium"))
		self.current_race = next(self.races)
		

		
