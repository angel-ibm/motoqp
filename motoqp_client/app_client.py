#!/usr/bin/env python3
# This is the main program that can be executed 
# from the command line ./app_client.py at any time
# no use of connexion here


##################
### FORMALISMS ###
##################
import os, json, requests
from ui_elements import Championship
from flask import Flask, render_template, request, redirect

serverurl = os.environ.get('MOTOQPAPI')
if (serverurl == None) :
	serverurl = 'http://0.0.0.0:5000/api'
	# serverurl = 'http://149.81.109.123:30672/api'
app = Flask(__name__)
ch2021 = None

##################
### initialize ###
##################

def initialize_championship() :

	global ch2021

	ch2021 = None
	ch2021 = Championship()

	callurl = serverurl + '/init'
	response = requests.delete(callurl)
	response = requests.post(callurl)
	response = requests.get(callurl)
	if (response.status_code != 200 ):
		print(response.text)
		exit(-1)
	response = response.json()
	ch2021.chname = response['chname']

	callurl = serverurl + '/rider'
	response = requests.get(callurl).json()
	for i in response:
		ch2021.riders[i['rider_type']]['rider_id'] = i['rider_id']
		ch2021.riders[i['rider_type']]['rider_name'] = i['rider_name']


	callurl = serverurl + '/bike'
	response = requests.get(callurl).json()
	for i in response :
		if ( i['rider_id'] == ch2021.riders['Quantum']['rider_id'] ) :
			next
		for j in ch2021.bikes :
			if (i['bike_id'] == ch2021.bikes[j]['bike_id']) :
				ch2021.bikes[j]['aerodyn'] = i['bike_specs']['aerodyn']
				ch2021.bikes[j]['braking'] = i['bike_specs']['braking']
				ch2021.bikes[j]['power'] = i['bike_specs']['power']
				ch2021.bikes[j]['speed'] = i['bike_specs']['speed']
				ch2021.bikes[j]['tyres'] = i['bike_specs']['tyres']


	callurl = serverurl + '/circuit'
	response = requests.get(callurl).json()
	for i in response:
		for j in ch2021.circuits :
			if (i['circuit_id'] == ch2021.circuits[j]['circuit_id']) :
				ch2021.circuits[j]['circuit_name'] = i['circuit_name']
				ch2021.circuits[j]['circuit_type'] = i['circuit_type']
				ch2021.circuits[j]['pic_type'] = ch2021.map_pics_circuit_types[i['circuit_type']]
				next

	callurl = serverurl + '/choice'
	response = requests.get(callurl)
	ch2021.next_choice = ''.join(filter(str.isalnum, response.text)) # clean the response
	if (ch2021.next_choice == 'racetype') :
		ch2021.message = ch2021.message + 'the type of race (normal / fool)'
	else :
		ch2021.message = ch2021.message + 'a circuit available for the race'

################
### run race ###
################

