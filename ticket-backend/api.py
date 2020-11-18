# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import json
import flask
from flask import request, jsonify,make_response
from flask_cors import CORS
import datetime 
from datetime import datetime
from datetime import date
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

tickets= []

id=0
def get_id():
    global id
    id=id+1
    return str(id)


def setStatut(ticket):
    complet=True
    date_passe=False
    for i in ticket:
        if(ticket[i]==''):
            complet=False
    date_inter = datetime.strptime(ticket['date_inter'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
    today = date.today()
    if (date_inter<today):
        date_passe=True

    if(complet==False):
        ticket['statut']="Brouillon"
    elif(complet and date_passe):
        ticket['statut']="Terminé"
    else:
        ticket['statut']="Validé"
    return ticket




def setStatutListe(tickets):
    liste=[]
    for t in tickets:
        liste.append(setStatut(t))
    with open("data.json", "w") as write_file:
        json.dump(liste, write_file)
    return liste


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/ressources/tickets', methods=['GET'])
def api_tickets():
    with open("data.json") as json_file:
        json_data = json.load(json_file)
        json_data=setStatutListe(json_data)
        return jsonify(json_data)
    
@app.route('/api/ressources/putTickets', methods=['PUT'])
def api_put():
    with open("data.json") as json_file:
        json_data = json.load(json_file)
        data=json.loads(request.data)
        data=setStatut(data)
        data["id"]=get_id()
        json_data.append(data)
    with open("data.json", "w") as write_file:
        json.dump(json_data, write_file)

    res = make_response(jsonify({"message": "Element ajouté"}), 201)
    return res


@app.route('/api/ressources/modifyTicket', methods=['POST'])
def api_post():
    newdata=[]
    with open("data.json") as json_file:
        json_data = json.load(json_file)
        data=json.loads(request.data)
        print((data['id']))
        for ticket in json_data:
            print(data)
            if (int(data['id'])==ticket['id']):
                newdata.append(data)
            else:
                newdata.append(ticket)
     
    with open("data.json", "w") as write_file:
        json.dump(newdata, write_file)  
 

    res = make_response(jsonify({"message": "Element ajouté"}), 201)
    return res



@app.route('/api/ressources/deleteTicket/<ticket_id>', methods=['DELETE'])
def api_delete(ticket_id):
    newdata=[]
    with open("data.json") as json_file:
        json_data = json.load(json_file)
        print(ticket_id)
        for ticket in json_data:
            if (int(ticket_id)!=ticket['id']):
                newdata.append(ticket)
    with open("data.json", "w") as write_file:
        json.dump(newdata, write_file)

    res = make_response(jsonify({"message": "Element supprimé"}), 201)
    return res


app.run()