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

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
from datetime import date

tickets= []

def setStatut(ticket):
    complet=True
    date_passe=False
    for i in ticket:
        if(ticket[i]==''):
            complet=False
    date_inter = datetime.strptime(ticket['date_inter'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
    today = date.today()
    print(today)
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
    print(request.data)
    print("fsdffs")
    with open("data.json") as json_file:
        json_data = json.load(json_file)
        data=json.loads(request.data)
        data=setStatut(data)
        json_data.append(data)
    with open("data.json", "w") as write_file:
        json.dump(json_data, write_file)

    res = make_response(jsonify({"message": "Element ajouté"}), 201)
    return res


@app.route('/api/ressources/modifyTicket', methods=['POST'])
def api_post():
    print(request.data)
    newdata=[]
    with open("data.json") as json_file:
        json_data = json.load(json_file)
        data=json.loads(request.data)
        for ticket in json_data:
            print(data)
            if (data['libel']==ticket['libel']):
                print("CEST LE MEME")
                newdata.append(data)
            else:
                newdata.append(ticket)
     
    with open("data.json", "w") as write_file:
        json.dump(newdata, write_file)  
 

    res = make_response(jsonify({"message": "Element ajouté"}), 201)
    return res



@app.route('/api/ressources/deleteTicket/<ticket_label>', methods=['DELETE'])
def api_delete(ticket_label):
    print(ticket_label)
    newdata=[]
    with open("data.json") as json_file:
        json_data = json.load(json_file)
        for ticket in json_data:
            if (ticket_label!=ticket['libel']):
                newdata.append(ticket)
    with open("data.json", "w") as write_file:
        json.dump(newdata, write_file)

    res = make_response(jsonify({"message": "Element supprimé"}), 201)
    return res


app.run()