def run_race () :

    # adjust some values required by the API
	if (ch2021.choice['race_type'] == '') :
		ch2021.choice['race_type'] = 'normal' # irrelevant depending on the race, but valid value
	if (ch2021.choice['circuit_id'] == -1) :
		ch2021.choice['circuit_id'] = 1 # irrelevant depending on the race, but valid value

	# build the data to send
	reqbody = {
		"bike_id": int(ch2021.choice['bike_id']),
		"circuit_id": int(ch2021.choice['circuit_id']),
		"race_type": ch2021.choice['race_type'] 
	}
	callurl = serverurl + '/choice'
	response = requests.post(callurl, json=reqbody)

	# confirm that it was a valid race with valid choices
	if (response.status_code == 200 ):
		response = response.json()
	else :
		return (-1)

	# Now, evaluate who won and who got the prize
	ch2021.score["Championship"]["HumanPoints"] = str(response["human_points"])
	ch2021.score["Championship"]["QuantumPoints"] = str(response["quantum_points"])
	
	if (response["race_prize_id"] == -1) :  # No winner
		ch2021.last_winner = ch2021.score[ch2021.current_race]["Winner"] = "None"
		ch2021.last_prize = ch2021.score[ch2021.current_race]["Prize"] = "Both"
		ch2021.score[ch2021.current_race]["HumanPoints"] = '1'
		ch2021.score[ch2021.current_race]["QuantumPoints"] = '1'

	elif (ch2021.riders["Human"]["rider_id"] ==  response["race_prize_id"] ): # Human gets the prize
		ch2021.last_prize = ch2021.score[ch2021.current_race]["Prize"] = ch2021.riders['Human']['rider_name'].split()[0]
		ch2021.score[ch2021.current_race]["HumanPoints"] = '2'
		ch2021.score[ch2021.current_race]["QuantumPoints"] = '0'
		if (response['race_type'] == 'normal' ) : # in normal races, human was the winner
			ch2021.last_winner = ch2021.score[ch2021.current_race]["Winner"] = ch2021.riders['Human']['rider_name'].split()[0]		
		else :
			ch2021.last_winner = ch2021.score[ch2021.current_race]["Winner"] = ch2021.riders['Quantum']['rider_name'].split()[0]
	else : # Quantum gets the prize
		ch2021.last_prize = ch2021.score[ch2021.current_race]["Prize"] = ch2021.riders['Quantum']['rider_name'].split()[0]
		ch2021.score[ch2021.current_race]["HumanPoints"] = '0'
		ch2021.score[ch2021.current_race]["QuantumPoints"] = '2'
		if (response['race_type'] == 'normal' ) : # in normal races, quantum was the winner
			ch2021.last_winner = ch2021.score[ch2021.current_race]["Winner"] = ch2021.riders['Quantum']['rider_name'].split()[0]
		else :
			ch2021.last_winner = ch2021.score[ch2021.current_race]["Winner"] = ch2021.riders['Human']['rider_name'].split()[0]
    
	# get the specs of the quantum bike to display them
	ch2021.specs_bike_quantum['aerodyn']  = ch2021.bikes['Bike0']['aerodyn'] = response['quantum_bike']['aerodyn']
	ch2021.specs_bike_quantum['braking']  = ch2021.bikes['Bike0']['braking'] = response['quantum_bike']['braking']
	ch2021.specs_bike_quantum['power'] = ch2021.bikes['Bike0']['power'] = response['quantum_bike']['power']
	ch2021.specs_bike_quantum['speed'] = ch2021.bikes['Bike0']['speed'] = response['quantum_bike']['speed']
	ch2021.specs_bike_quantum['tyres'] = ch2021.bikes['Bike0']['tyres'] = response['quantum_bike']['tyres']


	# get the choices provided by the API to compensate for the adjustments done in the beginning
	ch2021.race_racetype = response['race_type']
	ch2021.race_circuitype  = response['circuit_type']
	ch2021.race_circuitname = response['circuit_name']
	ch2021.race_criticalspec = response['critical_spec'] 
	ch2021.pic_racetype_logo = ch2021.map_pics_racetypes[ch2021.race_racetype]['pic_racetype_logo']
	ch2021.pic_racetype_title = ch2021.map_pics_racetypes[ch2021.race_racetype]['pic_racetype_title']
	for circuitindex in ch2021.circuits :
		if ( ch2021.circuits[circuitindex]['circuit_name'] == ch2021.race_circuitname ) :
			ch2021.pic_circuit = ch2021.circuits[circuitindex]['pic']
			ch2021.pic_circuit_type = ch2021.circuits[circuitindex]['pic_type']
			break


#####################
### reset choices ###
#####################

def reset_choices() :

	ch2021.confirmed_selections = "no"
	for i in ch2021.circuits :
		if (ch2021.race_circuitname  == ch2021.circuits[i]['circuit_name']) :
			ch2021.freecircuit[i] = "no"
			break
		
	ch2021.choice = {"bike_id": -1, "circuit_id": -1, "race_type": ''}
	callurl = serverurl + '/choice'
	response = requests.get(callurl)
	ch2021.next_choice = ''.join(filter(str.isalnum, response.text)) # clean the response
	if (ch2021.next_choice == 'racetype') :
		ch2021.message = 'Select one free bike and the type of race (normal / fool)'
	else :
		ch2021.message = 'Select one free bike and one available circuit'
	
	# reset all bikes... who knows what the user clicked before
	for i in (ch2021.freebike) :
		ch2021.freebike[i] = 'no'
	callurl = serverurl + '/bike?onlyfree=true'
	response = requests.get(callurl).json()
	for i in response :
		if ( i['rider_id'] == ch2021.riders['Quantum']['rider_id'] ) :
			next
		bikeindex="Bike"+str(i['bike_id'])
		ch2021.freebike[bikeindex] = 'yes'

	# reset all circuits... who knows what the user clicked before
	for i in (ch2021.freecircuit) :
		ch2021.freecircuit[i] = 'no'
	callurl = serverurl + '/circuit?onlyfree=true'
	response = requests.get(callurl).json()
	for i in response :
		circuitindex="Circuit"+str(i['circuit_id'])
		ch2021.freecircuit[circuitindex] = 'yes'
	ch2021.pic_bike_human=''
	ch2021.pic_bike_quantum = ''
	ch2021.pic_circuit=''
	ch2021.pic_circuit_type=''
	ch2021.pic_racetype_logo = ''
	ch2021.pic_racetype_title = ''
	ch2021.specs_bike_human = {"speed": -1,"power": -1,"braking": -1,"aerodyn": -1,"tyres": -1}



#########################
### prepare next race ###
#########################

def prepare_next_race() :

	ch2021.current_race = next(ch2021.races)

	if (ch2021.current_race == "Podium") : # championship is over
		ch2021.message = 'The winner of the Championship is'
		if (ch2021.score["Championship"]["HumanPoints"] == ch2021.score["Championship"]["QuantumPoints"]) :
			 ch2021.message = 'No winner in this Championship'
		else :
			ch2021.message = 'The winner of the Championship is '
			if (ch2021.score["Championship"]["HumanPoints"] > ch2021.score["Championship"]["QuantumPoints"]) :
				ch2021.message = ch2021.message + ch2021.riders['Human']['rider_name']
			else :
				ch2021.message = ch2021.message + ch2021.riders['Quantum']['rider_name']
		return 

	reset_choices()


###############
### welcome ###
###############
@app.route('/')
def welcome():
	return render_template("Welcome.html")

##########################
### Browser dispatcher ###
##########################
@app.route('/<api>/')
@app.route('/<api>/<param>')
def dispatch(api, param='get'):

	global ch2021

	if ( api == 'init') :
		initialize_championship()
	elif (api == 'rider') : # will not happen, just for completeness
		callurl = serverurl + '/rider'
		response = requests.get(callurl) # do nothing
	elif (api == 'circuit') :
		callurl = serverurl + '/circuit'
		onlyfree = request.args.get('onlyfree', '')
		if ( onlyfree == 'true') :
			callurl = callurl + '?onlyfree=true'
		response = requests.get(callurl) # do nothing
	elif (api == 'bike') : # will not happen, just for completeness
		callurl = serverurl + '/bike'
		onlyfree= request.args.get('onlyfree', '')
		if ( onlyfree == 'true') :
			callurl = callurl + '?onlyfree=true'
		else :
			bike_id = request.args.get('bike_id', '')
			if (bike_id == '' and param.isdigit() ) :
				bike_id = str(param)
			if (bike_id != '' ) :
				callurl = callurl + '/' + bike_id
		response = requests.get(callurl)  # do nothing,
	elif (api == 'choice') :
		callurl = serverurl + '/choice'
		if (param == 'get') :
			response = requests.get(callurl)
			ch2021.next_choice = ''.join(filter(str.isalnum, response.text)) # clean the response

		elif (param == 'post') :

			bike_id = request.args.get('bike_id', '')

			if (bike_id != ''):
				bikeindex="Bike"+bike_id
				if (ch2021.freebike[bikeindex] == 'yes'): 
					ch2021.choice['bike_id'] = bike_id
					ch2021.pic_bike_human = ch2021.bikes[bikeindex]['pic']
					ch2021.specs_bike_human["aerodyn"] = ch2021.bikes[bikeindex]["aerodyn"]
					ch2021.specs_bike_human["braking"] = ch2021.bikes[bikeindex]["braking"]
					ch2021.specs_bike_human["power"] = ch2021.bikes[bikeindex]["power"]
					ch2021.specs_bike_human["speed"] = ch2021.bikes[bikeindex]["speed"]
					ch2021.specs_bike_human["tyres"] = ch2021.bikes[bikeindex]["tyres"]
					ch2021.confirmed_selections = 'no'

			circuit_id = request.args.get('circuit_id', '')

			if (circuit_id != '') :
				circuitindex = "Circuit"+circuit_id
				if (ch2021.freecircuit[circuitindex] == 'yes'): 
					ch2021.choice['circuit_id'] = circuit_id
					ch2021.pic_circuit = ch2021.circuits[circuitindex]['pic']
					ch2021.pic_circuit_type = ch2021.circuits[circuitindex]['pic_type']
					ch2021.confirmed_selections = 'no'					

			race_type = request.args.get('race_type', '')

			if (race_type != ''):
				ch2021.choice['race_type'] = race_type
				ch2021.pic_racetype_logo = ch2021.map_pics_racetypes[race_type]['pic_racetype_logo']
				ch2021.pic_racetype_title = ch2021.map_pics_racetypes[race_type]['pic_racetype_title']

			confirmed_selections = request.args.get('confirmed_selections', '')
			if (confirmed_selections != '') :
				if (confirmed_selections) == 'reset' :
					prepare_next_race()
					if (ch2021.current_race == "Podium") :
						return render_template("Podium.html", data = ch2021)
				else:
					ch2021.confirmed_selections = 'yes'
			
			if (ch2021.choice['bike_id'] != -1) :
				if ((ch2021.next_choice == 'racetype' and ch2021.choice['race_type'] != '') or
				    (ch2021.next_choice == 'circuit' and ch2021.choice['circuit_id'] != -1)) :
					if (ch2021.confirmed_selections == 'yes') :
						rc = run_race()
						if (rc == -1) :
							# ch2021.message = "Invalid choices, try again"
							# ch2021.confirmed_selections = 'no'
							reset_choices()
							ch2021.message = "Invalid choices. Try again:" + ch2021.message

						else :							
							ch2021.message = "Result of the race"
							return render_template("Results.html", data = ch2021)
					else :
						ch2021.message = "Review your selections"
						ch2021.confirmed_selections = 'ask'


	else :
		return "Error - no api call defined"

	return render_template("Selections.html", data = ch2021)


############
### MAIN ###
############
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5555, debug=True)
	# app.run(debug=True, host='0.0.0.0', port=5555,  static_url_path='/static')
